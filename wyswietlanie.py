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
    def __init__(self, X, minMAD):
        self.X=X
        self.minMAD=numpy.float64(minMAD)
        self.MAD=0
        self.threshold=0
        self.isAnomaly=False
        self.degree=0
        self.upperBound=0
        self.lowerBound=0

    def __calcualteMAD(self):
        self.MAD=numpy.median(numpy.abs(X-numpy.median(X)))

    def detectAnomalies(self, threshold):
        self.__calcualteMAD()
        if(self.MAD<self.minMAD):
            self.MAD=self.minMAD
        MADn=1.4826*self.MAD
        Z=numpy.abs(self.X[-1]-numpy.median(self.X))/MADn
        self.upperBound=numpy.abs(numpy.median(self.X) + MADn * threshold)
        self.lowerBound=numpy.abs(numpy.median(self.X) - MADn * threshold)
        if( Z> threshold):
            self.isAnomaly=True
            self.degree=Z // threshold

    def calculateThreshold(self):
        self.__calcualteMAD()
        if(self.MAD<self.minMAD):
            self.MAD=self.minMAD
        MADn=1.4826*self.MAD
        self.threshold=numpy.abs(self.X[-1]-numpy.median(self.X))/MADn
        

def runMAD_onData(data,windowSize, learningWindowSize):
    threshold=0.0
    for i in range (0, learningWindowSize-windowSize+1):
        X = [data[i:i+windowSize]]
        m=mad(X[0], 0.01)
        m.calculateThreshold()
        threshold = max ( m.threshold, threshold )
        print(threshold)
    threshold=1.1*threshold
    for i in range(learningWindowSize-windowSize+1, len(data)-windowSize+1, 1):
        X = [data[i:i+windowSize]]
        m=mad(X[0], 0.01)
        m.detectAnomalies(threshold)
        if(m.isAnomaly==True):
            #anomaliesX.append(X_time[i + windowSize])
            #anomaliesY.append(data[i + windowSize])
            print('upper bound breach' if X[0][-1]>m.upperBound else 'lower bound breach','anomaly of rank ', m.degree if m.degree<5 else 5, ' at ', i,'upper bound:', m.upperBound,'lower bound:', m.lowerBound ,'value:', X[0][-1])

                                          #####
###############################################

file_name = 'wczytywanie danych/data.txt'
data = pd.read_csv(file_name, ';')  # wczytanie pliku
X = data.values[:, 1]  # wczytanie pomiarow

X_time = []
for t in data.values[:, 0]:
    X_time.append(dt.strptime(t, '%Y-%m-%d %H:%M:%S')) # wczytanie formatu czasu

runMAD_onData(X, 700, 4200)  # 96 - okienko powinno byc 1 dzien, 2880 - miesiac

plt.figure(figsize=(10, 5))
plt.plot_date(anomaliesX, anomaliesY, 'ro', markersize=5)  # wyswietlanie annomalii
plt.plot_date(X_time, X, markersize=0.5, linestyle='solid')  # wyswietlanie wykresu
plt.tight_layout()

plt.show()