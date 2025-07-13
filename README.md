# Computer Randomness: Are Compuiters Really Random?

## Introduction

This project explores the fascinating world of random number generators (RNGs), from simple algorithms to complex systems that draw randomness from the real world. We implement and analyze several popular RNGs to understand their strengths, weaknesses, and ideal use cases. By the end of this exploration, you'll see that **not all randomness is created equal**!

---

## File Descriptions

-   `lcg_generator.py`: Implements the **Linear Congruential Generator (LCG)**, a simple and fast PRNG.
-   `xorshift_generator.py`: Contains the **XORShift generator**, another efficient PRNG that relies on bitwise operations.
-   `mt_generator.py`: Implements the **Mersenne Twister**, a widely used PRNG known for its large period and good statistical properties.
-   `csprng_generator.py`: Implements a **Cryptographically Secure Pseudorandom Number Generator (CSPRNG)** using Python's `secrets` module.
-   `diyrng_generator.py`: A **Do-It-Yourself True Random Number Generator (TRNG)** that sources entropy from microphone noise.
-   `test/analyze_generators.py`: A script to perform **statistical analysis** on the implemented RNGs and generate visualizations.

---

## Installation & Running the Code

### Prerequisites

Ensure you have **Python 3.8+** installed. Then install the dependencies either via:

```bash
pip install numpy matplotlib scipy seaborn pyaudio
```

Or using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Clone the Repository

```bash
git clone https://github.com/manishacharya60/computer_randomness.git
cd computer_randomness
```

### Run the Analysis

```bash
python test/analyze_generators.py
```

This will print a statistical summary and generate visualizations in the `test/` folder.

---

## Statistical Analysis

To understand how "random" these generators really are, we evaluate them using the following statistical metrics:

-   **Mean**: Should be close to `0.5` for uniform `[0, 1)` output.
-   **Variance**: Ideal is around `0.083`.
-   **Chi-Square Test (p-value)**: High value (> 0.05) suggests uniformity.
-   **Kolmogorov–Smirnov Test (p-value)**: Higher is better, measures full-distribution match.

---

## 🧠 Summary Table

| **Generator**             | **Mean** | **Variance** | **Chi-Square p-value** | **K-S Test p-value** | **Notes**                       |
| ------------------------- | -------- | ------------ | ---------------------- | -------------------- | ------------------------------- |
| **LCG (Good Parameters)** | 0.499664 | 0.082337     | 0.929049               | 0.760772             | Fast, good for basic tasks      |
| **LCG (Poor Parameters)** | 0.506017 | 0.083422     | 0.947698               | 0.230356             | Bias risk despite passing tests |
| **XORShift**              | 0.498804 | 0.082538     | 0.080238               | 0.583085             | Fast, not secure                |
| **Mersenne Twister**      | 0.500251 | 0.082759     | 0.364056               | 0.825626             | Reliable for general use        |
| **CSPRNG**                | 0.495870 | 0.084255     | 0.583243               | 0.194732             | Best for secure applications    |
| **TRNG (Microphone)**     | 0.501197 | 0.084420     | 0.340698               | 0.548200             | Real-world entropy source       |

---

## 💡 What This Means for Different Methods

-   **LCG (Good)**: Excellent statistical balance and efficiency. Ideal for fast simulations.
-   **LCG (Poor)**: Passes tests but can have structural bias. Unsafe for sensitive applications.
-   **XORShift**: Lightweight and efficient. Not cryptographically secure.
-   **Mersenne Twister**: Good general-purpose RNG. Avoid for security.
-   **CSPRNG**: Designed for unpredictability. Slightly off metrics are acceptable in this context.
-   **TRNG**: Great entropy source. With filtering, can be a solid seed for other RNGs.

---

## ✅ Conclusion

This project demonstrates that randomness is not a one-size-fits-all concept. The "best" random number generator depends entirely on the application. For simple simulations, an LCG or XORShift might be sufficient. For more robust statistical applications, the Mersenne Twister is a solid choice. And for anything requiring security, only a CSPRNG or a well-designed TRNG will do.

For a deeper dive into the concepts check out the [blog post](https://acharyamanish.net/blog/2025/are-computers-random/).
