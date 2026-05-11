# Crystal Score for sequences of primes and their products

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This repository contains the code and data for the paper  
*"Crystal Score: A New Invariant for Classifying Integer Sequences"*.

We introduce the **Crystal Score** (λ₂/λ₁) – a spectral invariant derived from the transition matrix of quantized gaps.  
We apply it to:

- Prime numbers
- Consecutive prime products: `p_n × p_{n+1}` and `p_n × p_{n+1} × p_{n+2}`
- All semiprimes, twin primes, quadratic sequences, random walks, etc.

### Key result

The triple product `p_n × p_{n+1} × p_{n+2}` achieves an exceptionally high Crystal Score (**≈0.9715**), second only to deterministic quadratic sequences (≈0.998), and far above primes (≈0.41) and random walks (≈0.05).  
The Crystal Score clearly separates structured from chaotic sequences and outperforms Shannon entropy and autocorrelation in discriminative power.

## Repository structure
.
├── README.md
├── requirements.txt
├── crystal_score.py # core function
├── generate_sequences.py # generate all sequences (N=5000)
├── run_experiments.py # compute scores, compare invariants, produce plots
├── results/ # (auto-created) CSV files and figures
└── paper/ # template for the article

text

## How to reproduce

### Option 1: Run locally

```bash
git clone https://github.com/YOUR_USERNAME/crystal-score-prime-sequences.git
cd crystal-score-prime-sequences
pip install -r requirements.txt
python run_experiments.py
All results (tables, plots) will be saved in the results/ folder.
