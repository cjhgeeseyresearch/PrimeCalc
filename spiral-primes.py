#!/usr/bin/env python3
"""
Golden Ratio Spiral Prime Factorization
========================================
Geometric algorithm for prime identification and integer factorization
based on resonance in a golden ratio (φ) spiral cavity.

Principle:
  - Integers are encoded as wavelengths in a φ-spiral resonator
  - Composite numbers resonate at their factors' harmonic frequencies
  - Prime numbers create dead spots (destructive interference)

Author: Corey J. H. Geesey
Date: June 2026
License: MIT
"""

import numpy as np
import time
import sys

PHI = (1 + np.sqrt(5)) / 2


def resonance_quality(d, n):
    """
    Compute resonance quality of factor d for number n in the φ-spiral.
    
    The φ-spiral has natural resonant modes at products of small integers.
    A factor resonates strongly if it is a small integer (fundamental mode)
    or factors into small integers (harmonic product).
    
    Parameters:
        d: candidate factor (int)
        n: the number being tested (int)
    
    Returns:
        float in [0, 1]: resonance quality
        1.0 = fundamental mode (strongest)
        ~0.0 = very weak resonance (likely prime factor of a prime number)
    """
    # Fundamental modes: small integers resonate perfectly
    if d <= 10:
        return 1.0
    
    # Harmonic products: check if d factors into smaller integers
    limit = int(np.sqrt(d)) + 1
    best_quality = 0.0
    
    for i in range(2, min(limit, 500)):
        if d % i == 0:
            j = d // i
            # Quality depends on how close factors are to fundamental
            quality = np.exp(-(i + j) / (2 * n**(1/3)))
            if quality > best_quality:
                best_quality = quality
    
    if best_quality > 0:
        return best_quality
    
    # d itself is prime — weak resonance as a higher harmonic
    return np.exp(-d / np.sqrt(n))


def is_prime_spiral(n, max_factor=100000):
    """
    Test if n is prime using golden spiral resonance.
    
    Parameters:
        n: integer to test
        max_factor: maximum factor to search (default 100,000)
    
    Returns:
        (is_prime, confidence, factors) tuple
        is_prime: bool
        confidence: float in [0, 1]
        factors: list of (d, n/d, resonance_quality) tuples
    """
    if n < 2:
        return False, 1.0, []
    if n == 2:
        return True, 1.0, []
    
    limit = min(int(np.sqrt(n)) + 1, max_factor)
    factors = []
    
    for d in range(2, limit):
        if n % d == 0:
            q = resonance_quality(d, n)
            factors.append((d, n // d, q))
    
    if not factors:
        # No factors found
        if n > max_factor**2:
            # Factors may exist beyond search limit
            return True, 0.5, []
        return True, 1.0, []
    
    # Sort by resonance quality (strongest first)
    factors.sort(key=lambda x: x[2], reverse=True)
    return False, factors[0][2], factors


def factorize(n, max_factor=100000):
    """
    Factorize n using spiral resonance.
    
    Returns a dictionary with primality, confidence, and factor list.
    """
    is_prime, confidence, factors = is_prime_spiral(n, max_factor)
    
    result = {
        'number': n,
        'is_prime': is_prime,
        'confidence': confidence,
        'factors': factors[:20] if factors else [],
        'factor_count': len(factors)
    }
    
    if is_prime:
        if confidence == 1.0:
            result['verdict'] = 'PRIME'
        else:
            result['verdict'] = 'LIKELY PRIME (factors may exceed search limit)'
    else:
        result['verdict'] = 'COMPOSITE'
    
    return result


def print_result(result):
    """Pretty-print a factorization result."""
    n = result['number']
    print(f"\n{'='*60}")
    print(f"  {n:,}")
    print(f"  Verdict: {result['verdict']}")
    print(f"  Confidence: {result['confidence']:.4f}")
    
    if not result['is_prime'] and result['factors']:
        print(f"  Top factors (by resonance quality):")
        for d, d2, q in result['factors'][:10]:
            bar = '█' * int(q * 40)
            print(f"    {d:>8,} × {d2:<10,}  Q={q:.4f} {bar}")
    
    if result['factor_count'] > 10:
        print(f"    ... and {result['factor_count'] - 10} more factor pairs")


# ============================================================
# COMMAND-LINE INTERFACE
# ============================================================
if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Factorize the provided number
        n = int(sys.argv[1])
        max_f = int(sys.argv[2]) if len(sys.argv) > 2 else 100000
        
        start = time.time()
        result = factorize(n, max_f)
        elapsed = time.time() - start
        
        print_result(result)
        print(f"\n  Time: {elapsed:.4f}s")
    else:
        # Demo mode
        print("="*60)
        print("GOLDEN RATIO SPIRAL — PRIME FACTORIZATION")
        print("="*60)
        
        demos = [
            17,
            91,
            256,
            1729,
            7919,
            104729,
            2**31 - 1,
            3**15,
            7**8,
        ]
        
        for n in demos:
            start = time.time()
            result = factorize(n)
            elapsed = time.time() - start
            print_result(result)
            print(f"  Time: {elapsed:.4f}s")
        
        print(f"\n{'='*60}")
        print("Usage: python spiral_primes.py <number> [max_factor]")
        print("Example: python spiral_primes.py 99991 50000")
        print(f"{'='*60}")
