# True Random Number Generator (TRNG) using microphone noise as entropy source.
# Records ambient audio to extract true randomness from environmental noise.

import os
import time
import hashlib
import struct
import numpy as np
import threading
import queue
from collections import deque

try:
    import pyaudio
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("PyAudio not available. Install with: pip install pyaudio")
    print("Falling back to system entropy sources.")

class DIYRNGGenerator:
    def __init__(self, sample_rate=44100, chunk_size=1024):
        # Initialize TRNG generator with microphone parameters.
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.entropy_pool = bytearray()
        self.entropy_queue = queue.Queue(maxsize=1000)
        self.entropy_history = deque(maxlen=10000)
        self.audio = None
        self.stream = None
        self.collecting = False
        self.collection_thread = None
        
        if AUDIO_AVAILABLE:
            self._setup_audio()
            self._start_continuous_collection()
        
        self._collect_initial_entropy()
    
    def _setup_audio(self):
        # Setup audio recording for entropy collection.
        try:
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            print("Microphone initialized for entropy collection")
        except Exception as e:
            print(f"Failed to initialize microphone: {e}")
            self.audio = None
            self.stream = None
    
    def _collect_initial_entropy(self):
        # Collect initial entropy from various sources including microphone.

        # Microphone entropy (primary source)
        if self.stream and not self.stream.is_stopped():
            mic_entropy = self._collect_microphone_entropy()
            self.entropy_pool.extend(mic_entropy)
        
        # System entropy (fallback)
        self.entropy_pool.extend(os.urandom(32))
        
        # High-resolution timestamp
        timestamp = time.time_ns()
        self.entropy_pool.extend(struct.pack('Q', timestamp))
        
        # Process ID
        self.entropy_pool.extend(struct.pack('I', os.getpid()))
    
    def _start_continuous_collection(self):
        # Start continuous entropy collection in background thread.
        if not self.stream:
            return
        
        self.collecting = True
        self.collection_thread = threading.Thread(target=self._continuous_entropy_collection, daemon=True)
        self.collection_thread.start()
    
    def _continuous_entropy_collection(self):
        # Continuously collect entropy from microphone.
        while self.collecting and self.stream and not self.stream.is_stopped():
            try:
                entropy = self._collect_microphone_entropy()
                if not self.entropy_queue.full():
                    self.entropy_queue.put(entropy)
                time.sleep(0.01)  # Small delay to prevent overwhelming
            except Exception as e:
                print(f"Error in continuous collection: {e}")
                time.sleep(0.1)
    
    def _collect_microphone_entropy(self):
        # Collect entropy from microphone noise with advanced processing.
        if not self.stream or self.stream.is_stopped():
            return os.urandom(32)
        
        try:
            # Record audio sample
            audio_data = self.stream.read(self.chunk_size // 2, exception_on_overflow=False)
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            
            entropy_bytes = bytearray()
            
            # 1. Extract LSBs with von Neumann debiasing
            lsb_bits = audio_array & 0x01
            debiased_bits = self._von_neumann_debias(lsb_bits)
            entropy_bytes.extend(debiased_bits)
            
            # 2. Use spectral analysis for high-frequency noise
            if len(audio_array) >= 64:
                fft_data = np.fft.fft(audio_array)
                high_freq = np.abs(fft_data[len(fft_data)//2:])
                entropy_bytes.extend((high_freq.astype(np.uint8) & 0x0F).tobytes())
            
            # 3. Second-order differences for better entropy
            if len(audio_array) > 2:
                diff1 = np.diff(audio_array)
                diff2 = np.diff(diff1)
                entropy_bytes.extend((diff2.astype(np.uint8) & 0x07).tobytes())
            
            # 4. Jitter measurements
            sample_times = []
            for i in range(min(10, len(audio_array))):
                start = time.time_ns()
                _ = audio_array[i] * 2  # Simple operation
                end = time.time_ns()
                sample_times.append(end - start)
            
            if sample_times:
                jitter_entropy = np.array(sample_times, dtype=np.uint64)
                entropy_bytes.extend((jitter_entropy & 0xFF).astype(np.uint8).tobytes())
            
            # 5. Mix with high-resolution timing
            timestamp = time.time_ns()
            entropy_bytes.extend(struct.pack('Q', timestamp))
            
            return bytes(entropy_bytes)
            
        except Exception as e:
            print(f"Error collecting microphone entropy: {e}")
            return os.urandom(32)
    
    def _von_neumann_debias(self, bits):
        # Apply von Neumann debiasing to remove statistical bias.
        debiased = []
        i = 0
        while i < len(bits) - 1:
            if bits[i] != bits[i + 1]:
                debiased.append(bits[i])
            i += 2
        return bytes(debiased)
    
    def _collect_additional_entropy(self):
        # Collect additional entropy from multiple sources.
        entropy_sources = bytearray()
        
        # 1. Queued entropy from continuous collection
        try:
            while not self.entropy_queue.empty():
                entropy_sources.extend(self.entropy_queue.get_nowait())
        except queue.Empty:
            pass
        
        # 2. Fresh microphone entropy
        fresh_entropy = self._collect_microphone_entropy()
        entropy_sources.extend(fresh_entropy)
        
        # 3. System entropy mixing
        entropy_sources.extend(os.urandom(16))
        
        # 4. CPU timing jitter
        jitter_samples = []
        for _ in range(20):
            start = time.time_ns()
            os.getpid()  # System call with variable timing
            end = time.time_ns()
            jitter_samples.append(end - start)
        
        jitter_array = np.array(jitter_samples, dtype=np.uint64)
        entropy_sources.extend((jitter_array & 0xFF).astype(np.uint8).tobytes())
        
        # 5. Memory allocation timing
        start = time.time_ns()
        temp_data = bytearray(1024)
        end = time.time_ns()
        entropy_sources.extend(struct.pack('Q', end - start))
        
        return bytes(entropy_sources)
    
    def next(self):
        # Generate next random number using true entropy with cryptographic whitening.

        # Collect fresh entropy
        entropy = self._collect_additional_entropy()
        
        # Add to entropy history for analysis
        self.entropy_history.extend(entropy[:100])
        
        # Multi-stage entropy conditioning
        # Stage 1: SHA-256 mixing
        hasher1 = hashlib.sha256()
        hasher1.update(self.entropy_pool)
        hasher1.update(entropy)
        stage1_hash = hasher1.digest()
        
        # Stage 2: SHA-512 for better mixing
        hasher2 = hashlib.sha512()
        hasher2.update(stage1_hash)
        hasher2.update(entropy[-32:])  # Use different portion of entropy
        stage2_hash = hasher2.digest()
        
        # Stage 3: XOR folding for final output
        hash_part1 = stage2_hash[:32]
        hash_part2 = stage2_hash[32:]
        xor_result = bytes(a ^ b for a, b in zip(hash_part1, hash_part2))
        
        # Get 4 bytes from final result
        random_int = struct.unpack('I', xor_result[:4])[0]
        
        # Update entropy pool with mixed entropy
        self.entropy_pool = bytearray(xor_result[4:28])
        
        return random_int
    
    def generate_sequence(self, n):
        # Generate sequence of n random numbers.
        return [self.next() for _ in range(n)]
    
    def normalized_next(self):
        # Generate normalized random number between 0 and 1.
        return self.next() / 0xFFFFFFFF
    
    def normalized_sequence(self, n):
        # Generate sequence of n normalized random numbers.
        return [self.normalized_next() for _ in range(n)]
    
    def get_entropy_estimate(self):
        # Get rough estimate of entropy pool size.
        return len(self.entropy_pool)
    
    def refresh_entropy(self):
        # Refresh entropy pool with new system entropy.
        self._collect_initial_entropy()
    
    def get_audio_status(self):
        # Get status of audio recording.
        if not AUDIO_AVAILABLE:
            return "PyAudio not available"
        if not self.stream:
            return "Microphone not initialized"
        if self.stream.is_stopped():
            return "Microphone stopped"
        return "Microphone active"
    
    def get_entropy_quality_metrics(self):
        # Get metrics about entropy quality.
        if len(self.entropy_history) < 100:
            return {"status": "insufficient_data"}
        
        # Convert to numpy array for analysis
        data = np.array(list(self.entropy_history), dtype=np.uint8)
        
        # Calculate statistics
        mean = np.mean(data)
        std = np.std(data)
        
        # Entropy estimation (simple)
        unique_bytes = len(set(data))
        entropy_estimate = unique_bytes / 256.0
        
        # Serial correlation test
        if len(data) > 1:
            correlation = np.corrcoef(data[:-1], data[1:])[0, 1]
        else:
            correlation = 0
        
        return {
            "sample_size": len(data),
            "mean": mean,
            "std": std,
            "entropy_estimate": entropy_estimate,
            "unique_bytes": unique_bytes,
            "serial_correlation": correlation,
            "queue_size": self.entropy_queue.qsize()
        }
    
    def cleanup(self):
        # Clean up audio resources.
        self.collecting = False
        if self.collection_thread:
            self.collection_thread.join(timeout=1.0)
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()
        print("Audio resources cleaned up")
    
    def __del__(self):
        # Destructor to ensure cleanup.
        try:
            self.cleanup()
        except:
            pass