# ARCHER2 Wait Time Analysis 2024

This repository contains data, analysis scripts and output from the wait time
analysis that was done as part of experiments on different Slurm fair share 
configuration settings on ARCHER in the first half of 2024.

The three analysis periods correspond to:

- Baseline period: 20 Mar – 3 Apr 2024: baseline measurements with original fair share configuration
- Expt. 1 period: 14 – 28 Apr 2024: experiment 1, 6 hour half-life
- Expt. 2 period: 9 – 22 May 2024: experiment 2, single tier fair share tree

The raw wait time data for these three periods is available in the `data`
directory.

To run the analysis script yourself, from the top level repository directory issue 
the command

```
python3 analysis/WaitTimeAnalysis.py
```

The tables of the wait time distribution will be printed to STDOUT and plots
of the distributions will be produced in the `output` directory.
