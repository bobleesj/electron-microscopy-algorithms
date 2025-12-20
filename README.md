# Electron Microscopy Algorithms

Optimized Python code for electron microscopy.

## Principles

- Each notebook should be self-contained so that it can be passed between emails and Slack
- Only use for-loop for sequential tasks
- Don't import uncommon Python packages (e.g., `bobleesj.widget`)
- Use Pytorch for all computation if possible so that GPU can be easily accessed

## Scope

- Calculus
- Physics
- Crystallography
- Memory optimization
- Algorithms

## Tutorial writing guide

### Structure

Each tutorial notebook should follow this structure (results first, tutorials in appendix):

```
1. Problem/Solution  → What's slow, what's fast, why
2. Setup             → Test data configuration
3. Method 1          → Slow baseline (just the function)
4. Method 2          → Fast solution (just the function)
5. Benchmark         → Timing + correctness check
6. Appendix          → Step-by-step tutorial with visuals
```

**Key principle**: Readers want quick results first. Put the working code and benchmarks up front, detailed explanations in appendix.

### Section Details

#### 1. Problem/Solution (intro cell)
- State the problem in 2-3 sentences with ASCII diagram
- Why is the naive approach slow?
- What's the solution? (one sentence)
- Include comparison table

#### 2. Setup
- Configuration constants
- Create test data
- Print shapes

#### 3-4. Method 1 & 2
- Just the function definitions
- Minimal code, no explanations
- Comments inside code only

#### 5. Benchmark
- Verify correctness: `assert torch.allclose(...)`
- Timing comparison
- Print speedup

#### 6. Appendix
- How the algorithm works (for those who want to learn)
- ASCII diagrams

### Naming Convention

```
YYYYMMDD_topic_subtopic.ipynb
```

Examples:
- `20251217_patching_unfold.ipynb`
- `20251220_patching_gather_channel.ipynb`

### Code Style

- **No extra blank lines**: No blank lines within functions or between related statements
- **CAPITALIZED constants**: Use `NUM_STATES`, `BATCH_SIZE`, `OBJ_HEIGHT`, not lowercase
- **Prefer ASCII diagrams over text**: Visualize tensor operations instead of explaining them
- **Sentence case for headers**: Only capitalize the first letter (e.g., "Step 1: Extract patches" not "Step 1: Extract Patches")
- **No horizontal rules**: Don't use `---` separators in markdown cells
- Use descriptive variable names
- Print tensor shapes after operations
- Include `# comments` explaining non-obvious steps
- Prefer `view` over `reshape` when possible (zero-copy)
- Use this device detection pattern (CUDA → XPU → MPS → CPU):

```python
def get_device():
    """Get the best available device: CUDA → XPU → MPS → CPU."""
    if torch.cuda.is_available():
        return torch.device('cuda')
    if hasattr(torch, 'xpu') and torch.xpu.is_available():
        return torch.device('xpu')
    if torch.backends.mps.is_available():
        return torch.device('mps')
    return torch.device('cpu')

device = get_device()
```

## Validating Notebooks

Use `check_notebooks.py` to run all notebooks and verify no errors:

```bash
# Run all notebooks (clears outputs, executes all cells, saves results)
python check_notebooks.py

# Run a specific notebook
python check_notebooks.py 20251217_patching_unfold.ipynb

# Quick check: only inspect saved outputs (no execution)
python check_notebooks.py --check
```

The script will:
1. Execute each notebook from scratch
2. Report any cells that raise exceptions
3. Save the notebook with fresh outputs

## Questions?

If any part of the tutorials is confusing or you need help with optimization for your scientific project, please reach out to [@bobleesj](https://github.com/bobleesj). I'm happy to provide feedback.
