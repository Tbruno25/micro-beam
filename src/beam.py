from time import sleep, time

from machine import PWM, Pin

import config

DELAY = 0.003
RANGE = list(range(256, 1024))


pin = Pin(config.LED_GPIO)
frequency = 1_000
pwm = PWM(pin, freq=frequency, duty=0)


def fade_in() -> None:
    for i in RANGE:
        pwm.duty(i)
        sleep(DELAY)


def fade_out() -> None:
    for i in RANGE[::-1]:
        pwm.duty(i)
        sleep(DELAY)


def pulse(minutes: int) -> None:
    seconds = minutes * 60
    start = time()
    while time() - start < seconds:
        fade_in()
        fade_out()
    pwm.duty(0)


def flash(times: int) -> None:
    for _ in range(times):
        pwm.duty(RANGE[-1])
        sleep(0.2)
        pwm.duty(0)
        sleep(0.2)
