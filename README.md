![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# Horton Infiltration Calculator
 
*For soil scientists and hydrologists: enter Horton infiltration parameters and a time range to instantly compute infiltration rate and cumulative infiltration with a plot.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Soil Science
 
Inputs: (1) initial infiltration rate (f₀, mm/hr, numeric input), (2) steady infiltration rate (f_c, mm/hr, numeric input), (3) decay constant (k, 1/hr, numeric input), (4) time range start (t_start, hours, numeric), (5) time range end (t_end, hours, numeric), (6) time step (Δt, hours, numeric, default 0.1). Core calculation uses Horton's equation: infiltration rate f(t) = f_c + (f₀ - f_c) * exp(-k * t). Cumulative infiltration F(t) = f_c * t + (f₀ - f_c)/k * (1 - exp(-k*t)). The tool generates a time vector from t_start to t_end at Δt increments, then computes f(t) and F(t) for each step. Gradio UI: a clean layout with inputs in a row at the top, a 'Compute' button, and two output areas: (a) a data table with columns t (hr), f(t) (mm/hr), F(t) (mm), sorted and scrollable; (b) a matplotlib dual-axis plot with time on x-axis, left y-axis for f(t) (line, blue), right y-axis for F(t) (line, green). The plot includes a horizontal dashed line at f_c for reference. Below the plot, a summary box shows total infiltration (final F(t_end) value) and time to reach near-steady state (when f(t) is within 5% of f_c). No AI/ML component; purely deterministic calculation. Download button for table as CSV.
 
## Run it
 
```bash
docker build -t horton-infiltration-calculator .
docker run -p 7860:7860 horton-infiltration-calculator
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-09-29.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
