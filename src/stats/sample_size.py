import math
from scipy.stats import norm

# Sample Size (per group)
def sample_size_proportion(p, delta, alpha=0.05, power=0.8):
    """
    Calculate sample size for two-proportion test
    
    Where:
    p       : baseline conversion rate
    delta   : absolute expected effect
    alpha   : significance level
    power   : statistical power
    """

    var = p * (1 - p)

    n = 2 * (z_alpha(alpha) + z_beta(power))**2 * var / (delta**2)

    return math.ceil(n)

# Test duration (days)
def estimate_experiment_duration(n, daily_users):
    return math.ceil(n / daily_users)


# Z-scores
def z_alpha(alpha):
    return norm.ppf(1 - alpha/2)

def z_beta(power):
    return norm.ppf(power)
   