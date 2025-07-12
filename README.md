# LTC_presentation_tools
Tools for presenting syndrome maps in greedy loop traversal codes.

## About This Project
This repository contains the code implementation for the Master's thesis, "Loop Transversal Code".

* **Traditional Method**: Design an error-correcting "code" first, then analyze what errors it can fix.
* **Loop Transversal Code Method**: This method does the reverse. It starts with a "list of errors" you want to fix, and then uses an algorithm to build a custom code for that list. This project implements the "Greedy construction" algorithm to demonstrate the process.

## Files
* **`GLTC_presentation.py`**: Run this file to see the demo.
* **`tools.py`**: Contains the core greedy algorithm code.

## How to Run
1.  **Install numpy:**
    ```bash
    pip install numpy
    ```

2.  **Run the main script:**
    ```bash
    python GLTC_presentation.py
    ```
    The script will print the parity-check matrix constructed from the error list `T_given_1`.
