# Pycom is still working on implementing the WDT
try: from machine import WDT
except ImportError: from pseudoWDT import WDT

def stop():
  """ If we are using a pseudoWDT stop it. Ignored on the real WDT. """
  try: wdt.stop()
  except: pass # FIXME What exception?