from machine import Pin, PWM
from time import sleep, time
import config


DELAY = 0.003
RANGE = list(range(256, 1024))


pin = Pin(config.LED_GPIO)
frequency = 5_000
pwm = PWM(pin, freq=frequency, duty=0)


def fade_in():
    for i in RANGE:
        pwm.duty(i)
        sleep(DELAY)


def fade_out():
    for i in RANGE[::-1]:
        pwm.duty(i)
        sleep(DELAY)


def pulse(minutes: int):
    seconds = minutes * 60
    start = time()
    while time() - start < seconds:
        fade_in()
        fade_out()
