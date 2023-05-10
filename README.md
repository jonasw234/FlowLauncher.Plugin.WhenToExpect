# Overview
A plugin for calculating the expected number of trials before an event occurs given a probability (or odds) and confidence level in [Flow Launcher](https://www.flowlauncher.com/).

The expected number of trials is calculated using the formula: $log(1 - c) / log(1 - p)$, where $p$ is the probability of the event occurring and `c` is the desired confidence level. If $c$ is not specified, it defaults to 0.5.

The query should be in the form `p [c]`, where `p` is the probability (or odds) of the event occurring and `c` is the desired confidence level (expressed as a fraction; defaults to 0.5 if not specified).  
For example, `1/6 0.95` would calculate the expected number of dice rolls needed to get a specific number at least once with 95 % confidence.

`p` can be given as probability (`0.n`/`n/m`) or odds (`n:m`).

# Credits
- [Icon by Muhammad Atif - Flaticon](https://www.flaticon.com/free-icon/ideas_9322526?term=expect&page=1&position=66&origin=search&related_id=9322526)
