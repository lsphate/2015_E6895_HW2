import sys
import datetime as dt
import pandas as pd
import pandas.io.data as pio
from pandas import Series
import matplotlib.pyplot as plot
from yahoo_finance import Share

def plotDiagram(company, today):
    df = pio.get_data_yahoo(
        company,
        start = dt.datetime(2015, 1, 1),
        end = dt.datetime(today.year, today.month, today.day))

    cprice = df['Adj Close']
    mavg = pd.rolling_mean(cprice, 10)
    ewma = pd.ewma(cprice, span = 3)
    print "\n" + company
    print ("  Close Price: "
            + str(Share(company).get_price())
#            + str(Share(company).get_historical(str(today), str(today)).pop(-1)['Adj_Close'])
            + " @ " + str(today))
    print ("  Estimate Price: "
            + str(predictPrice(cprice, mavg, ewma))
            + " @ " + str(today + dt.timedelta(days=1)))
    print "  Data analysis until " + str(today)
    cprice.plot(label = company)
    mavg.plot(label = 'MAVG')
    ewma.plot(label = 'EWMA')
    plot.legend()
    plot.show()

def predictPrice(CPRICE, MAVG, EWMA):
    gr = (1 - 5 ** 0.5) / 2
    return ((EWMA[-1] - EWMA[-2]) * (gr)
            + (MAVG[-1] - MAVG[-2]) * (1 - gr)
            + CPRICE[-1])

if __name__ == '__main__':
    print "\nCandidate Companies:"
    print "American Express(AXP), AT&T(T), Boeing(BA), General Electric(GE), Nike(NKE)"
    print "Goldman Sachs(GS), IBM(IBM), Microsoft(MSFT), McDonald\'s(MCD), Walmart(WMT)"

    today = dt.date.today()
    company = raw_input('\nEnter Company Code to estimate the price: ')

    plotDiagram(company, today)
