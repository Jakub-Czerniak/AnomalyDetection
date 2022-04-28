import numpy


class mad: 
    def __init__(self, X, minMAD, threshold):
        self.X=X
        self.minMAD=numpy.float64(minMAD)
        self.MAD=0
        self.threshold=threshold
        self.isAnomaly=False

    def __calcualteMAD(self):
        self.MAD=numpy.median(numpy.fabs(X-numpy.median(X)))

    def detectAnomalies(self):
        self.__calcualteMAD()
        print('MAD ' + self.MAD.astype(str))
        if(self.MAD<self.minMAD):
            self.MAD=self.minMAD
        MADn=1.4826*self.MAD
        print('MADn ' + MADn.astype(str))
        print('Last: ' + str(self.X[-1]))
        Z=numpy.fabs(X[-1]-numpy.median(X))/MADn
        print('Z ' + Z.astype(str))
        if(Z>self.threshold):
            self.isAnomaly=True

def runMAD_onData(data,windowSize):
    for i in range(0, len(data)-windowSize+1, 1):
        X = [data[i:i+windowSize] ]
        m=mad(X, 0.01,3)
        m.detectAnomalies()
        if(m.isAnomaly==True):
            print('anomaly at', len(X))

#X=[0.5,0.5,0.5,0.5,0.5,0.5,0.55,0.55,0.55,0.55,0.6,0.6,0.6,0.6,0.65,0.65,0.65,0.65,0.65,0.8,0.8,0.8,0.9]
#X=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,10,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,5]
X=[1,2,2.5,4,5,5,100]

runMAD_onData(X, 5)


        
