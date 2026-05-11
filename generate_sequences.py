import numpy as np
from sympy import primerange, isprime
import math

def generate_all_sequences(N=5000):
    """
    Generate all sequences used in the analysis.
    Returns a dictionary: name -> list of numbers.
    """
    # Primes
    primes = list(primerange(2, 10**7))[:N]
    
    # p_n * p_{n+1}
    prod1 = [primes[i] * primes[i+1] for i in range(N-1)]
    
    # p_n * p_{n+1} * p_{n+2}
    prod2 = [primes[i] * primes[i+1] * primes[i+2] for i in range(N-2)]
    
    # Squares
    squares = [i*i for i in range(1, N+1)]
    
    # Triangular numbers
    triangular = [i*(i+1)//2 for i in range(1, N+1)]
    
    # Cubes
    cubes = [i**3 for i in range(1, N+1)]
    
    # Fibonacci (only up to ~2000 to avoid huge numbers)
    fib = [0, 1]
    for _ in range(2, min(N, 2000)):
        fib.append(fib[-1] + fib[-2])
    
    # log(factorials) – stable
    fact_log = [math.log(math.factorial(i)) for i in range(1, min(N, 1000))]
    
    # Powers of 2
    powers2 = [2**i for i in range(min(N, 2000))]
    
    # Periodic sin
    periodic = 1000 + 500 * np.sin(np.linspace(0, 20*np.pi, N))
    
    # Random walk
    np.random.seed(42)
    random_walk = np.cumsum(np.random.normal(0, 1, N)) + 1000
    
    # Semiprimes (all numbers with exactly two prime factors)
    def gen_semiprime(limit=N*10):
        semiprimes = []
        for i in range(2, limit):
            if len([d for d in range(2, int(i**0.5)+1) if i % d == 0 and isprime(d) and isprime(i//d)]) >= 1:
                semiprimes.append(i)
            if len(semiprimes) >= N:
                break
        return semiprimes[:N]
    semiprimes = gen_semiprime()
    
    # Composite numbers
    composite = [i for i in range(4, N*10) if not isprime(i)][:N]
    
    # Twin primes (the primes that belong to a twin pair)
    twin_primes = []
    for p in primes:
        if isprime(p+2):
            twin_primes.append(p)
            twin_primes.append(p+2)
    twin_primes = sorted(set(twin_primes))[:N]
    
    # Additional combinations from the paper
    prod_skip = [primes[i] * primes[i+2] for i in range(N-2)]
    sum_sq = [primes[i]**2 + primes[i+1]**2 for i in range(N-1)]
    prod_sq = [primes[i]**2 * primes[i+1] for i in range(N-1)]
    sum_adj = [primes[i] + primes[i+1] for i in range(N-1)]
    sq_primes = [p**2 for p in primes[:N]]
    cube_primes = [p**3 for p in primes[:N]]
    
    # Log versions
    log_prod2 = [math.log(x) for x in prod2]
    diff_log_prod2 = np.diff(log_prod2).tolist()
    
    sequences = {
        "Squares (n^2)": squares,
        "Triangular numbers": triangular,
        "Cubes (n^3)": cubes,
        "p_n × p_{n+1} × p_{n+2}": prod2,
        "log(p_n × p_{n+1} × p_{n+2})": log_prod2,
        "diff(log(p_n...p_{n+2}))": diff_log_prod2,
        "p_n² × p_{n+1}": prod_sq,
        "p_n × p_{n+1}": prod1,
        "p_n² + p_{n+1}²": sum_sq,
        "Cubes of primes (p_n³)": cube_primes,
        "p_n × p_{n+2}": prod_skip,
        "Squares of primes (p_n²)": sq_primes,
        "p_n + p_{n+1}": sum_adj,
        "Twin primes": twin_primes,
        "Primes": primes,
        "All semiprimes": semiprimes,
        "Random walk": random_walk,
        "Periodic (sin)": periodic,
        "Composite numbers": composite,
        "log(factorials)": fact_log,
        "Fibonacci (int)": fib,
        "Powers of 2": powers2,
    }
    
    return sequences

if __name__ == "__main__":
    seqs = generate_all_sequences(2000)
    for name, seq in seqs.items():
        print(f"{name}: {len(seq)} elements")
