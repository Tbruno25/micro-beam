import gc

import machine
import senko
from microwifimanager import manager

import config

wlan = manager.WifiManager().get_connection()


if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass


ota = senko.Senko(**config.REPO)


if ota.fetch():
    print("A newer version is available!\nUpdating...")
    if ota.update():
        print("Update complete!\nRebooting...")
        machine.reset()
else:
    print("Version up to date!")


gc.collect()
