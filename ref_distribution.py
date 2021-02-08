
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pylab as plt

a = np.array([[1,2,3], [4,5,6]])

# stats.distribution.rvs: generates random numbers from the specified distribution
uniform_data = stats.uniform.rvs(size=100000, loc=0, scale=10)
pd.DataFrame(uniform_data).plot(kind="density",
                                figsize=(9,9),
                                xlim=(-1,11))

# stats.distribution.cdf()은 분포로부터 특정한 값으로 떨어지는 관측치에 대한 확률을 보는데 사용된다.
stats.uniform.cdf(x=2.5,
                  loc=0,
                  scale=10)

# stats.distribution.ppf()는 주어진 확률에 대한 x축의 cutoff value를 반환한다.(cdf의 역임)
stats.uniform.ppf(q=0.4,
                  loc=0,
                  scale=10)

# stats.distribution.pdf()는 pdf의 height를 반환한다.
for x in range(-1, 12, 3):
    print("Density at x value: " + str(x))
    print(stats.uniform.pdf(x, loc=0, scale=10))

# random libary는 다양한 random 관련 함수를 제공한다.
import random
random.randint(0, 10) # Get a random integer in the specified range
random.choice([2,4,6,9]) # Get a random element from a sequence
random.random() # Get a real number between 0 and 1
random.uniform(0, 10) # Get a real in the specified range

# reproducible한 random 값 만들기
random.seed(12) # Set the seed to an arbitrary value
print([random.uniform(0, 10) for i in range(4)])

# Normal distribution
stats.norm.ppf(q= 0.025) # Find quantile for the 2.5% cutoff
stats.norm.cdf(x=-3) # Find how much data is below = -3

# Binomial distribution
fair_coin_flip = stats.binom.rvs(n=10, # Number of flips per trial
                                 p=0.5, # Success probability
                                 size=10000) # Number of trials
pd.crosstab(index="counts", columns=fair_coin_flip)
pd.DataFrame(fair_coin_flip).hist(range=(-0.5, 10.5), bins=11)

biased_coin_flips = stats.binom.rvs(n=10,
                                    p=0.8,
                                    size=10000)
pd.crosstab(index="counts", columns= biased_coin_flips)
pd.DataFrame(biased_coin_flips).hist(range=(-0.5, 10.5), bins=11)

stats.binom.cdf(k=5, # Probability of k = 5 successes or less
            n=10, # With 10 flips
            p=0.8) # And Success probability 0.8

1 - stats.binom.cdf(k=8,
                    n=10,
                    p=0.8)

# 확률 질량함수의 경우 확률 밀도함수의 높이를 알기 위해 pmf 라는 함수를 사용
stats.binom.pmf(k=5, # Probability of k=5 success
                n=10, # With 10 flips
                p=0.5) # And Success probability 0.5

# Geometric and Exponential Distributions
random.seed(12)
flips_till_heads = stats.geom.rvs(size=10000,
                                  p=0.5)
pd.crosstab(index="counts", columns=flips_till_heads)
pd.DataFrame(flips_till_heads).hist(range=(-0.5, max(flips_till_heads) + 0.5),
                                    bins=max(flips_till_heads) + 1)

first_five = stats.geom.cdf(k=5,
                            p=0.5)
1 - first_five

stats.geom.pmf(k=2,
               p=0.5)





