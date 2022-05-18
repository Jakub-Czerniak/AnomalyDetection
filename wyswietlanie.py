import numpy
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt

anomaliesX = []
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

    def __init__(self, X, minMAD, threshold):
        self.X = X
        self.minMAD = numpy.float64(minMAD)
        self.MAD = 0
        self.threshold = threshold
        self.isAnomaly = False

    def __calcualteMAD(self):
        self.MAD = numpy.median(numpy.abs(X-numpy.median(X)))


    def detectAnomalies(self):
        self.__calcualteMAD()
        # print('MAD ' + self.MAD.astype(str))
        if self.MAD < self.minMAD:
            self.MAD = self.minMAD
        MADn = 1.4826 * self.MAD
        # print('MADn ' + MADn.astype(str))
        # print('Last: ' + str(self.X[-1]))
        Z = numpy.abs(self.X[-1]-numpy.median(self.X))/MADn
        # print('Z ' + Z.astype(str))
        if Z > self.threshold:
            self.isAnomaly = True


def runMAD_onData(data, windowSize):
    for i in range(0, len(data)-windowSize+1, 1):
        X = [data[i:i+windowSize] ]
        # print(X[0])
        m = mad(X[0], 0.01, 3)
        m.detectAnomalies()
        if m.isAnomaly:
            anomaliesX.append(X_time[i + windowSize])
            anomaliesY.append(data[i + windowSize])
            print('anomaly at', i+windowSize)

                                          #####
###############################################

file_name = 'wczytywanie danych/data/p1.txt'
data = pd.read_csv(file_name, ';')  # wczytanie pliku
X = data.values[:, 1]  # wczytanie pomiarow

X_time = []
for t in data.values[:, 0]:
    X_time.append(dt.strptime(t, '%Y-%m-%d %H:%M:%S')) # wczytanie formatu czasu

runMAD_onData(X, 700)  # 96 - okienko powinno byc 1 dzien, 2880 - miesiac

plt.figure(figsize=(10, 5))
plt.plot_date(anomaliesX, anomaliesY, 'ro', markersize=5)  # wyswietlanie annomalii
plt.plot_date(X_time, X, markersize=0.5, linestyle='solid')  # wyswietlanie wykresu
plt.tight_layout()

plt.show()