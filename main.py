import asyncio
import network
import socket
import settings
from machine import Pin, PWM
from time import sleep_ms
from wifi import WIFI
from emitter import Emitter
from keyer import Keyer
from breakin import BreakIn
from buzzer import Buzzer
from led import LED

key = Pin(settings.KEY_PIN, Pin.IN, Pin.PULL_UP)

tx_emitter = Emitter()
rx_emitter = Emitter()

tx_keyer = Keyer(tx_emitter)
rx_keyer = Keyer(rx_emitter)

bkin = BreakIn(settings.BREAK_IN_DELAY, tx_keyer)
tx_emitter.on("on", bkin.start_sending)
tx_emitter.on("off", bkin.stop_sending)

buzzer = Buzzer(PWM(Pin(settings.BUZZER_PIN)))
buzzer.frequency = settings.PITCH
tx_emitter.on("on", buzzer.on)
tx_emitter.on("off", buzzer.off)
rx_emitter.on("on", buzzer.on)
rx_emitter.on("off", buzzer.off)

led = LED(Pin("LED", Pin.OUT))
tx_emitter.on("on", led.on)
tx_emitter.on("off", led.off)
rx_emitter.on("on", led.on)
rx_emitter.on("off", led.off)

def setup_wifi():
    wifi = WIFI(settings.WIFI_MODE)

    wifi.deactivate()
    wifi.activate()

    ifconfig = (settings.HOST_ADDR, settings.SUBNET_MASK,
                settings.GATEWAY_ADDR, settings.DNS_ADDR)

    if settings.WIFI_MODE == "AP":
        wifi.config(essid=settings.WIFI_SSID, password=settings.WIFI_KEY)
        wifi.ifconfig(ifconfig)
        print("AP mode started", wifi.ifconfig())
    else:
        wifi.ifconfig(ifconfig)
        wifi.connect(settings.WIFI_SSID, settings.WIFI_KEY)
        print("STA mode started", wifi.ifconfig())

async def rx():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", settings.PORT))
    s.setblocking(False)

    while True:
        try:
            data, addr = s.recvfrom(1024)

            if not bkin.sending:
                if data[0] == 1:
                    rx_keyer.on()
                else:
                    rx_keyer.off()
        except OSError:
            pass

        await asyncio.sleep(settings.TASK_DELAY)

async def tx():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        try:
            d = bytes([not key.value()])
            n = s.sendto(d, (settings.PEER_ADDR, settings.PORT))
        except OSError:
            pass

        await asyncio.sleep(settings.TASK_DELAY)

async def loop():
    while True:
        if key.value() == 0:
            tx_keyer.on()
        else:
            tx_keyer.off()

        await asyncio.sleep(settings.TASK_DELAY)

async def main():
    led.on()

    setup_wifi()

    led.off()

    await asyncio.gather(loop(), rx(), tx())

if __name__ == "__main__":
    asyncio.run(main())
