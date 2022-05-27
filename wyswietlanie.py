import numpy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from datetime import datetime as dt

anomaliesX = []
anomalies_ranks = []
anomaliesY = []

def calculate_mean_delta(dat, date,  num):
    iterator = num
    data_out = []
    date_out = []
    while iterator < len(dat):
        data_out.append(dat[iterator] - dat[iterator-num])
        date_out.append(date[iterator])
        iterator = iterator + num
    return data_out, date_out


###############################################
#### Algorytm
class mad:
    def __init__(self, X, minMAD):
        self.X = X
        self.minMAD = numpy.float64(minMAD)
        self.MAD = 0
        self.threshold = 0
        self.isAnomaly = False
        self.degree = 0
        self.upperBound = 0
        self.lowerBound = 0

    def __calcualteMAD(self):
        self.MAD = numpy.median(numpy.abs(X - numpy.median(X)))

    def detectAnomalies(self, threshold):
        self.__calcualteMAD()
        if (self.MAD < self.minMAD):
            self.MAD = self.minMAD
        MADn = 1.4826 * self.MAD
        Z = numpy.abs(self.X[-1] - numpy.median(self.X)) / MADn
        self.upperBound = numpy.abs(numpy.median(self.X) + MADn * threshold)
        self.lowerBound = numpy.abs(numpy.median(self.X) - MADn * threshold)
        if (Z > threshold):
            self.isAnomaly = True
            self.degree = Z // threshold

    def calculateThreshold(self):
        self.__calcualteMAD()
        if (self.MAD < self.minMAD):
            self.MAD = self.minMAD
        MADn = 1.4826 * self.MAD
        self.threshold = numpy.abs(self.X[-1] - numpy.median(self.X)) / MADn


def runMAD_onData(data, windowSize, learningWindowSize):
    threshold = 0.0
    for i in range(0, learningWindowSize - windowSize + 1):
        X = [data[i:i + windowSize]]
        m = mad(X[0], 0.01)
        m.calculateThreshold()
        threshold = max(m.threshold, threshold)
        print(threshold)
    threshold = 1.1 * threshold
    for i in range(learningWindowSize - windowSize + 1, len(data) - windowSize, 1):
        X = [data[i:i + windowSize]]
        m = mad(X[0], 0.01)
        m.detectAnomalies(threshold)
        if (m.isAnomaly == True):
            anomaliesX.append(X_time[i + windowSize])
            anomaliesY.append(data[i + windowSize])
            if  m.degree < 5:
                anomalies_ranks.append(m.degree)
            else:
                anomalies_ranks.append(5)
            print('upper bound breach' if X[0][-1] > m.upperBound else 'lower bound breach', 'anomaly of rank ',
                  m.degree if m.degree < 5 else 5, ' at ', i, 'upper bound:', m.upperBound, 'lower bound:',
                  m.lowerBound, 'value:', X[0][-1])

            #####
###############################################

file_name = './data/24713573.txt.txt'
data = pd.read_csv(file_name, ';')  # wczytanie pliku
X = data.values[:, 1]  # wczytanie pomiarow

X_time = []
for t in data.values[:, 0]:
    X_time.append(dt.strptime(t, '%Y-%m-%d %H:%M:%S')) # wczytanie formatu czasu

X1, Y1 = calculate_mean_delta(X, X_time, 1)

runMAD_onData(X1, 300, 700)  # 96 - okienko powinno byc 1 dzien, 2880 - miesiac, 5760 - 2 miesiace

delta_usage_anomalies = plt.figure(figsize=(10, 5))
# plt.plot_date(anomaliesX, anomaliesY, 'ro', markersize=5)  # wyswietlanie annomalii
plt.plot_date(Y1, X1, markersize=0.5, linestyle='solid')

#   Zdefiniowane kolory wyswietlania
colours = ['thistle', 'plum', 'violet', 'red', 'darkred']
for x in anomaliesX:
    anomaly_rank = int(anomalies_ranks[anomaliesX.index(x)])
    colour = colours[anomaly_rank - 1]
    plt.axvline(x, ls='-', color=colour)
plt.xlabel("date")
plt.ylabel("Δ water usage")
plt.tight_layout()

delta_usage = plt.figure(figsize=(10, 5))
# plt.plot_date(anomaliesX, anomaliesY, 'ro', markersize=5)  # wyswietlanie annomalii
plt.plot_date(Y1, X1, markersize=0.5, linestyle='solid')
plt.xlabel("date")
plt.ylabel("Δ water usage")
plt.tight_layout()

usage = plt.figure(figsize=(10, 5))
plt.plot_date(X_time, X, markersize=0.5, linestyle='solid')
for x in anomaliesX:
    anomaly_rank = int(anomalies_ranks[anomaliesX.index(x)])
    colour = colours[anomaly_rank - 1]
    plt.axvline(x, ls='-', color=colour, alpha=0.1)
plt.xlabel("date")
plt.ylabel("water usage")
plt.tight_layout()
plt.show()

