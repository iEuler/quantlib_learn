"""
For equity option, including vanilla option, knocked in option, Black-Scholes process, Heston process
"""

import QuantLib as ql

today = ql.Date(23, ql.September, 2020)
ql.Settings.instance().evaluationDate = today

option = ql.EuropeanOption(ql.PlainVanillaPayoff(ql.Option.Call, 100.0),
                           ql.EuropeanExercise(ql.Date(23, ql.December, 2020)))

u = ql.SimpleQuote(100.0)
r = ql.SimpleQuote(0.01)
sigma = ql.SimpleQuote(0.20)

riskFreeCurve = ql.FlatForward(0, ql.TARGET(), ql.QuoteHandle(r), ql.Actual360())
volatility = ql.BlackConstantVol(0, ql.TARGET(), ql.QuoteHandle(sigma), ql.Actual360())

process = ql.BlackScholesProcess(ql.QuoteHandle(u), ql.YieldTermStructureHandle(riskFreeCurve),
                                 ql.BlackVolTermStructureHandle(volatility))

engine = ql.AnalyticEuropeanEngine(process)

option.setPricingEngine(engine)

print(option.NPV())
print(option.delta())
print(option.gamma())
print(option.vega())

u.setValue(105.0)
print(option.NPV())

engine = ql.MCEuropeanEngine(process, "PseudoRandom", timeSteps=20, requiredSamples=250000)
option.setPricingEngine(engine)
print(option.NPV())

# from ipywidgets import interact
#
# @interact
# def show_off(underlying=(80, 120, .5),
#              rate=(0, .05, .001),
#              volatility=(0, .3, .01)):
#     u.setValue(underlying)
#     r.setValue(rate)
#     sigma.setValue(volatility)
#
#     print('-----')
#     print(f"value = {option.NPV(): .2f}")
#     print(f"delta = {option.delta(): .2f}")
#     print(f"gamma = {option.gamma(): .2f}")
#     print(f"vega = {option.vega(): .2f}")

# Heston model
process_Heston = ql.HestonProcess(ql.YieldTermStructureHandle(riskFreeCurve),
                                  ql.YieldTermStructureHandle(ql.FlatForward(0, ql.TARGET(), 0, ql.Actual360())),
                                  ql.QuoteHandle(u),
                                  0.04, 0.1, .01, .05, -.75)
model = ql.HestonModel(process_Heston)
engine = ql.AnalyticHestonEngine(model)
option.setPricingEngine(engine)
print(option.NPV())

# knock-in barrier option

option = ql.BarrierOption(ql.Barrier.UpIn, 120, 0, ql.PlainVanillaPayoff(ql.Option.Call, 100),
                          ql.EuropeanExercise(ql.Date(23, ql.December, 2020)))
option.setPricingEngine(ql.AnalyticBarrierEngine(process))
print(option.NPV())

# delta not defined, use a bump-and-reval for numerical calculation
# print(option.delta())
