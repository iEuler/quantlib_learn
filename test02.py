"""
For bond
"""
import QuantLib as ql

schedule = ql.Schedule(ql.Date(8, ql.February, 2017),
                       ql.Date(8, ql.February, 2027),
                       ql.Period(6, ql.Months),
                       ql.TARGET(),
                       ql.Following,
                       ql.Following,
                       ql.DateGeneration.Backward,
                       False)

settlementDays = 3
faceAmount = 100
coupons = [0.02]
paymentDayCounter = ql.Thirty360()

bond = ql.FixedRateBond(settlementDays, faceAmount, schedule, coupons, paymentDayCounter)

y = ql.SimpleQuote(0.02)
yield_curve = ql.FlatForward(bond.settlementDate(), ql.QuoteHandle(y),
                             ql.Actual360(), ql.Compounded, ql.Semiannual)
bond.setPricingEngine(ql.DiscountingBondEngine(ql.YieldTermStructureHandle(yield_curve)))

P = bond.dirtyPrice()
h = 0.0001
y0 = y.value()
y.setValue(y0+h)
P_plus = bond.dirtyPrice()
y.setValue(y0-h)
P_minus = bond.dirtyPrice()
duration = - (P_plus - P_minus) / P / h / 2
print(f'Price = {P}, duration = {duration}')
Y = ql.InterestRate(y0, ql.Actual360(), ql.Compounded, ql.Semiannual)
print(ql.BondFunctions.duration(bond, Y, ql.Duration.Modified))