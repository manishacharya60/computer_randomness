import math
import pyaudio
import hashlib
import numpy as np

# Record microphone noise
def get_microphone_noise(required_bits, rate=44100, chunk=1024):
    p = pyaudio.PyAudio()

    # Open microphone stream
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=chunk)
    
    print(f"Recording microphone noise for approximately {math.ceil(required_bits / (chunk * 16))} seconds...")
    frames = []
    total_bits = 0

    while total_bits < required_bits:
        data = stream.read(chunk)
        frames.append(np.frombuffer(data, dtype=np.int16))
        total_bits += chunk * 16  # Each sample is 16 bits

    stream.stop_stream()
    stream.close()
    p.terminate()

    return np.concatenate(frames)

# Extract least significant bits (LSBs) from microphone noise
def extract_entropy(noise_data):
    return noise_data & 1  

# Convert extracted bits into the desired number of random numbers with given decimal digit length
def bits_to_random_numbers(bit_array, num_digits, num_random_numbers):
    total_bits_needed = num_random_numbers * 10  
    bit_array = bit_array[:total_bits_needed]

    random_numbers = []
    for i in range(num_random_numbers):
        bits = bit_array[i * 10:(i + 1) * 10]  # Extract 10 bits (more than needed)
        num = int("".join(map(str, bits)), 2)  # Convert to integer
        lower_bound = 10**(num_digits - 1)
        upper_bound = (10**num_digits) - 1 
        final_num = lower_bound + (num % (upper_bound - lower_bound + 1))
        random_numbers.append(final_num)

    return random_numbers

# Hash random numbers using SHA-256 for enhanced randomness
def hash_random_numbers(random_numbers):
    hashed_numbers = []
    for num in random_numbers:
        hash_obj = hashlib.sha256(str(num).encode()) 
        hashed_numbers.append(int.from_bytes(hash_obj.digest(), "big") % (10**len(str(num))))

    return hashed_numbers

num_random_numbers = int(input("Enter the number of random numbers to generate: "))
num_digits = int(input("Enter the number of digits for each random number (e.g., 2, 3, 4, 5): "))

# Calculate the total number of bits required
required_bits = num_random_numbers * 10  # 10 bits per number (approximation)

# Run the TRNG
noise = get_microphone_noise(required_bits)
random_bits = extract_entropy(noise)
random_numbers = bits_to_random_numbers(random_bits, num_digits, num_random_numbers)
secure_random_numbers = hash_random_numbers(random_numbers)

print("\nGenerated Secure Random Numbers:")
for i, num in enumerate(secure_random_numbers):  
    print(f"{i+1}: {num}")
