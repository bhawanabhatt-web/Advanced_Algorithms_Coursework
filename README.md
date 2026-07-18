# Advanced Algorithms Coursework (ST5003CEM)

Individual coursework for **ST5003CEM – Advanced Algorithms**, Soffwarica College of IT & E-Commerce, in collaboration with Coventry University (March Intake 2026).

**Author:** Bhawana Kumari Bhatta (Coventry ID: 15938314)
**Module Leader:** Hikmat Saud

This repository contains the full Python implementation, unit tests, benchmarks, and plots for five tasks covering efficient data structures, graph algorithms, algorithmic design strategies, NP-Hard heuristics, and concurrent programming.

---

## Repository Structure

```
.
├── Task1/                  # Efficient Data Structures
│   ├── city.py
│   ├── binary_search_tree.py
│   ├── avl_tree.py
│   ├── hash_table.py
│   ├── min_heap.py
│   ├── benchmark.py
│   ├── main.py
│   └── test_*.py
│
├── Task2/                  # Graph Algorithms and Pathfinding
│   ├── graph.py
│   ├── dijkstra.py
│   ├── prim.py
│   ├── bellman_ford.py
│   ├── main.py
│   └── test_*.py
│
├── Task3/                  # Algorithmic Strategies (DP, Greedy, Backtracking)
│   ├── job_scheduling.py       # Dynamic Programming – Weighted Job Scheduling
│   ├── platform_scheduling.py  # Greedy – Minimum Number of Platforms
│   ├── knights_tour.py         # Backtracking – Knight's Tour (Warnsdorff heuristic)
│   ├── main.py
│   └── test_*.py
│
├── Task4/                  # NP-Hard Problem and Heuristics
│   ├── packing.py              # Multi-dimensional Bin Packing core (Item, Bin, PackingResult)
│   ├── first_fit_decreasing.py
│   ├── local_search.py
│   ├── simulated_annealing.py
│   ├── main.py
│   └── test_*.py
│
├── Task5/                  # Concurrent Programming
│   ├── sequential_bfs.py
│   ├── parallel_bfs.py
│   ├── benchmark.py
│   ├── main.py
│   └── test_*.py
│
├── common/                 # Shared utilities used across tasks
│   ├── generator.py            # Random data generation (with seeding)
│   ├── utils.py                 # Logger, path constants, CSV/Excel export helpers
│   ├── timer.py                 # Benchmarking helper (BenchmarkResult, benchmark())
│   ├── plotting.py              # Bar/line comparison plot helpers
│   └── excel_export.py
│
├── raw_data/                # Exported CSV benchmark results
├── plots/                   # Generated figures (PNG)
├── excel/                   # Exported Excel benchmark workbooks
├── Bhawana_Kumari_Bhatta_240620.pdf   # Full individual report
└── README.md
```

> Folder/file names above reflect the project layout referenced in the report and source code screenshots; see the repository for the exact current structure.

---

## Overview

The coursework is split into five tasks that compare theoretical complexity against measured, real-world performance:

| Task | Topic | Key Techniques |
|------|-------|-----------------|
| 1 | Efficient Data Structures | BST, AVL Tree, Min-Heap, Hash Table (separate chaining) |
| 2 | Graph Algorithms & Pathfinding | Dijkstra, Prim's MST, Bellman-Ford |
| 3 | Algorithmic Strategies | DP (Weighted Job Scheduling), Greedy (Minimum Platforms), Backtracking (Knight's Tour + Warnsdorff heuristic) |
| 4 | NP-Hard Problem & Heuristics | Multi-Dimensional Bin Packing — First-Fit Decreasing, Local Search, Simulated Annealing |
| 5 | Concurrent Programming | Sequential vs. multi-threaded BFS with mutex synchronization |

Each task includes pseudocode, a from-scratch Python implementation, complexity analysis, and benchmark experiments with plotted results.

---

## Key Findings

- **Task 1:** Hash Table gives the fastest average-case lookups; AVL Tree trades slower insertion for consistently balanced (and thus faster) search; BST is simplest but degrades on skewed input; Min-Heap is efficient for priority-based access.
- **Task 2:** Dijkstra and Prim (`O((V+E) log V)`) scale far better than Bellman-Ford (`O(V·E)`), though Bellman-Ford is the only one supporting negative weights and negative-cycle detection.
- **Task 3:** Warnsdorff's heuristic reduces the Knight's Tour search space by several orders of magnitude compared to naive move ordering (e.g., 64 nodes vs. 500,096+ on an 8×8 board).
- **Task 4:** All three bin-packing heuristics reach the same solution quality on large inputs, but Local Search is fastest, followed by Simulated Annealing, with First-Fit Decreasing slowest at scale.
- **Task 5:** Due to Python's Global Interpreter Lock (GIL), multi-threaded BFS does **not** outperform the sequential version for this CPU-bound workload — speedup stayed around 0.32× regardless of thread count.



---

## Requirements

- Python 3.10+
- No external dependencies are required for the core algorithms (standard library only: `dataclasses`, `typing`, `threading`, `unittest`, `bisect`, `math`, `random`)
- Optional, for benchmarking/plotting/export utilities:
  - `matplotlib`
  - `openpyxl` (Excel export)

Install optional dependencies:

```bash
pip install matplotlib openpyxl
```

---

## Getting Started

Clone the repository:

```bash
git clone https://github.com/bhawanabhatt-web/Advanced_Algorithms_Coursework.git
cd Advanced_Algorithms_Coursework
```

### Run a task's demo

Each task folder has a `main.py` entry point that demonstrates the implementation on sample data:

```bash
python Task1/main.py
python Task2/main.py
python Task3/main.py
python Task4/main.py
python Task5/main.py
```

### Run benchmarks

Benchmark scripts regenerate the timing data, CSV exports, and plots used in the report:

```bash
python Task1/benchmark.py
python Task5/benchmark.py
```

Results are written to `raw_data/` (CSV), `excel/` (XLSX), and `plots/` (PNG).

### Run tests

Unit tests are provided per task using `unittest`:

```bash
python -m unittest discover -s Task1
python -m unittest discover -s Task2
python -m unittest discover -s Task3
python -m unittest discover -s Task4
python -m unittest discover -s Task5
```

Or run the full suite from the project root:

```bash
python -m unittest discover
```

---

## License

This repository is submitted as academic coursework for ST5003CEM (Advanced Algorithms) and is intended for educational/reference purposes.
