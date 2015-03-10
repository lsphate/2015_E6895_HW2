import sys
import datetime
import pandas as pd
import pandas.io.data
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from yahoo_finance import Share

def plotDiagram(company, today):
    df = pd.io.data.get_data_yahoo(
        company,
        start = datetime.datetime(2015, 1, 1),
        end = datetime.datetime(today.year, today.month, today.day))

    cprice = df['Adj Close']
    mavg = pd.rolling_mean(cprice, 3)
    ewma = pd.ewma(cprice, span = 3)
    print "\n" + company
    print ("  Actual Price: "
            + str(Share(company).get_historical(str(today), str(today)).pop(-1)['Adj_Close'])
            + " @ " + str(today))
    print ("  Estimate Price: "
            + str(predictPrice(cprice, mavg, ewma))
            + " @ " + str(today + datetime.timedelta(days=1)))
    print "  Analysis by data until " + str(today)
#    cprice.plot(label = company)
#    mavg.plot(label = 'mavg')
#    ewma.plot(label = 'EWMA')
#    plt.legend()
#    plt.show()

def predictPrice(CPRICE, MAVG, EWMA):
    gr = (1 - 5 ** 0.5) / 2
    return ((EWMA[-1] - EWMA[-2]) * (gr)
            + (MAVG[-1] - MAVG[-2]) * (1 - gr)
            + CPRICE[-1])

if __name__ == '__main__':
#    print "\nCandidate Companies:"
#    print "American Express(AXP), AT&T(T), Boeing(BA), General Electric(GE), Nike(NKE)"
#    print "Goldman Sachs(GS), IBM(IBM), Microsoft(MSFT), McDonald\'s(MCD), Walmart(WMT)"

    firms = ['AXP', "T", 'BA', 'GE', 'NKE', 'GS', 'IBM', 'MSFT', 'MCD', 'WMT']
    today = datetime.date.today() - datetime.timedelta(days=0)
#    company = raw_input('\nEnter Company Code to estimate the price: ')

    for company in firms:
        plotDiagram(company, today)



