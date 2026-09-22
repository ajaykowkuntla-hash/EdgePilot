import json
import os

def load_json(filepath):
    """Loads a JSON file and returns the dictionary. Returns empty dict if not found."""
    if not os.path.exists(filepath):
        return {}
    with open(filepath, 'r') as f:
        return json.load(f)

def get_comparison_metrics():
    """Loads the comparison benchmark json."""
    return load_json("phase3/benchmark/comparison.json")

def get_phase0_metrics():
    """Loads the phase 0 benchmark json."""
    return load_json("phase0/benchmark.json")

def get_phase3_custom_metrics():
    """Loads the phase 3 custom benchmark json."""
    return load_json("phase3/benchmark/custom_benchmark.json")
