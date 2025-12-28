# Latency Visualization for april9_256_40.jsonl

This document describes how to visualize tail latency and latency distribution from the `april9_256_40.jsonl` file.

## Overview

The `visualize_latency.py` script generates two types of visualizations:

1. **Tail Latency (Percentiles)**: Shows P50, P90, P95, P99, and P99.9 percentiles
2. **Latency Distribution**: Histogram showing the frequency distribution of latency values

## File Structure

- `april9_256_40.jsonl` - Input data file containing 256 latency measurements
- `visualize_latency.py` - Python script for generating visualizations
- Generated outputs:
  - `tail_latency.png` - Tail latency percentile chart
  - `latency_distribution.png` - Latency distribution histogram
  - `combined_latency_visualization.png` - Combined view (optional)

## Data Characteristics

The `april9_256_40.jsonl` file contains latency values that:
- Start from a few seconds (minimum ~2s)
- Gradually increase through the dataset
- Reach thousands of seconds at the end (maximum ~5000s)
- Show a wide distribution with mean ~945s and median ~260s

## Usage

### Basic Usage (Separate Plots)

Generate two separate visualization files:

```bash
python3 visualize_latency.py
```

This creates:
- `tail_latency.png` - Bar chart showing percentile values
- `latency_distribution.png` - Color-coded histogram

### Combined Visualization

Generate a single file with both plots side-by-side:

```bash
python3 visualize_latency.py --combined
```

This creates:
- `combined_latency_visualization.png` - Both visualizations in one image

### Using a Different Input File

Visualize latency from any JSONL file:

```bash
python3 visualize_latency.py path/to/your/file.jsonl
```

### Custom Output Directory

Save plots to a specific directory:

```bash
python3 visualize_latency.py --output-dir ./results
```

### Full Options

```bash
python3 visualize_latency.py [input_file] [--output-dir DIR] [--combined]
```

**Arguments:**
- `input_file` - Path to JSONL file (default: `april9_256_40.jsonl`)
- `--output-dir DIR` - Output directory for plots (default: current directory)
- `--combined` - Create single combined visualization instead of separate plots

## Visualization Details

### Tail Latency Chart

- **Color Coding**: 
  - Green (P50) - Median latency
  - Orange (P90) - 90th percentile
  - Light Red (P95) - 95th percentile
  - Dark Red (P99, P99.9) - Tail latencies
- **Statistics Box**: Shows min, mean, median, max, and standard deviation
- **Value Labels**: Each bar shows the exact latency value in seconds

### Latency Distribution Chart

- **Color Coding**:
  - Green: Low latencies (< 100s)
  - Orange: Medium latencies (100-500s)
  - Red: High latencies (> 500s)
- **Bins**: 50 bins for detailed distribution view
- **Statistics Box**: Shows total samples, min, max, mean, and median
- **Legend**: Explains the color coding scheme

## Results Summary

For `april9_256_40.jsonl`:

| Metric | Value |
|--------|-------|
| Total Samples | 256 |
| Minimum | 2.13s |
| Median (P50) | 260.33s |
| Mean | 944.75s |
| P90 | 3235.20s |
| P95 | 4261.88s |
| P99 | 4893.11s |
| P99.9 | 4988.97s |
| Maximum | 4996.86s |
| Std Dev | 1397.20s |

## Dependencies

Required Python packages:
- `matplotlib` - For plotting
- `numpy` - For statistical calculations

Install with:
```bash
pip3 install matplotlib numpy
```

## Input File Format

The script expects JSONL files where each line contains a JSON object with a `latency` field:

```json
{"latency": 2.7165447515499075}
{"latency": 5.469128681757267}
{"latency": 9.554756591665388}
...
```

## Examples

### Example 1: Quick Visualization
```bash
python3 visualize_latency.py
```

### Example 2: Combined Plot in Custom Directory
```bash
mkdir -p visualization_results
python3 visualize_latency.py --output-dir visualization_results --combined
```

### Example 3: Analyze Different Dataset
```bash
python3 visualize_latency.py implementation/no_lru_no_adap/latency_values.jsonl
```

## Interpreting the Results

The visualizations for `april9_256_40.jsonl` show:

1. **High Tail Latency**: P99 is ~4893s, indicating that 1% of requests experience very high latency
2. **Wide Distribution**: Large standard deviation (1397s) shows high variability
3. **Skewed Distribution**: Mean (945s) is much higher than median (260s), indicating right skew
4. **Performance Issues**: The majority of latencies are in the hundreds to thousands of seconds range

This suggests potential performance bottlenecks or resource contention issues that cause some requests to take significantly longer than others.
