from driver import epd7in3f as epd_driver

print("Clearing screen on shutdown...")

epd = epd_driver.EPD()
epd.init()
epd.Clear()
epd.sleep()

print("Done")