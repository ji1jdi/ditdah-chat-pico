from machine import Timer

class BreakIn:
    def __init__(self, delay, keyer):
        self._delay = delay
        self._keyer = keyer
        self._timer = Timer()
        self._sending = False

    def start_sending(self):
        if self._sending:
            return

        self._sending = True

    def stop_sending(self):
        if not self._sending:
            return

        self._start_timer()

    def _timeout(self, timer):
        if self._keyer.keying:
            self._start_timer()
        else:
            self._sending = False

    def _start_timer(self):
        self._timer.init(mode=Timer.ONE_SHOT, period=self._delay, callback=self._timeout)

    def _stop_timer(self):
        self._timer.deinit()

    @property
    def sending(self):
        return self._sending
