#!/usr/bin/env python3
"""
Script to plot tail latency and latency distribution from JSONL files.

This script reads latency data from a JSONL file (like april9_256_40.jsonl)
and generates two plots:
1. Tail Latency Metrics (P50, P90, P95, P99)
2. Latency Distribution (Histogram and CDF)

Usage:
    python plot_latency.py <jsonl_file>
    
Example:
    python plot_latency.py april9_256_40.jsonl
"""

import json
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def load_latencies_from_jsonl(filepath):
    """
    Load latency values from a JSONL file.
    
    Supports two formats:
    1. {"latency": <value>} - direct latency field
    2. {"latency": {"model1": <value>, "model2": <value>}} - nested latency dict
    
    Args:
        filepath: Path to the JSONL file
        
    Returns:
        list: List of latency values in seconds
    """
    latencies = []
    
    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                data = json.loads(line)
                
                # Check if latency field exists
                if 'latency' in data:
                    lat = data['latency']
                    
                    # Handle nested dictionary (multiple models)
                    if isinstance(lat, dict):
                        for model_name, model_latency in lat.items():
                            if model_latency is not None:
                                latencies.append(float(model_latency))
                    # Handle direct value
                    elif lat is not None:
                        latencies.append(float(lat))
                        
            except json.JSONDecodeError as e:
                print(f"Warning: Skipping invalid JSON at line {line_num}: {e}")
                continue
            except (ValueError, TypeError) as e:
                print(f"Warning: Skipping invalid latency value at line {line_num}: {e}")
                continue
    
    return latencies


def calculate_tail_latencies(latencies):
    """
    Calculate tail latency percentiles.
    
    Args:
        latencies: List of latency values
        
    Returns:
        dict: Dictionary with percentile values
    """
    if not latencies:
        return {}
    
    percentiles = [50, 90, 95, 99]
    results = {}
    
    for p in percentiles:
        results[f'P{p}'] = np.percentile(latencies, p)
    
    results['mean'] = np.mean(latencies)
    results['median'] = np.median(latencies)
    results['min'] = np.min(latencies)
    results['max'] = np.max(latencies)
    results['std'] = np.std(latencies)
    
    return results


def plot_tail_latency(latencies, output_file='tail_latency.png'):
    """
    Create a bar plot showing tail latency percentiles.
    
    Args:
        latencies: List of latency values
        output_file: Output filename for the plot
    """
    tail_metrics = calculate_tail_latencies(latencies)
    
    if not tail_metrics:
        print("No latency data to plot")
        return
    
    # Prepare data for plotting
    percentiles = ['P50', 'P90', 'P95', 'P99']
    values = [tail_metrics[p] for p in percentiles]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create bar plot
    bars = ax.bar(percentiles, values, color=['#2ecc71', '#f39c12', '#e74c3c', '#c0392b'], 
                   alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add value labels on top of bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.3f}s',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Styling
    ax.set_ylabel('Latency (seconds)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Percentile', fontsize=12, fontweight='bold')
    ax.set_title(f'Tail Latency Metrics\n(n={len(latencies)} requests)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add grid for better readability
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add statistics text box
    stats_text = (f"Mean: {tail_metrics['mean']:.3f}s\n"
                  f"Median: {tail_metrics['median']:.3f}s\n"
                  f"Std Dev: {tail_metrics['std']:.3f}s\n"
                  f"Min: {tail_metrics['min']:.3f}s\n"
                  f"Max: {tail_metrics['max']:.3f}s")
    
    ax.text(0.98, 0.97, stats_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Tail latency plot saved to: {output_file}")
    
    # Print statistics to console
    print("\n=== Tail Latency Statistics ===")
    for key, value in tail_metrics.items():
        print(f"{key}: {value:.3f} seconds")


def plot_latency_distribution(latencies, output_file='latency_distribution.png'):
    """
    Create a combined plot showing latency histogram and CDF.
    
    Args:
        latencies: List of latency values
        output_file: Output filename for the plot
    """
    if not latencies:
        print("No latency data to plot")
        return
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # --- Histogram ---
    # Calculate optimal number of bins using Freedman-Diaconis rule
    q75, q25 = np.percentile(latencies, [75, 25])
    iqr = q75 - q25
    bin_width = 2 * iqr / (len(latencies) ** (1/3))
    n_bins = int((max(latencies) - min(latencies)) / bin_width) if bin_width > 0 else 30
    n_bins = min(max(n_bins, 20), 100)  # Limit between 20 and 100 bins
    
    counts, bins, patches = ax1.hist(latencies, bins=n_bins, color='#3498db', 
                                      alpha=0.7, edgecolor='black', linewidth=0.5)
    
    # Color the bars by percentile
    percentile_90 = np.percentile(latencies, 90)
    percentile_95 = np.percentile(latencies, 95)
    percentile_99 = np.percentile(latencies, 99)
    
    for i, (patch, left_edge, right_edge) in enumerate(zip(patches, bins[:-1], bins[1:])):
        if left_edge >= percentile_99:
            patch.set_facecolor('#c0392b')  # P99+ in dark red
        elif left_edge >= percentile_95:
            patch.set_facecolor('#e74c3c')  # P95-P99 in red
        elif left_edge >= percentile_90:
            patch.set_facecolor('#f39c12')  # P90-P95 in orange
    
    ax1.set_xlabel('Latency (seconds)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax1.set_title(f'Latency Distribution - Histogram\n(n={len(latencies)} requests)', 
                  fontsize=13, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_axisbelow(True)
    
    # Add legend for color coding
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#3498db', alpha=0.7, label='< P90'),
        Patch(facecolor='#f39c12', alpha=0.7, label='P90-P95'),
        Patch(facecolor='#e74c3c', alpha=0.7, label='P95-P99'),
        Patch(facecolor='#c0392b', alpha=0.7, label='≥ P99')
    ]
    ax1.legend(handles=legend_elements, loc='upper right', fontsize=9)
    
    # --- CDF (Cumulative Distribution Function) ---
    sorted_latencies = np.sort(latencies)
    cdf = np.arange(1, len(sorted_latencies) + 1) / len(sorted_latencies) * 100
    
    ax2.plot(sorted_latencies, cdf, linewidth=2, color='#2c3e50', label='CDF')
    
    # Add percentile lines
    tail_metrics = calculate_tail_latencies(latencies)
    percentiles_to_mark = [
        ('P50', tail_metrics['P50'], '#2ecc71'),
        ('P90', tail_metrics['P90'], '#f39c12'),
        ('P95', tail_metrics['P95'], '#e74c3c'),
        ('P99', tail_metrics['P99'], '#c0392b')
    ]
    
    for label, value, color in percentiles_to_mark:
        ax2.axvline(x=value, linestyle='--', linewidth=1.5, color=color, alpha=0.7)
        ax2.axhline(y=float(label[1:]), linestyle='--', linewidth=1.5, color=color, alpha=0.7)
        # Add annotation
        ax2.text(value, float(label[1:]) - 5, f'{label}\n{value:.3f}s', 
                fontsize=9, ha='center', 
                bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.3))
    
    ax2.set_xlabel('Latency (seconds)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Cumulative Probability (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Latency Distribution - CDF\n(Cumulative Distribution Function)', 
                  fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_axisbelow(True)
    ax2.set_ylim(0, 105)
    ax2.legend(loc='lower right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Latency distribution plot saved to: {output_file}")


def main():
    """Main function to run the latency analysis."""
    if len(sys.argv) < 2:
        print("Usage: python plot_latency.py <jsonl_file>")
        print("\nExample:")
        print("  python plot_latency.py april9_256_40.jsonl")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Check if file exists
    if not Path(input_file).exists():
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    print(f"Loading latency data from: {input_file}")
    latencies = load_latencies_from_jsonl(input_file)
    
    if not latencies:
        print("Error: No valid latency data found in the file")
        sys.exit(1)
    
    print(f"Successfully loaded {len(latencies)} latency measurements")
    
    # Generate base filename for output plots
    base_name = Path(input_file).stem
    
    # Create plots
    print("\nGenerating plots...")
    plot_tail_latency(latencies, output_file=f'{base_name}_tail_latency.png')
    plot_latency_distribution(latencies, output_file=f'{base_name}_latency_distribution.png')
    
    print("\n✓ All plots generated successfully!")


if __name__ == '__main__':
    main()
