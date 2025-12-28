#!/usr/bin/env python3
"""
Script to generate sample april9_256_40.jsonl file with 500 requests.
This creates realistic latency data for testing the plotting script.
"""

import json
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

def generate_sample_latencies(n_requests=500):
    """
    Generate sample latency data with realistic distribution.
    
    Most requests have normal latency, with some tail latency outliers.
    
    Args:
        n_requests: Number of requests to generate
        
    Returns:
        list: List of latency values
    """
    latencies = []
    
    # 70% normal latency (mean=5s, std=1.5s)
    normal_count = int(n_requests * 0.7)
    normal_latencies = np.random.normal(5.0, 1.5, normal_count)
    normal_latencies = np.clip(normal_latencies, 1.0, 10.0)  # Clip to reasonable range
    latencies.extend(normal_latencies)
    
    # 20% slightly elevated latency (mean=10s, std=2s)
    elevated_count = int(n_requests * 0.2)
    elevated_latencies = np.random.normal(10.0, 2.0, elevated_count)
    elevated_latencies = np.clip(elevated_latencies, 7.0, 15.0)
    latencies.extend(elevated_latencies)
    
    # 10% high tail latency (mean=20s, std=5s)
    tail_count = n_requests - normal_count - elevated_count
    tail_latencies = np.random.normal(20.0, 5.0, tail_count)
    tail_latencies = np.clip(tail_latencies, 15.0, 40.0)
    latencies.extend(tail_latencies)
    
    # Shuffle to mix the distributions
    np.random.shuffle(latencies)
    
    return latencies


def write_jsonl_file(filename, latencies):
    """
    Write latency data to a JSONL file.
    
    Args:
        filename: Output filename
        latencies: List of latency values
    """
    with open(filename, 'w') as f:
        for latency in latencies:
            record = {"latency": float(latency)}
            f.write(json.dumps(record) + '\n')
    
    print(f"Generated {len(latencies)} requests in {filename}")


def main():
    """Generate sample data file."""
    latencies = generate_sample_latencies(500)
    write_jsonl_file('april9_256_40.jsonl', latencies)
    
    # Print some statistics
    print(f"\nSample Statistics:")
    print(f"  Mean: {np.mean(latencies):.3f}s")
    print(f"  Median: {np.median(latencies):.3f}s")
    print(f"  P90: {np.percentile(latencies, 90):.3f}s")
    print(f"  P95: {np.percentile(latencies, 95):.3f}s")
    print(f"  P99: {np.percentile(latencies, 99):.3f}s")
    print(f"  Max: {np.max(latencies):.3f}s")


if __name__ == '__main__':
    main()
