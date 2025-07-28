from PIL import Image

import services.infoscreen.driver.epd7in3f as epd_driver


class InfoscreenDriver:
    def __init__(self, infoscreen_helper):
        self.epd = epd_driver.EPD()
        self.epd.init()
        self.infoscreen_helper = infoscreen_helper

    def clear_display_sleep(self, current_image, rotation):
        self.epd.init()
        self.epd.Clear()
        rotated_image = current_image.rotate(rotation)
        self.epd.display(self.epd.getbuffer(rotated_image))
        self.epd.sleep()

    def clear_display_on_shutdown(self, sig):
        print(f"Received signal {sig}. Shutting down...")
        self.epd.init()
        self.epd.Clear()
        self.epd.sleep()

    def run_screensaver(self):
        print("Starting screen saver.")
        self.epd.init()
        colors = (
            self.epd.WHITE,
            self.epd.BLACK,
            self.epd.GREEN,
            self.epd.BLUE,
            self.epd.RED,
            self.epd.YELLOW,
            self.epd.ORANGE,
        )

        for color in colors:
            image = Image.new("RGB", (self.epd.width, self.epd.height), color)
            self.epd.display(self.epd.getbuffer(image))
            self.epd.sleep(0.5)

        self.epd.Clear()
        self.epd.sleep()
        print("Screen saver finished.")

    def get_current_image(self):
        return self.infoscreen_helper.get_current_image(
            self.epd.width, self.epd.height, self.epd.WHITE
        )
