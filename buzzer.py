class Buzzer:
    def __init__(self, pwm):
        self._pwm = pwm
        self._frequency = 600

    def on(self):
        self._pwm.freq(self._frequency)
        self._pwm.duty_u16(32768)

    def off(self):
        self._pwm.duty_u16(0)

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self._frequency = value
