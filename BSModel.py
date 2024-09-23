import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize_scalar

class BSModel:
    '''
    This class calculates the price and Greeks of a European call/put option using the Black-Scholes formula.

    S0: the current market price of the underlying asset
    K: the strike price of the option
    T: the time to maturity of the option
    r: the risk-free interest rate
    sigma: volatility
    '''

    def __init__(self, S0, K, T, r, sigma):
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    def bs_call(self):
        d1 = (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return self.S0 * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)

    def bs_put(self):
        d1 = (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S0 * norm.cdf(-d1)
    
    def bs_call_delta(self):
        d1 = (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        return norm.cdf(d1)
    
    def bs_put_delta(self):
        d1 = (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        return -norm.cdf(-d1)
    
    def bs_gamma(self):
        d1 = (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        return norm.pdf(d1) / (self.S0 * self.sigma * np.sqrt(self.T))
    
    def bs_call_theta(self):
        d1 = (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return -(self.S0 * norm.pdf(d1) * self.sigma) / (2 * np.sqrt(self.T)) - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2)

    def bs_put_theta(self):
        d1 = (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return -(self.S0 * norm.pdf(d1) * self.sigma) / (2 * np.sqrt(self.T)) + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)

    def bs_vega(self):
        d1 = (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        return self.S0 * norm.pdf(d1) * np.sqrt(self.T) 

    def bs_call_rho(self):
        d1 = (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return self.K * np.exp(-self.r * self.T) * self.T * norm.cdf(d2)
    
    def bs_put_rho(self):
        d1 = (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return -self.K * np.exp(-self.r * self.T) * self.T * norm.cdf(-d2)
    
    def bs_vanna(self):
        d1 = (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return -norm.pdf(d1) * d2 / self.sigma
    
    def bs_volga(self):
        d1 = (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return self.S0 * norm.pdf(d1) * np.sqrt(self.T) * d1 * d2 / self.sigma


class ImpliedVol():
    '''
    This class calculates the BSM implied volatility of a European call/put option using Newton's method.
    '''

    def __init__(self, S0, K, T, r, mkt_price, option_type, initial_vol):
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.mkt_price = mkt_price
        self.option_type = option_type
        self.initial_vol = initial_vol

    def implied_vol(self):
        tol = 1e-8
        max_iter = 1000
        
        d1 = lambda sigma: (np.log(self.S0 / self.K) + (self.r + 0.5 * sigma**2) * self.T) / (sigma * np.sqrt(self.T))
        d2 = lambda sigma: d1(sigma) - sigma * np.sqrt(self.T)

        sigma = self.initial_vol            # initial guess
        
        for i in range(max_iter):
            vega = self.S0 * norm.pdf(d1(sigma)) * np.sqrt(self.T)

            if self.option_type == 'Call':
                C = self.mkt_price - (self.S0 * norm.cdf(d1(sigma)) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2(sigma)))
            else:
                C = self.mkt_price - (self.K * np.exp(-self.r * self.T) * norm.cdf(-d2(sigma)) - self.S0 * norm.cdf(-d1(sigma)))

            sigma_new = sigma + C / vega
            sigma = sigma_new

            if self.option_type == 'Call':
                C_new = self.mkt_price - (self.S0 * norm.cdf(d1(sigma_new)) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2(sigma_new)))
            else:
                C_new = self.mkt_price - (self.K * np.exp(-self.r * self.T) * norm.cdf(-d2(sigma_new)) - self.S0 * norm.cdf(-d1(sigma_new)))

            if abs(C_new) < tol or abs(sigma - sigma_new) < tol:
                break
        
        return sigma_new
    









