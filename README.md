# Control Systems Lab
# Control Systems Lab

A collection of Python tools and utilities for Industrial Control Systems (ICS), SCADA, Data Centers, and Ignition development.

Created by Sara Mirbagheri

---

## Overview

This repository contains engineering tools developed for:

- Ignition SCADA development
- UDT version control
- JSON configuration comparison
- Source code comparison
- Data center automation
- Power monitoring projects
- Engineering productivity utilities

The goal is to simplify troubleshooting, version tracking, and configuration management in industrial and mission-critical environments.

---

## Repository Structure

├── Ignition_Version_Control/
│
├── EAM_UDT_Definitions_20260605/
│   Exported Ignition UDT definitions
│
├── IAD2_DC2_UDT_Definitions_20260605/
│   Exported Ignition UDT definitions
│
├── compare_folders.py
│   Compare two folders and report differences
│
├── compare_one_json_visual.py
│   Visual JSON comparison tool
│
├── clean_json_difference.html
│   HTML report showing JSON differences
│
├── json_difference_highlight.html
│   Highlighted JSON comparison report
│
├── smarter_json_difference.html
│   Enhanced JSON comparison report
│
└── folder_comparison.xlsx
    Example comparison output

---

## Features

### Folder Comparison

Compare two folders and identify:

- Missing files
- Added files
- Modified files

Output can be exported to Excel.

---

### JSON Comparison

Compare Ignition exported JSON files and identify:

- Added tags
- Removed tags
- Changed properties
- Modified UDT definitions

Results can be displayed in HTML for easier review.

---

### Ignition Version Control

Track changes between Ignition exports to:

- Audit modifications
- Review engineering changes
- Support commissioning activities
- Assist troubleshooting

---

## Why This Repository Matters

In SCADA and industrial control systems, small configuration changes can create major operational problems. This repository helps track engineering changes, compare exported files, and make version differences easier to review.

## Technologies Used

- Python
- Git
- GitHub
- Ignition SCADA exports
- JSON
- Excel reports
- HTML reports

## How to Clone This Repository

```bash
git clone https://github.com/shararehmirbagheri/control-systems-lab.git