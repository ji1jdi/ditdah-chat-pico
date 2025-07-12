class LED():
    def __init__(self, led):
        self._led = led

    def on(self):
        self._led.value(1)

    def off(self):
        self._led.value(0)
