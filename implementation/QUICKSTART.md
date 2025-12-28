# Quick Start Guide - Latency Plotting

## For april9_256_40.jsonl (500 requests)

The plots have already been generated! Check these files:
- **`april9_256_40_tail_latency.png`** - Bar chart showing P50, P90, P95, P99 percentiles
- **`april9_256_40_latency_distribution.png`** - Histogram and CDF showing latency distribution

## View the Results

### Tail Latency Metrics (P50, P90, P95, P99)
```
P50:   5.773 seconds (median - half of requests complete faster)
P90:  14.442 seconds (90% of requests complete faster)
P95:  19.064 seconds (95% of requests complete faster)
P99:  27.402 seconds (99% of requests complete faster)
Mean:  7.541 seconds (average latency)
```

The bar chart uses color coding:
- 🟢 Green (P50): Normal performance
- 🟠 Orange (P90): Acceptable tail
- 🔴 Red (P95): High tail latency
- 🔴 Dark Red (P99): Worst-case latency

### Distribution Plots
The combined histogram and CDF plot shows:
- **Left**: Frequency distribution with color-coded percentile ranges
- **Right**: Cumulative probability showing what % of requests complete by each latency

## Regenerate or Customize

If you want to regenerate plots or use your own data:

```bash
# Regenerate plots for april9_256_40.jsonl
python3 plot_latency.py april9_256_40.jsonl

# Or create plots for a different file
python3 plot_latency.py your_latency_file.jsonl
```

## Generate New Sample Data

To create a new sample file with different characteristics:

```bash
# Edit generate_sample_data.py to adjust the distribution
# Then run:
python3 generate_sample_data.py
```

This creates a new `april9_256_40.jsonl` with 500 requests.

## Key Insights from Current Data

From the april9_256_40.jsonl analysis:
1. **Median latency (P50) is 5.77s** - Most requests are relatively fast
2. **P90 is 14.44s** - 10% of requests take longer (tail latency starts here)
3. **P99 is 27.40s** - 1% of requests experience high delays (27+ seconds)
4. **Large P95-P99 gap** - Indicates some significant outliers affecting user experience

## Understanding Your Results

- **Low P99/P95 ratio (< 2x)**: Consistent performance, minimal outliers
- **High P99/P95 ratio (> 3x)**: High variance, optimization needed
- **Current ratio**: 27.40/19.06 = 1.44x (relatively consistent)

For production systems:
- Target P99 < 2x P50 for good user experience
- Monitor P99 as it represents worst-case user experience
- Current data: P99/P50 = 27.40/5.77 = 4.75x (indicates tail latency issues)

## Next Steps

1. ✅ Plots generated for april9_256_40.jsonl
2. 📊 Review the visualization plots
3. 🔍 Analyze tail latency behavior
4. 🎯 Identify optimization opportunities
5. 📈 Compare with other configurations

See **README_LATENCY_PLOTS.md** for detailed documentation.
