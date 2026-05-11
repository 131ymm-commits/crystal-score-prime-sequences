import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import entropy
from crystal_score import crystal_score
from generate_sequences import generate_all_sequences

def shannon_entropy(seq):
    if len(seq) < 100:
        return np.nan
    gaps = np.diff(seq).astype(float)
    hist, _ = np.histogram(gaps, bins=32, density=True)
    hist = hist[hist > 0]
    return entropy(hist, base=2)

def autocorr_lag1(seq):
    if len(seq) < 100:
        return np.nan
    gaps = np.diff(seq)
    if np.std(gaps) < 1e-12:
        return 0.0
    return np.corrcoef(gaps[:-1], gaps[1:])[0,1]

def main():
    # Create results directory
    os.makedirs("results", exist_ok=True)
    
    # Generate sequences (N=2000 for speed, but you can increase)
    sequences = generate_all_sequences(N=2000)
    
    results = []
    for name, seq in sequences.items():
        cs = crystal_score(seq)
        ent = shannon_entropy(seq)
        acf = autocorr_lag1(seq)
        results.append({
            "Sequence": name,
            "Crystal Score": cs,
            "Shannon Entropy (bits)": ent,
            "Autocorr (lag1)": acf,
            "Length": len(seq)
        })
        print(f"{name:35} | CS={cs:.4f} | H={ent:.3f} | ACF={acf:.3f}")
    
    df = pd.DataFrame(results)
    df = df.dropna(subset=["Crystal Score"])
    df = df.sort_values("Crystal Score", ascending=False)
    
    # Save to CSV
    df.to_csv("results/crystal_scores_full.csv", index=False)
    print("\nSaved to results/crystal_scores_full.csv")
    
    # Print summary table
    print("\n" + "="*80)
    print("SUMMARY TABLE (sorted by Crystal Score)")
    print("="*80)
    print(df[["Sequence", "Crystal Score", "Shannon Entropy (bits)", "Autocorr (lag1)"]].to_string(index=False))
    
    # Plot comparison: Crystal Score vs Entropy
    plt.figure(figsize=(12,5))
    plt.subplot(1,2,1)
    plt.scatter(df["Shannon Entropy (bits)"], df["Crystal Score"], c='blue', s=60)
    for _, row in df.iterrows():
        plt.annotate(row["Sequence"], (row["Shannon Entropy (bits)"], row["Crystal Score"]),
                     fontsize=7, alpha=0.7)
    plt.xlabel("Shannon Entropy (bits)")
    plt.ylabel("Crystal Score")
    plt.title("Crystal Score vs Entropy")
    plt.grid(alpha=0.3)
    
    # Plot Crystal Score vs Autocorrelation
    plt.subplot(1,2,2)
    plt.scatter(df["Autocorr (lag1)"], df["Crystal Score"], c='red', s=60)
    for _, row in df.iterrows():
        plt.annotate(row["Sequence"], (row["Autocorr (lag1)"], row["Crystal Score"]),
                     fontsize=7, alpha=0.7)
    plt.xlabel("Autocorrelation (lag 1)")
    plt.ylabel("Crystal Score")
    plt.title("Crystal Score vs Autocorrelation")
    plt.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("results/comparison_plots.png", dpi=150)
    plt.show()
    print("\nFigure saved to results/comparison_plots.png")
    
    # Bar plot of Crystal Scores for key sequences
    key_names = [
        "Squares (n^2)", "p_n × p_{n+1} × p_{n+2}", "p_n × p_{n+1}",
        "Twin primes", "Primes", "All semiprimes", "Random walk"
    ]
    df_key = df[df["Sequence"].isin(key_names)]
    df_key = df_key.set_index("Sequence")
    plt.figure(figsize=(10,6))
    df_key["Crystal Score"].sort_values(ascending=True).plot(kind='barh', color='skyblue')
    plt.xlabel("Crystal Score")
    plt.title("Crystal Score for Selected Sequences (N=2000)")
    plt.tight_layout()
    plt.savefig("results/spectrum_bar.png", dpi=150)
    plt.show()
    print("Bar chart saved to results/spectrum_bar.png")
    
    print("\nAll results are in the 'results/' folder.")

if __name__ == "__main__":
    main()
