# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 18:19:27 2017

@author: Student
"""
import numpy as np
import time
import random
from scipy.stats import norm
from math import log2

class Option(object):
    """An abstract interface for plain vanilla options"""

    def __init__(self, strike, expiry):
        self.strike = strike
        self.expiry = expiry

    def payoff(self, spot):
        pass

class CallOption(Option):
    """A concrete class for vanilla call options"""

    def payoff(self, spot):
        return np.maximum(spot - self.strike, 0.0)

    
class PutOption(Option):
    """A concrete class for vanilla put options"""

    def payoff(self, spot):
        return np.maximum(self.strike - spot, 0.0)


class MarketData(object):
    
    def __init__(self, spot, rate, vol, div):
        self.spot = spot
        self.rate = rate
        self.vol = vol
        self.div = div

def WienerBridge(expiry, num_steps, endval):
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

    
class Euro_Down_Out_Barrier(object):
    
    def __init__(self, option, data, barrier, steps = 8, simulations = 1000):
        self.barrier = barrier
        self.steps = steps
        self.simulations = simulations
        self.spot = data.spot
        self.expiry = option.expiry
        self.strike = option.strike
        self.dt = option.expiry / steps
        self.nudt = (data.rate - data.div - 0.5 * (data.vol ** 2)) * self.dt
        self.nu = (data.rate - data.div - 0.5)
        self.sigsdt = (data.vol * np.sqrt(self.dt))
        self.rate = data.rate
        self.St = np.zeros(self.steps)
        self.St[0] = self.spot 
    
        self.sum_CT = 0
        self.sum_CT2 = 0
        
        
        
    def StratifiedMC(self):
        
        for i in range(self.simulations):
            
            unif = random.uniform(0,1)
            epsilon = norm.ppf(unif)
            
            z = WienerBridge(self.expiry, self.steps, epsilon)
            
            for j in range(1,(self.steps)):
                self.St[j] = self.St[j-1] * np.exp(self.nudt + self.sigsdt * z[j])
                if(self.St[j] < self.barrier):
                    self.St[j] = 0
                    
            Price = self.St[-1]        
                    
            CT = np.maximum(0, Price - self.strike)
            self.sum_CT = self.sum_CT + CT
            self.sum_CT2 = self.sum_CT2 + CT*CT
                        
        self.value = self.sum_CT/ self.simulations * np.exp(-self.rate * self.expiry)
        self.SD = np.sqrt((self.sum_CT2 - self.sum_CT * self.sum_CT / self.simulations) * np.exp(-2 * self.rate * self.expiry) / (self.simulations - 1))
        self.SE = self.SD / np.sqrt(self.simulations)
        
        return(self.value, self.SE)
        
        
        
call = CallOption(100, 1)

data = MarketData(100, 0.06, 0.2, 0.03) 
                    
priceIt = Euro_Down_Out_Barrier(call, data, barrier = 99, steps = 256, simulations = 100000)                  
                    
t1 = time.time()  
                  
priceIt.StratifiedMC()   
                 
t2 = time.time()  
print("The Price is: $", priceIt.value)         
print("The stardard error is: $", priceIt.SE)         
print("Time: ", t2 - t1)                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
    
    

        
        
    