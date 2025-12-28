#!/usr/bin/env python3
"""
Calculate per-model average inference time from inference_times2.jsonl

This script reads the inference_times2.jsonl file and calculates the average
inference time and standard deviation for each model present in the data.
"""

import json
from collections import defaultdict
import sys
import os
import math


def calculate_std_deviation(values, mean):
    """
    Calculate sample standard deviation for a list of values.
    
    Args:
        values: List of numeric values
        mean: Pre-calculated mean of the values
        
    Returns:
        Sample standard deviation
    """
    if len(values) < 2:
        return 0.0
    
    # Use sample standard deviation (n-1) for unbiased estimator
    variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
    return math.sqrt(variance)


def calculate_avg_inference_times(filepath):
    """
    Calculate average inference times and standard deviations per model from a JSONL file.
    
    Args:
        filepath: Path to the JSONL file containing inference time data
        
    Returns:
        Tuple of (model_averages, model_std_devs, model_times) dictionaries
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    
    model_times = defaultdict(list)
    
    # Read the JSONL file and collect inference times per model
    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                model = data['model']
                inf_time = data['inf_time']
                model_times[model].append(inf_time)
            except json.JSONDecodeError as e:
                print(f"Warning: Skipping invalid JSON on line {line_num}: {e}", file=sys.stderr)
            except KeyError as e:
                print(f"Warning: Missing key {e} on line {line_num}", file=sys.stderr)
    
    # Calculate averages and standard deviations
    model_averages = {}
    model_std_devs = {}
    for model, times in model_times.items():
        avg = sum(times) / len(times)
        model_averages[model] = avg
        model_std_devs[model] = calculate_std_deviation(times, avg)
    
    return model_averages, model_std_devs, model_times


def print_results(model_averages, model_std_devs, model_times):
    """
    Print the per-model average inference times and standard deviations in a formatted table.
    
    Args:
        model_averages: Dictionary mapping model names to average inference times
        model_std_devs: Dictionary mapping model names to standard deviations
        model_times: Dictionary mapping model names to list of inference times
    """
    print('Per Model Average Inference Time')
    print('=' * 75)
    print(f'{"Model":<20} {"Avg Time (s)":>12} {"Std Dev (s)":>12} {"Count":>8}')
    print('-' * 75)
    
    # Sort by model name for consistent output
    for model in sorted(model_averages.keys()):
        avg_time = model_averages[model]
        std_dev = model_std_devs[model]
        count = len(model_times[model])
        print(f'{model:<20} {avg_time:>12.4f} {std_dev:>12.4f} {count:>8}')
    
    print('=' * 75)
    
    # Print summary statistics
    all_times = []
    for times in model_times.values():
        all_times.extend(times)
    
    overall_avg = sum(all_times) / len(all_times)
    overall_std = calculate_std_deviation(all_times, overall_avg)
    total_samples = len(all_times)
    
    print(f'\nSummary:')
    print(f'  Total samples: {total_samples}')
    print(f'  Overall average: {overall_avg:.4f}s')
    print(f'  Overall std dev: {overall_std:.4f}s')
    print(f'  Number of models: {len(model_averages)}')


def main():
    """Main entry point for the script."""
    # Default file path
    default_filepath = 'implementation/cache_adap/inference_times2.jsonl'
    
    # Allow custom filepath from command line argument
    filepath = sys.argv[1] if len(sys.argv) > 1 else default_filepath
    
    print(f'Analyzing: {filepath}\n')
    
    # Calculate and display results
    model_averages, model_std_devs, model_times = calculate_avg_inference_times(filepath)
    print_results(model_averages, model_std_devs, model_times)


if __name__ == '__main__':
    main()
