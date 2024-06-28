#classic BS
import numpy as np
from scipy.stats import norm

def calculate_pure_bond_value(coupon_rate, maturity, discount_rate, payments_per_year=1):
    """
    计算纯债价值
    coupon_rate: 票息率（年化）
    maturity: 到期时间（以年为单位）
    discount_rate: 折现率（年化）
    payments_per_year: 每年的票息支付次数，默认为1（年付）
    """
    coupon_payment=100
    for i in coupon_rate:
        coupon_payment*=(1+i)
    discount_factor = 1 + discount_rate / payments_per_year
    
    pure_bond_value=coupon_payment/(discount_factor**maturity)
    return pure_bond_value


def black_scholes_call(S, K, T, r, sigma):
    """
    计算欧式看涨期权的 Black-Scholes 价格
    S: 标的资产现价
    K: 期权行权价
    T: 期权到期时间（以年为单位）
    r: 无风险利率
    sigma: 标的资产的波动率
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

def conversion_option_value(S, K, T, r, sigma):
    return black_scholes_call(S, K, T, r, sigma)

#回售条款可以被视为一个欧式看跌期权，其行权价为回售价格。
def black_scholes_put(S, K, T, r, sigma):
    """
    计算欧式看跌期权的 Black-Scholes 价格
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return put_price

def put_option_value(S, K, T, r, sigma):
    return black_scholes_put(S, K, T, r, sigma)

#赎回条款可以被视为一个欧式看涨期权，其行权价为赎回价格。
def call_option_value(S, K, T, r, sigma):
    return black_scholes_call(S, K, T, r, sigma)

S = 8.27  # 股票现价
K_conversion = 12.4  # 转股价
K_put = 8.67  # 回售价格
K_call = 16.15  # 赎回价格
T = 2.4  # 到期时间（年)
r = 0.025  # 无风险利率
sigma = 0.3  # 波动率
coupon_rate=[0.003,0.005,0.01,0.015,0.018,0.02]#票息率
discount_rate=0.03#折现率

conversion_value = conversion_option_value(S, K_conversion, T, r, sigma)
put_value = put_option_value(S, K_put, T, r, sigma)
call_value = call_option_value(S, K_call, T, r, sigma)
pure_bond_value=calculate_pure_bond_value(coupon_rate,T,discount_rate)

print(f"转股权价值: {conversion_value:.2f}")
print(f"回售条款价值: {put_value:.2f}")
print(f"赎回条款价值: {call_value:.2f}")
print(f'纯债价值{pure_bond_value:.2f}')
print(f"BS估值: {conversion_value + put_value + call_value+pure_bond_value:.2f}")
