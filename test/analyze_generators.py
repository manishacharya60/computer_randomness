# Statistical analysis and visualization of random number generators.

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
from lcg_generator import LCGGenerator
from xorshift_generator import XORShiftGenerator
from diyrng_generator import DIYRNGGenerator
from mt_generator import MTGenerator
from csprng_generator import CSPRNGGenerator

def calculate_entropy(data):
    # Calculate Shannon entropy of data.

    # Convert to histogram
    hist, _ = np.histogram(data, bins=256, density=True)
    # Remove zeros to avoid log(0)
    hist = hist[hist > 0]
    # Calculate entropy
    return -np.sum(hist * np.log2(hist))

def analyze_generator(generator, name, n_samples=10000):
    # Analyze a random number generator.
    print(f"\n=== Analyzing {name} ===")
    
    # Generate samples
    samples = generator.normalized_sequence(n_samples)
    
    # Basic statistics
    mean = np.mean(samples)
    variance = np.var(samples)
    std_dev = np.std(samples)
    entropy = calculate_entropy(samples)
    
    print(f"Mean: {mean:.6f}")
    print(f"Variance: {variance:.6f}")
    print(f"Standard Deviation: {std_dev:.6f}")
    print(f"Entropy: {entropy:.6f}")
    
    # Statistical tests
    # Kolmogorov-Smirnov test for uniformity
    ks_statistic, ks_pvalue = stats.kstest(samples, 'uniform')
    print(f"KS Test (uniformity): statistic={ks_statistic:.6f}, p-value={ks_pvalue:.6f}")
    
    # Chi-square test for uniformity
    observed, _ = np.histogram(samples, bins=50)
    expected = np.full(50, n_samples/50)
    chi2_statistic, chi2_pvalue = stats.chisquare(observed, expected)
    print(f"Chi-square Test: statistic={chi2_statistic:.6f}, p-value={chi2_pvalue:.6f}")
    
    return {
        'name': name,
        'samples': samples,
        'mean': mean,
        'variance': variance,
        'std_dev': std_dev,
        'entropy': entropy,
        'ks_statistic': ks_statistic,
        'ks_pvalue': ks_pvalue,
        'chi2_statistic': chi2_statistic,
        'chi2_pvalue': chi2_pvalue
    }

def create_visualizations(results):
    # Create separate visualization files for each generator.
    for result in results:
        samples = result['samples']
        name = result['name']
        
        # Create figure with 3 subplots (removed Q-Q plot)
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle(f'{name} - Analysis', fontsize=16)
        
        # Histogram
        axes[0].hist(samples, bins=50, alpha=0.7, density=True)
        axes[0].set_title(f'{name} - Histogram')
        axes[0].set_xlabel('Value')
        axes[0].set_ylabel('Density')
        axes[0].axhline(y=1, color='red', linestyle='--', alpha=0.5, label='Uniform')
        axes[0].legend()
        
        # Scatter plot (x vs x+1)
        if len(samples) > 1:
            axes[1].scatter(samples[:-1], samples[1:], alpha=0.5, s=1)
            axes[1].set_title(f'{name} - Scatter Plot (x vs x+1)')
            axes[1].set_xlabel('x_n')
            axes[1].set_ylabel('x_{n+1}')
        
        # Autocorrelation plot
        autocorr = np.correlate(samples, samples, mode='full')
        autocorr = autocorr[autocorr.size // 2:]
        lags = np.arange(len(autocorr))
        axes[2].plot(lags[:100], autocorr[:100])
        axes[2].set_title(f'{name} - Autocorrelation')
        axes[2].set_xlabel('Lag')
        axes[2].set_ylabel('Correlation')
        
        plt.tight_layout()
        # Save each generator to its own file
        filename = f'{name.lower().replace(" ", "_").replace("(", "").replace(")", "")}_analysis.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

def create_comparison_plot(results):
    # Create separate comparison plots for mean/variance and entropy/k-test.
    names = [r['name'] for r in results]
    means = [r['mean'] for r in results]
    variances = [r['variance'] for r in results]
    entropies = [r['entropy'] for r in results]
    ks_stats = [r['ks_statistic'] for r in results]
    
    # Plot 1: Mean and Variance comparison
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Generator Comparison - Mean and Variance', fontsize=16)
    
    # Mean comparison
    axes[0].bar(names, means)
    axes[0].set_title('Mean Values')
    axes[0].set_ylabel('Mean')
    axes[0].axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='Expected (0.5)')
    axes[0].legend()
    axes[0].tick_params(axis='x', rotation=45)
    
    # Variance comparison
    axes[1].bar(names, variances)
    axes[1].set_title('Variance')
    axes[1].set_ylabel('Variance')
    axes[1].axhline(y=1/12, color='red', linestyle='--', alpha=0.5, label='Expected (1/12)')
    axes[1].legend()
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('generator_mean_variance.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 2: Entropy and K-S test comparison
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Generator Comparison - Entropy and K-S Test', fontsize=16)
    
    # Entropy comparison
    axes[0].bar(names, entropies)
    axes[0].set_title('Entropy')
    axes[0].set_ylabel('Entropy (bits)')
    axes[0].tick_params(axis='x', rotation=45)
    
    # KS test statistic comparison
    axes[1].bar(names, ks_stats)
    axes[1].set_title('KS Test Statistic (lower is better)')
    axes[1].set_ylabel('KS Statistic')
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('generator_entropy_ks.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # Main analysis function.
    print("Random Number Generator Analysis")
    print("="*50)
    
    # Initialize generators
    lcg = LCGGenerator(seed=42)
    xorshift = XORShiftGenerator(seed=42)
    mt = MTGenerator(seed=42)
    csprng = CSPRNGGenerator()
    trng = DIYRNGGenerator()
    
    # Poor LCG parameters for comparison
    poor_lcg = LCGGenerator(seed=1, modulus=2**16, multiplier=1103515245, increment=12345)
    
    # Analyze each generator
    results = []
    results.append(analyze_generator(lcg, "LCG (Good Parameters)"))
    results.append(analyze_generator(poor_lcg, "LCG (Poor Parameters)"))
    results.append(analyze_generator(xorshift, "XORShift"))
    results.append(analyze_generator(mt, "Mersenne Twister"))
    results.append(analyze_generator(csprng, "CSPRNG"))
    results.append(analyze_generator(trng, "TRNG"))
    
    # Create visualizations
    create_visualizations(results)
    create_comparison_plot(results)

if __name__ == "__main__":
    main()