# Euro 2024 Final — Centre-Back Passing Analysis

## Project context

This report analyses the centre-backs who participated in the Euro 2024 final between Spain and England.

The analysis is based on StatsBomb Open Data and focuses on passing behaviour:

- pass volume;
- pass completion;
- forward passing;
- long passing;
- average pass length;
- pass density heatmaps;
- pass maps.

## Match context

| Field | Value |
|---|---|
| Competition | UEFA Euro |
| Season | 2024 |
| Match | Spain 2 - 1 England |
| Date | 2024-07-14 |
| Data source | StatsBomb Open Data |
| Event type | Pass |
| Population | Centre-backs |

## Comparison table

The table below excludes players with very low passing volume in order to avoid misleading interpretation from very small samples.

| Player | Team | Position | Total passes | Completed passes | Incomplete passes | Completion rate (%) | Forward passes | Forward pass share (%) | Long passes | Long pass share (%) | Average pass length |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Robin Aime Robert Le Normand | Spain | Right Center Back | 84 | 80 | 4 | 95.2 | 65 | 77.4 | 11 | 13.1 | 21.9 |
| Aymeric Laporte | Spain | Left Center Back | 83 | 80 | 3 | 96.4 | 50 | 60.2 | 19 | 22.9 | 22.3 |
| John Stones | England | Right Center Back | 35 | 30 | 5 | 85.7 | 23 | 65.7 | 11 | 31.4 | 27.7 |
| Marc Guehi | England | Left Center Back | 26 | 23 | 3 | 88.5 | 17 | 65.4 | 4 | 15.4 | 18.9 |

## Automatic profile summary

- **Most involved in possession**: Robin Aime Robert Le Normand (Spain) — 84.0 `total_passes`
- **Best pass completion rate**: Aymeric Laporte (Spain) — 96.4 `completion_rate_pct`
- **Highest forward pass share**: Robin Aime Robert Le Normand (Spain) — 77.4 `forward_pass_share_pct`
- **Highest long pass share**: John Stones (England) — 31.4 `long_pass_share_pct`
- **Longest average pass length**: John Stones (England) — 27.7 `average_pass_length`

## Comparison charts

### Total passes

![Total passes](../comparison_charts/total_passes_comparison.png)

### Completion rate

![Completion rate](../comparison_charts/completion_rate_comparison.png)

### Forward pass share

![Forward pass share](../comparison_charts/forward_pass_share_comparison.png)

### Long pass share

![Long pass share](../comparison_charts/long_pass_share_comparison.png)

### Average pass length

![Average pass length](../comparison_charts/average_pass_length_comparison.png)

## Player visualisations

### Aymeric Laporte

**Pass density heatmap**

![Aymeric Laporte pass density heatmap](../heatmaps/aymeric_laporte_pass_density_heatmap.png)

**Pass map**

![Aymeric Laporte pass map](../passmaps/aymeric_laporte_pass_map.png)

---

### John Stones

**Pass density heatmap**

![John Stones pass density heatmap](../heatmaps/john_stones_pass_density_heatmap.png)

**Pass map**

![John Stones pass map](../passmaps/john_stones_pass_map.png)

---

### Jose Ignacio Fernandez Iglesias

**Pass density heatmap**

![Jose Ignacio Fernandez Iglesias pass density heatmap](../heatmaps/jose_ignacio_fernandez_iglesias_pass_density_heatmap.png)

**Pass map**

![Jose Ignacio Fernandez Iglesias pass map](../passmaps/jose_ignacio_fernandez_iglesias_pass_map.png)

---

### Marc Guehi

**Pass density heatmap**

![Marc Guehi pass density heatmap](../heatmaps/marc_guehi_pass_density_heatmap.png)

**Pass map**

![Marc Guehi pass map](../passmaps/marc_guehi_pass_map.png)

---

### Robin Aime Robert Le Normand

**Pass density heatmap**

![Robin Aime Robert Le Normand pass density heatmap](../heatmaps/robin_aime_robert_le_normand_pass_density_heatmap.png)

**Pass map**

![Robin Aime Robert Le Normand pass map](../passmaps/robin_aime_robert_le_normand_pass_map.png)

## Methodological notes

- A completed pass is identified when `pass_outcome` is missing in StatsBomb event data.
- A forward pass is approximated with `end_x > x`.
- A long pass is defined with `pass_length >= 30`.
- The comparison is based on a single match and should not be interpreted as a full player profile across a season.
