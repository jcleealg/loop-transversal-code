# Loop Transversal Code Project

This repository provides tools for constructing and presenting syndrome maps in greedy loop transversal codes, as part of the Master's thesis "Loop Transversal Code".

## Project Overview
Traditional error-correcting codes are designed first, then analyzed to determine which errors they can correct. In contrast, the Loop Transversal Code method starts with a list of errors you want to fix, and uses a greedy algorithm to build a custom code tailored to that list. This project demonstrates the greedy construction process and provides CLI tools for exploring syndrome mappings and parity check matrices.

## Reference
This project is based on the following Master's thesis:
- [Loop Transversal Code (NCKU Thesis Library)](https://thesis.lib.ncku.edu.tw/thesis/detail/4759066580a6172d56505500348dae66/)

## Main Features
- `full-syndrome-mapping`: Display syndrome mappings for all error patterns.
- `basis-mapping`: Display syndrome mappings for basis vectors.
- `parity-check-matrix`: Output the parity check matrix.
- `all-mapping`: Run all three features in sequence.

## File Structure
- `main.py`: Typer-based CLI for syndrome mapping and parity check matrix generation.
- `greedy_syndrome_mapper.py`: Core greedy algorithm implementation.
- `tests/`: Pytest test cases for main features.
- `archive/GLTC_presentation.py`: Demo script for parity-check matrix construction (archived draft).
- `archive/tools.py`: Early prototype of the greedy algorithm (archived, for reference only).

## Installation
Install all required dependencies:
```bash
pip install -r requirements.txt
```

## Example Usage
```powershell
# Example 1: Simple basis
python main.py all-mapping --error-patterns "[[1,0,0],[0,1,0],[0,0,1]]"

# Example 2: Custom error patterns
python main.py all-mapping --error-patterns "[[0,0,0,0,0,1],[0,0,0,0,1,0],[0,0,0,0,1,1],[0,0,0,1,0,0],[0,0,0,1,1,0],[0,0,1,0,0,0],[0,0,1,1,0,0],[0,1,0,0,0,0],[0,1,1,0,0,0],[1,0,0,0,0,0],[1,1,0,0,0,0]]"

# Example 3: Standard basis
python main.py parity-check-matrix --standard-basis 3
```

## How to Test

To run all tests and verify the core logic, use:
```bash
pytest
```
This will automatically discover and execute all test cases in the `tests/` folder. Make sure all dependencies are installed before running tests.

## Typer CLI Autocompletion

This CLI supports command and option autocompletion for a smoother user experience.

**Install autocompletion** (run once):
```powershell
python main.py --install-completion
```
After running, follow the instructions to add the output to your shell profile (PowerShell, bash, zsh, etc.).

**Show autocompletion script**:
```powershell
python main.py --show-completion
```
Use this to manually copy or customize the installation.

Once installed, you can use the tab key to autocomplete commands and options when typing `python main.py` in your terminal.

## Archive

The `archive/` folder contains early drafts and prototype scripts from the initial development phase. These files are preserved for reference and historical context, but are not maintained or recommended for direct use.

---
