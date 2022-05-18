import numpy

class mad: 
    def __init__(self, X, minMAD):
        self.X=X
        self.minMAD=numpy.float64(minMAD)
        self.MAD=0
        self.threshold=0
        self.isAnomaly=False

    def __calcualteMAD(self):
        self.MAD=numpy.median(numpy.fabs(X-numpy.median(X)))

    def detectAnomalies(self, threshold):
        self.__calcualteMAD()
        if(self.MAD<self.minMAD):
            self.MAD=self.minMAD
        MADn=1.4826*self.MAD
        Z=numpy.fabs(self.X[-1]-numpy.median(self.X))/MADn
        if( Z> threshold):
            self.isAnomaly=True

    def calculateThreshold(self):
        self.__calcualteMAD()
        if(self.MAD<self.minMAD):
            self.MAD=self.minMAD
        MADn=1.4826*self.MAD
        self.threshold=numpy.fabs(self.X[-1]-numpy.median(self.X))/MADn
        

def runMAD_onData(data,windowSize, learningWindowSize):
    threshold=0.0
    for i in range (0, learningWindowSize-windowSize+1):
        X = [data[i:i+windowSize]]
        m=mad(X[0], 0.01)
        m.calculateThreshold()
        threshold = max ( m.threshold, threshold )
        print(threshold)
    for i in range(learningWindowSize-windowSize+1, len(data)-windowSize+1, 1):
        X = [data[i:i+windowSize]]
        m=mad(X[0], 0.01)        
        m.detectAnomalies(threshold)
        if(m.isAnomaly==True):
            print('anomaly at', i+windowSize)

X=[0.5,0.5,0.5,0.5,0.5,0.5,0.55,0.55,0.55,0.55,0.6,0.6,0.6,0.6,0.65,0.65,0.65,0.65,0.65,0.8,0.8,0.8,0.9]
#X=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,10,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,5]
#X=[1.0,2.0,2.5,4.0,5.0,5.0,100]

runMAD_onData(X, 5, 10)
