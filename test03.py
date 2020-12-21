"""
implied term structures
https://www.youtube.com/watch?v=8Lc5r0YxAME&list=PLu_PrO8j6XAvOAlZND9WUPwTHY_GYhJVr&index=3&ab_channel=LuigiBallabio
"""

import QuantLib as ql
import pandas as pd
from datetime import date

today = ql.Date(23, ql.September, 2020)
ql.Settings.instance().evaluationDate = today


def to_datetime(d):
    return date(d.year(), d.month(), d.dayOfMonth())


def format_rate(r):
    return '%.4f %%' % (r.rate()*100.0)


from matplotlib.dates import MonthLocator, DateFormatter
import matplotlib.pyplot as plt
def plot_curve(*curves):
    fig, ax = plt.subplots()
    plt.rc('lines', linewidth=4)
    # ax.set_color_cycle(['b', 'y', 'b', 'k'])
    dates = [today+ql.Period(i, ql.Weeks) for i in range(52*5)]
    for c in curves:
        valid_dates = [d for d in dates if d >= c.referenceDate()]
        rates = [c.forwardRate(d, d+1, ql.Actual360(), ql.Simple).rate() for d in valid_dates]
        ax.plot_date([to_datetime(d) for d in valid_dates], rates, '-')
    ax.set_xlim(to_datetime(min(dates)), to_datetime(max(dates)))
    ax.xaxis.set_major_locator(MonthLocator(bymonth=[6, 12]))
    ax.xaxis.set_major_formatter(DateFormatter("%b '%y"))
    ax.set_ylim(0.001, 0.009)
    ax.autoscale_view()
    ax.xaxis.grid(True, 'major')
    ax.xaxis.grid(False, 'minor')
    fig.autofmt_xdate()
    plt.show()


helpers = [ql.SwapRateHelper(ql.QuoteHandle(ql.SimpleQuote(rate/100.0)),
                             ql.Period(*tenor), ql.TARGET(),
                             ql.Annual, ql.Unadjusted, ql.Thirty360(), ql.Euribor6M())
           for tenor, rate in [((6, ql.Months), 0.201),
                               ((2, ql.Years), 0.258),
                               ((5, ql.Years), 0.464),
                               ((10, ql.Years), 1.151),
                               ((15, ql.Years), 1.588)
                               ]
           ]

curve = ql.PiecewiseLinearZero(0, ql.TARGET(), helpers, ql.Actual360())

plot_curve(curve)
