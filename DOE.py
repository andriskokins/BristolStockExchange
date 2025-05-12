from pyDOE import lhs
import numpy as np

# Parameters
n_agents = 5
n_levels = 4
n_samples = 10  # Decide how many experiments you want

# LHS sampling
lhs_samples = lhs(n_agents, samples=n_samples, criterion='maximin')

# Map to levels [5, 15, 50, 100]
levels = np.array([5, 15, 50, 100])
experiment_matrix = levels[(lhs_samples * n_levels).astype(int)]

print(experiment_matrix)