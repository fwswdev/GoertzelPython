'''
Goertzel Algorithm Implementation for
Translated from http://cms.edn.com/uploads/SourceCode/09banks.txt

Credits:
    http://www.embedded.com/design/configurable-systems/4024443/The-Goertzel-Algorithm

'''
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
        self._SAMPLING_FREQUENCY=SAMPLING_FREQUENCY*1.0;
        self._TARGET_FREQUENCY=TARGET_FREQUENCY*1.0;
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



TARGET_FREQUENCY, N, SAMPLING_FREQUENCY = (941,205,8000)


g = Goertzel()

g.ChangeParameters(TARGET_FREQUENCY, N, SAMPLING_FREQUENCY)


SWEEPFREQ_START = 691
SWEEPFREQ_END = 1191
for x in range(SWEEPFREQ_START,SWEEPFREQ_END):
    g.Generate(x)
    mag = g.Detect()
    print '%d,%f' % (x,mag)  # we print frequency in Hz, then the magnitude. This way we can easily import it to Openoffice Calc or Excel and graph it easily


print "Done"