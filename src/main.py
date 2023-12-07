from time import sleep_ms

import machine
import requests

import beam
import config

if config.LAMBDA_URL is None:
    print("AWS lambda address is not set.")
    while True:
        pass


def minutes_to_ms(minutes: float) -> int:
    return int(minutes * 60 * 1000)


def sleep(minutes: float) -> None:
    # Ensure never sleep more than 12 hours
    minutes = min(minutes, 720)

    # Deepsleep will disable wifi and reset device on wakeup
    func = machine.deepsleep
    if minutes < 60:
        func = sleep_ms

    print(f"Sleeping for {minutes} minutes...")
    func(minutes_to_ms(minutes))


# Signal that mcu is entering main loop
beam.flash(times=3)

while True:
    try:
        response = requests.get(config.LAMBDA_URL).json()

        if response["lightBeam"] == True:
            print("Kings win! LIGHT THE BEAM!!")
            beam.pulse(minutes=120)  # Blocking

        sleep(response["sleepMinutes"])

    except Exception as e:
        print(f"Error: {e}\nResetting after 1 minute...")
        sleep_ms(minutes_to_ms(1))
        machine.reset()
