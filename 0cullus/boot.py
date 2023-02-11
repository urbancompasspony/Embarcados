# This file is executed on every boot (including wake-boot from deepsleep)
# JAMAIS modifique este arquivo!

import gc
import network

ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

sta_if = network.WLAN(network.STA_IF)
sta_if.active(False)

gc.collect()
