from PIL import Image
from time import sleep
from driver import epd7in3f as epd_driver

class ScreenSaver:
    def run(self):
        print("Starting screen saver.")
        epd = epd_driver.EPD()
        epd.init()
        colors = (epd.WHITE, epd.BLACK, epd.GREEN, epd.BLUE, epd.RED, epd.YELLOW, epd.ORANGE)

        for color in colors:
            image = Image.new('RGB', (epd.width, epd.height), color)
            epd.display(epd.getbuffer(image))
            sleep(0.5)
    
        epd.Clear()
        epd.sleep()
        print("Screen saver finished.")