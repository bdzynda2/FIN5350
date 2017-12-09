# -*- coding: utf-8 -*-
"""
European Down and Out

Number of steps must be power of 2 (8,16,32, 256, etc)

generate Strata epsilon,
put in weiner 
calculate path forward
while checking for barrier cross

for each rep in j get a path
within time loop build out stock price

for j in range (M)
  get weiner bridge - path[k] = path[k-1] x np.exp(nudt + sgdt *)
  steps
  for k in range (n)
    get price path
    check for barrier crossing
  
  ct[j] = callPayoff(price path[-1], k) #average and discsount this
  
Co = ct.mean() * exp(-r*T)

"""

import numpy as np
import time
import random
from scipy.stats import norm
from math import log2

#norm.ppf
#random.uniform


def WienerBridge(expiry, num_steps, endval = 0.0):
    num_bisect = int(log2(num_steps))
    tjump = int(expiry)
    ijump = int(num_steps - 1)

    if endval == 0.0:
        endval = np.random.normal(scale = np.sqrt(expiry), size=1)

    z = np.random.normal(size=num_steps + 1)
    w = np.zeros(num_steps + 1)
    w[num_steps] = endval
    

    for k in range(num_bisect):
        left = 0
        i = ijump // 2 + 1    ## make sure this is integer division!
        right = ijump + 1
        limit = 2 ** k

        for j in range(limit):
            a = 0.5 * (w[left] + w[right])
            b = 0.5 * np.sqrt(tjump)
            w[i] = a + b * z[i]
            right += ijump + 1
            left += ijump + 1
            i += ijump + 1
        
        ijump //= 2    ## Again, make this is integer division!
        tjump /= 2

    return np.diff(w)  ## Recall the the Brownian motion is the first difference of the Wiener process

## main



K = 100
T = 1
S = 100
sig = 0.2
r = .06
div = .03
H = 99
N = 8
M = 10000

dt = T/N
nudt = (r - div - 0.5 * (sig**2)) * dt
nu = (r - div - 0.5 * (sig**2))
sigsdt = (sig * np.sqrt(dt))

St = np.zeros(N)
St[0] = S


sum_CT = 0
sum_CT2 = 0


'''
1) Draw from a uniform distn
2) Implement antithetic on uniform
3) Draw from normal 
'''

zeros = 0


t1 = time.time()


for i in range(M):
  
    
    unif = random.uniform(0,1)
    #unif = np.array([unif1, 1-unif1])
    
    epsilon = norm.ppf(unif)
    
    #St = St * np.exp(nu * T + sig*np.sqrt(T) * epsilon)
    
    Barrier_Crossed = False
    
  
     # N = num_steps Don't use ST, use epsilon
     # Second does not work properly
     
    z = WienerBridge(T, N, epsilon)
    
    for j in range(1,(N)):
      St[j] = St[j-1] * np.exp(nudt + sigsdt * z[j])
      if(St[j] < H):
        St[j] = 0
    
    
    Price = St[-1]
    if(Price == 0):
      zeros += 1
    
    CT = np.maximum(0, Price - K)
    sum_CT = sum_CT + CT
    sum_CT2 = sum_CT2 + CT*CT
    

print("the number going below H is :", zeros)
  
t2 = time.time()
call_value = sum_CT/ M * np.exp(-r * T)
SD = np.sqrt((sum_CT2 - sum_CT * sum_CT / M) * np.exp(-2 * r * T) / (M - 1))
SE = SD / np.sqrt(M)


print(call_value)
print(SE)
print("Time: ", t2 - t1)
  