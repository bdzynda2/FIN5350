#HW 3 - The first options pricer for American Options
import numpy as np
from scipy.stats import binom

class VanillaOption(object):
    """An abstract interface for plain vanilla options"""

    def __init__(self, strike, expiry):
        self.strike = strike
        self.expiry = expiry

    #def payoff(self, spot):
       # pass

class VanillaCallOption(VanillaOption):
    """A concrete class for vanilla call options"""

    def payoff(self, spot):
        return np.maximum(spot - self.strike, 0.0)

    
class VanillaPutOption(VanillaOption):
    """A concrete class for vanilla put options"""

    def payoff(self, spot):
        return np.maximum(self.strike - spot, 0.0)



def EuropeanBinomialPricer(option, spot, rate, vol, div, steps):
    h = option.expiry / steps
    nodes = steps + 1
    u = np.exp((rate - div) * h + vol * np.sqrt(h))
    d = np.exp((rate - div) * h - vol * np.sqrt(h))

    p = (np.exp((rate - div) * h) - d) / (u - d)
    disc = np.exp(-(rate - div))
    callT = 0.0

    for i in range(nodes):
        spotT = spot * (u ** (steps - i)) * (d ** i)
        callT += option.payoff(spotT) * binom.pmf(steps - i, steps, p)

    price = callT * disc
    return price
 


def AmericanBinomialPricer(option, spot, rate, vol, div, steps):
    h = option.expiry / steps
    nodes = steps + 1
    u = np.exp((rate - div) * h + vol * np.sqrt(h))
    d = np.exp((rate - div) * h - vol * np.sqrt(h))

    p = (np.exp((rate - div) * h) - d) / (u - d)
    St = np.zeros((nodes, nodes))
    callPutT = np.zeros((nodes, nodes))

    for i in range(nodes):
        St[i,steps] = spot * (u ** (steps - i)) * (d ** i)
        
    callPutT[:,[steps]] = option.payoff(St[:,[steps]]) 

    for i in range(steps - 1, -1, -1):
        for j in range(i+1):
            St[j,i] = St[j,i+1] / u
            
    for i in range(steps - 1, -1, -1):
        for j in range(i+1):
            callPutT[j,i] = np.maximum(np.exp(-(rate * h)) * ((p * callPutT[j, i+1]) + ((1 - p) * callPutT[j+1, i+1])), 
                    option.payoff(St[j,i]))
            
           
    
    print("\n The price of the American Option is: $ {0:.6f}".format(callPutT[0,0]))
 