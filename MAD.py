import numpy

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

X=[0.5,0.5,0.5,0.5,0.5,0.5,0.55,0.55,0.55,0.55,0.6,0.6,0.6,0.6,0.1,0.65,0.65,0.65,0.65,0.65,0.8,0.8,0.8,0.9]
#X=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,10,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,5]
#X=[1.0,2.0,2.5,4.0,5.0,5.0,100]

runMAD_onData(X, 5, 10)
