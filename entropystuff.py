import math
from collections import Counter
import numpy as np

def calculate_joint_entropy(X, Y):
    # Generate a grid of all possible combinations of X and Y
    X_grid, Y_grid = np.meshgrid(X, Y)
    pairs = np.stack((X_grid.flatten(), Y_grid.flatten()), axis=1)

    # Count the occurrences of each pair
    pair_counts = Counter(map(tuple, pairs))

    # Calculate the total number of pairs
    total_pairs = len(pairs)

    # Calculate the joint probability of each pair
    joint_probabilities = {pair: count / total_pairs for pair, count in pair_counts.items()}

    # Calculate the joint entropy
    joint_entropy = 0
    for probability in joint_probabilities.values():
        joint_entropy -= probability * math.log2(probability)

    return joint_entropy

# Usage
X = np.linspace(0.0, 0.9, num=10, dtype=np.float64)
Y = np.arange(361, dtype=np.int32)

joint_entropy = calculate_joint_entropy(X, Y)
print("Joint Entropy:", joint_entropy)
