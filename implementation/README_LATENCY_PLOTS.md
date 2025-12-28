# Latency Plotting Tool

This directory contains tools to visualize tail latency and latency distribution from JSONL files.

## Files

- **`plot_latency.py`**: Main script to generate latency plots
- **`generate_sample_data.py`**: Utility script to generate sample data for testing
- **`april9_256_40.jsonl`**: Sample data file with 500 requests

## Generated Plots

The script generates two comprehensive plots:

### 1. Tail Latency Metrics (`*_tail_latency.png`)
- Bar chart showing P50, P90, P95, and P99 percentiles
- Color-coded bars (green → orange → red) indicating severity
- Statistics box with mean, median, std dev, min, and max values
- Values displayed on top of each bar

### 2. Latency Distribution (`*_latency_distribution.png`)
- **Left panel**: Histogram showing frequency distribution
  - Color-coded bins by percentile ranges (< P90, P90-P95, P95-P99, ≥ P99)
  - Helps identify latency patterns and outliers
  
- **Right panel**: Cumulative Distribution Function (CDF)
  - Shows what percentage of requests complete by each latency value
  - Percentile markers with values for P50, P90, P95, P99
  - Useful for understanding tail behavior

## Usage

### Basic Usage

```bash
python3 plot_latency.py <jsonl_file>
```

### Example

```bash
# Generate plots for april9_256_40.jsonl
python3 plot_latency.py april9_256_40.jsonl

# This will create:
# - april9_256_40_tail_latency.png
# - april9_256_40_latency_distribution.png
```

### Using with Other Files

```bash
# Works with any JSONL file containing latency data
python3 plot_latency.py no_lru_no_adap/latency_values.jsonl
python3 plot_latency.py cache_adap/inference_times.jsonl
```

## Input File Format

The script supports two JSONL formats:

### Format 1: Simple latency value
```json
{"latency": 5.234}
{"latency": 10.567}
```

### Format 2: Multiple models (nested dictionary)
```json
{"latency": {"model1": 5.234, "model2": 8.901}}
{"latency": {"model1": 10.567}}
```

The script automatically handles both formats and extracts all latency values.

## Requirements

Install required packages:

```bash
pip3 install numpy matplotlib
```

## Generating Sample Data

To generate a sample `april9_256_40.jsonl` file with 500 requests:

```bash
python3 generate_sample_data.py
```

This creates a file with realistic latency distribution:
- 70% normal latency (around 5s)
- 20% elevated latency (around 10s)
- 10% tail latency (around 20s)

## Output

The script outputs:
1. **Console statistics**: P50, P90, P95, P99, mean, median, min, max, std dev
2. **Two PNG files**: High-resolution (300 DPI) plots suitable for reports/papers

### Example Output

```
Loading latency data from: april9_256_40.jsonl
Successfully loaded 500 latency measurements

Generating plots...
Tail latency plot saved to: april9_256_40_tail_latency.png

=== Tail Latency Statistics ===
P50: 5.773 seconds
P90: 14.442 seconds
P95: 19.064 seconds
P99: 27.402 seconds
mean: 7.541 seconds
median: 5.773 seconds
min: 1.000 seconds
max: 35.394 seconds
std: 5.101 seconds

Latency distribution plot saved to: april9_256_40_latency_distribution.png

✓ All plots generated successfully!
```

## Understanding the Plots

### Tail Latency Bar Chart
- **P50 (Median)**: 50% of requests complete faster than this
- **P90**: 90% of requests complete faster than this (important SLA metric)
- **P95**: 95% of requests complete faster than this
- **P99**: 99% of requests complete faster than this (critical for worst-case)

### Histogram
- Shows the distribution shape (normal, bimodal, skewed, etc.)
- Color coding helps identify tail latency regions quickly
- High bars indicate common latency values

### CDF (Cumulative Distribution Function)
- Steep slope = most requests in that range
- Flat tail = wide spread in tail latencies
- Easier to read exact percentile values than histogram

## Tips

1. **Compare multiple runs**: Generate plots for different configurations to compare performance
2. **Identify outliers**: Look at the histogram to spot unusual patterns
3. **SLA validation**: Check if P95/P99 meet your service level objectives
4. **Performance tuning**: Focus on reducing P99 if tail latency is problematic

## Example Analysis

For `april9_256_40.jsonl` with 500 requests:
- **P50 (5.77s)**: Typical request completes in under 6 seconds
- **P90 (14.44s)**: 90% of users get response within 14 seconds
- **P99 (27.40s)**: 1% of users experience 27+ second delays
- **Tail behavior**: The gap between P95 (19s) and P99 (27s) suggests some high-latency outliers

## Troubleshooting

### No data loaded
- Check that the JSONL file contains a "latency" field
- Verify the file is not empty
- Ensure proper JSON formatting (one JSON object per line)

### Import errors
```bash
pip3 install numpy matplotlib
```

### Plots not generated
- Ensure you have write permissions in the current directory
- Check available disk space
