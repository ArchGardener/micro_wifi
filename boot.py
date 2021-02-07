import esp
import gc
from micro_wifi import MicroWifi


def setup():
  esp.osdebug(None)
  gc.collect()


setup()
mw = MicroWifi()
mw.start()
