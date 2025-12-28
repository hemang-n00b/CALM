#!/usr/bin/env python3
"""
Visualize latency data from april9_256_40.jsonl
Creates two visualizations:
1. Tail Latency (percentiles: P50, P90, P95, P99)
2. Latency Distribution (histogram)
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import argparse
from pathlib import Path
from matplotlib.patches import Patch


def load_latencies(file_path):
    """Load latency values from JSONL file"""
    latencies = []
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            try:
                data = json.loads(line)
                if 'latency' not in data:
                    print(f"Warning: Line {line_num} missing 'latency' key, skipping")
                    continue
                latencies.append(data['latency'])
            except json.JSONDecodeError as e:
                print(f"Warning: Line {line_num} has invalid JSON: {e}, skipping")
                continue
    return latencies


def calculate_percentiles(latencies):
    """Calculate percentile statistics for tail latency"""
    percentiles = [50, 90, 95, 99, 99.9]
    values = np.percentile(latencies, percentiles)
    
    stats = {
        'percentiles': percentiles,
        'values': values,
        'min': min(latencies),
        'max': max(latencies),
        'mean': np.mean(latencies),
        'median': np.median(latencies),
        'std': np.std(latencies)
    }
    return stats


def plot_tail_latency(latencies, output_file='tail_latency.png'):
    """Plot tail latency (percentiles)"""
    stats = calculate_percentiles(latencies)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot percentiles as bars
    percentile_labels = [f'P{int(p)}' for p in stats['percentiles']]
    colors = ['#2ecc71', '#f39c12', '#e74c3c', '#c0392b', '#8b0000']
    
    bars = ax.bar(percentile_labels, stats['values'], color=colors, alpha=0.7, edgecolor='black')
    
    # Add value labels on bars
    for bar, value in zip(bars, stats['values']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.2f}s',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Percentile', fontsize=12, fontweight='bold')
    ax.set_ylabel('Latency (seconds)', fontsize=12, fontweight='bold')
    ax.set_title('Tail Latency Distribution - april9_256_40.jsonl', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add statistics text box
    stats_text = f'Min: {stats["min"]:.2f}s\nMean: {stats["mean"]:.2f}s\nMedian: {stats["median"]:.2f}s\nMax: {stats["max"]:.2f}s\nStd Dev: {stats["std"]:.2f}s'
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
            fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Tail latency plot saved to: {output_file}")
    plt.close()
    
    return stats


def plot_latency_distribution(latencies, output_file='latency_distribution.png'):
    """Plot latency distribution as histogram"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create histogram
    n, bins, patches = ax.hist(latencies, bins=50, color='#3498db', 
                                alpha=0.7, edgecolor='black')
    
    # Color code the histogram by latency ranges
    # Low latencies (< 100s) - green
    # Medium latencies (100-500s) - yellow
    # High latencies (> 500s) - red
    for i, patch in enumerate(patches):
        if bins[i] < 100:
            patch.set_facecolor('#2ecc71')
        elif bins[i] < 500:
            patch.set_facecolor('#f39c12')
        else:
            patch.set_facecolor('#e74c3c')
    
    ax.set_xlabel('Latency (seconds)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax.set_title('Latency Distribution - april9_256_40.jsonl', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add legend for color coding
    legend_elements = [
        Patch(facecolor='#2ecc71', edgecolor='black', label='Low (< 100s)'),
        Patch(facecolor='#f39c12', edgecolor='black', label='Medium (100-500s)'),
        Patch(facecolor='#e74c3c', edgecolor='black', label='High (> 500s)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    # Add statistics
    stats_text = f'Total Samples: {len(latencies)}\nMin: {min(latencies):.2f}s\nMax: {max(latencies):.2f}s\nMean: {np.mean(latencies):.2f}s\nMedian: {np.median(latencies):.2f}s'
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
            fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Latency distribution plot saved to: {output_file}")
    plt.close()


def plot_combined_visualization(latencies, output_file='combined_latency_visualization.png'):
    """Create a combined visualization with both plots"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: Tail Latency (Percentiles)
    stats = calculate_percentiles(latencies)
    percentile_labels = [f'P{int(p)}' for p in stats['percentiles']]
    colors = ['#2ecc71', '#f39c12', '#e74c3c', '#c0392b', '#8b0000']
    
    bars = ax1.bar(percentile_labels, stats['values'], color=colors, alpha=0.7, edgecolor='black')
    
    for bar, value in zip(bars, stats['values']):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.2f}s',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax1.set_xlabel('Percentile', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Latency (seconds)', fontsize=11, fontweight='bold')
    ax1.set_title('Tail Latency (Percentiles)', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    stats_text = f'Mean: {stats["mean"]:.2f}s\nMedian: {stats["median"]:.2f}s\nMax: {stats["max"]:.2f}s'
    ax1.text(0.02, 0.98, stats_text, transform=ax1.transAxes,
            fontsize=8, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Plot 2: Latency Distribution (Histogram)
    n, bins, patches = ax2.hist(latencies, bins=50, color='#3498db', 
                                alpha=0.7, edgecolor='black')
    
    for i, patch in enumerate(patches):
        if bins[i] < 100:
            patch.set_facecolor('#2ecc71')
        elif bins[i] < 500:
            patch.set_facecolor('#f39c12')
        else:
            patch.set_facecolor('#e74c3c')
    
    ax2.set_xlabel('Latency (seconds)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Frequency', fontsize=11, fontweight='bold')
    ax2.set_title('Latency Distribution', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    legend_elements = [
        Patch(facecolor='#2ecc71', edgecolor='black', label='< 100s'),
        Patch(facecolor='#f39c12', edgecolor='black', label='100-500s'),
        Patch(facecolor='#e74c3c', edgecolor='black', label='> 500s')
    ]
    ax2.legend(handles=legend_elements, loc='upper right', fontsize=9)
    
    plt.suptitle('Latency Analysis - april9_256_40.jsonl', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Combined visualization saved to: {output_file}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description='Visualize latency data from JSONL file',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'input_file', 
        nargs='?',
        default='april9_256_40.jsonl',
        help='Path to input JSONL file (default: april9_256_40.jsonl)'
    )
    parser.add_argument(
        '--output-dir',
        default='.',
        help='Output directory for plots (default: current directory)'
    )
    parser.add_argument(
        '--combined',
        action='store_true',
        help='Create a single combined visualization (default: separate plots)'
    )
    
    args = parser.parse_args()
    
    # Load latencies
    print(f"Loading latencies from: {args.input_file}")
    latencies = load_latencies(args.input_file)
    print(f"Loaded {len(latencies)} latency values")
    print(f"Range: {min(latencies):.2f}s to {max(latencies):.2f}s")
    print()
    
    # Create output directory if it doesn't exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.combined:
        # Create combined visualization
        output_file = output_dir / 'combined_latency_visualization.png'
        plot_combined_visualization(latencies, str(output_file))
    else:
        # Create separate visualizations
        print("Creating visualizations...")
        
        # Tail latency plot
        tail_output = output_dir / 'tail_latency.png'
        stats = plot_tail_latency(latencies, str(tail_output))
        
        print("\nTail Latency Statistics:")
        for p, v in zip(stats['percentiles'], stats['values']):
            print(f"  P{p}: {v:.2f}s")
        print()
        
        # Distribution plot
        dist_output = output_dir / 'latency_distribution.png'
        plot_latency_distribution(latencies, str(dist_output))
    
    print("\nVisualization complete!")


if __name__ == '__main__':
    main()
