import math

class Goertzel:


    Q2 = 0
    Q1 = 0
    _N = 0

    MAXN = 200

    omega=0
    coeff=0
    testData = None

    def ResetGoertzel(self):
        self.Q2 = 0;
        self.Q1 = 0;


    def ChangeParameters(self , TARGET_FREQUENCY, N, SAMPLING_FREQUENCY):
        self._SAMPLING_FREQUENCY=SAMPLING_FREQUENCY;	#on 16mhz, ~8928.57142857143, on 8mhz ~44444
        self._TARGET_FREQUENCY=TARGET_FREQUENCY; #should be integer of SAMPLING_RATE/N
        MAXN = self.MAXN
        if(N>MAXN):
            self._N=MAXN
        else:
            self._N=N;


        self.omega = (2.0 * math.pi * self._TARGET_FREQUENCY) / self._SAMPLING_FREQUENCY;

        self.coeff = 2.0 * math.cos(self.omega);

        self.ResetGoertzel();


    def Sample(self,sensorPin):
        self.testData = list()
        for x in range(self._N):
            self.testData.append(0) # add data here


    def Detect(self):
        for index in range(self._N):
            ProcessSample(self.testData[index]);

        magnitude = math.sqrt(self.Q1*self.Q1 + self.Q2*self.Q2 - self.coeff*self.Q1*self.Q2);
        ResetGoertzel()
        return magnitude




g = Goertzel()
g.ChangeParameters(700,100,8900)



print "OK"