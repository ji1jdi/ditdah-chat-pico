import network
from time import sleep_ms

STATUS_NAME = {
    network.STAT_IDLE:           "IDLE",
    network.STAT_CONNECTING:     "CONNECTING",
    network.STAT_WRONG_PASSWORD: "WRONG_PASSWORD",
    network.STAT_GOT_IP:         "GOT_IP",
    network.STAT_NO_AP_FOUND:    "NO_AP_FOUND",
    network.STAT_CONNECT_FAIL:   "CONNECT_FAIL",
}

class WIFI:
    def __init__(self, mode):
        self._wlan = network.WLAN(mode == "AP" if network.AP_IF else network.STA_IF)

    def activate(self):
        self._wlan.active(True)
        while not self._wlan.active():
            sleep_ms(100)

    def deactivate(self):
        self._wlan.active(False)
        self._wlan.disconnect()
        while self._wlan.active() or self._wlan.isconnected():
            sleep_ms(100)

    def is_active(self):
        return self._wlan.active()

    def status(self):
        return self._wlan.status()

    def config(self, *args, **kwargs):
        return self._wlan.config(*args, **kwargs)

    def ifconfig(self, *args):
        return self._wlan.ifconfig(*args)

    def connect(self, ssid, key):
        print("connecting...")

        while not self._wlan.isconnected():
            self._wlan.connect(ssid, key)

            for i in range(10):
                print(self.status_name(), self.ifconfig())

                if self._wlan.status() == network.STAT_GOT_IP:
                    break

                sleep_ms(1000)

        print("connected")

    def is_connected(self):
        return self._wlan.isconnected()

    def status_name(self):
        return STATUS_NAME.get(self._wlan.status(), "?")
