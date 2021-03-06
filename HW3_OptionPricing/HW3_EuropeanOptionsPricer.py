#HW 3 - The first options pricer for American Options
import numpy as np
from scipy.stats import binom

class VanillaOption(object):
    """An abstract interface for plain vanilla options"""

    def __init__(self, strike, expiry):
        self.strike = strike
        self.expiry = expiry

    def payoff(self, spot):
        pass

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
            
