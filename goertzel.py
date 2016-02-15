import math

class Goertzel:


    Q2 = 0
    Q1 = 0
    _N = 1000

    ADCCENTER = 512 # used to remove the DC offset

    omega=0
    coeff=0
    testData = None

    def ResetGoertzel(self):
        self.Q2 = 0;
        self.Q1 = 0;


    def ChangeParameters(self , TARGET_FREQUENCY, N, SAMPLING_FREQUENCY):
        self._SAMPLING_FREQUENCY=SAMPLING_FREQUENCY*1.0;	#on 16mhz, ~8928.57142857143, on 8mhz ~44444
        self._TARGET_FREQUENCY=TARGET_FREQUENCY*1.0; #should be integer of SAMPLING_RATE/N
        self._N=N;
        self.omega = (2.0 * math.pi * self._TARGET_FREQUENCY) / self._SAMPLING_FREQUENCY;
        self.coeff = 2.0 * math.cos(self.omega);
        self.ResetGoertzel();

        print "Bin Width ", SAMPLING_FREQUENCY/(N*1.0)


    def ProcessSample(self,sample):
        Q0 = self.coeff * self.Q1 - self.Q2 + (sample - self.ADCCENTER)
        self.Q2 = self.Q1
        self.Q1 = Q0

    def Detect(self):
        for index in range(self._N):
            self.ProcessSample(self.testData[index])

        magnitude = math.sqrt(self.Q1*self.Q1 + self.Q2*self.Q2 - self.coeff*self.Q1*self.Q2);
        self.ResetGoertzel()
        return magnitude

    def Generate(self,freq):
        step = freq * ((2.0 * math.pi) / self._SAMPLING_FREQUENCY);
        self.testData = []
        for index in range(self._N):
            val =(100.0 * math.sin(index * step) + 100.0)
            self.testData.append(val)






g = Goertzel()
g.ChangeParameters(941,205,8000)
##g.Generate(691)
##g.Detect()
##g.Generate(941)
##g.Detect()
##g.Generate(1191)
##g.Detect()

for x in range(691,1191):
    g.Generate(x)
    mag = g.Detect()
    print '%d,%f' % (x,mag)



print "OK"