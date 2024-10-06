from PIL import Image, ImageDraw, ImageFont
from scipy.interpolate import make_interp_spline
from datetime import datetime
import os
import math
import warnings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class InfoScreenHelper:
    def __init__(self):
        self.path_to_this_file = os.path.dirname(os.path.abspath(__file__))
        self.path_to_current_image = os.path.join(self.path_to_this_file, "current_image.bmp")
        self.path_to_current_weather_forecast = os.path.join(self.path_to_this_file, "current_weather_forecast.png")
        self.path_to_icons = os.path.join(self.path_to_this_file, "icons")
        self.fonts = {}
        self.initFonts()

    def getFont(self, font_name):
        return self.fonts[font_name]

    def initFonts(self):
        roboto = self.path_to_this_file + "/fonts/roboto/Roboto-"
        self.fonts = {

            'robotoBlack14': ImageFont.truetype(roboto + "Black.ttf", 14),
            'robotoBlack18': ImageFont.truetype(roboto + "Black.ttf", 18),
            'robotoBold22': ImageFont.truetype(roboto + "Bold.ttf", 22),
            'robotoBlack22': ImageFont.truetype(roboto + "Black.ttf", 22),
            'robotoBlack24': ImageFont.truetype(roboto + "Black.ttf", 24),
            'robotoBlack30': ImageFont.truetype(roboto + "Black.ttf", 30),
            'robotoBlack54': ImageFont.truetype(roboto + "Black.ttf", 54),
        }
    
    def add_panel_with_text(self, draw, panel_config, text):
        panel_height = panel_config["height"]
        font_text = self.fonts[panel_config["font_text"]]
        font_title = self.fonts[panel_config["font_title"]]
        padding = panel_config["padding"]
        panel_x1 = panel_config["x0"] + panel_config["width"] + padding

        draw = self.add_title_with_background(draw, panel_config, font_title, padding, panel_x1)

        # Break lines in case text length exceeds box width
        lines = []
        current_line = ""
        for word in text.split():
            test_line = current_line + word + " "
            text_width = draw.textlength(test_line, font=font_text)
            if text_width <= panel_config["width"]:
                current_line = test_line
            else:
                lines.append(current_line.rstrip())
                current_line = word + " "
        lines.append(current_line.rstrip())

        # Draw the text on the image with line breaks
        panel_y1 = panel_config["y0"] + font_title.size + 3*padding
        for index, line in enumerate(lines):
            if panel_y1 + 2*font_text.size > panel_config["y0"] + panel_height and index < len(lines) - 1:
                cut_off_line = line[:-3] + "..."
                draw.text((panel_config["x0"] + padding, panel_y1), cut_off_line, font=font_text, fill="black")
                warnings.warn("Text is cut off because it exceeds the given panel height.", category=UserWarning)
                break
            else:
                draw.text((panel_config["x0"] + padding, panel_y1), line, font=font_text, fill="black")
                panel_y1 += font_text.size # Move the y-coordinate down for the next line

        self.add_panel_border(draw, panel_config["x0"], panel_config["y0"], panel_x1, panel_config["y0"] + panel_height + padding)

    def clear_panel(self, draw, panel_config):
        panel_x1 = panel_config["x0"] + panel_config["width"] + panel_config["padding"]
        panel_y1 = panel_config["y0"] + panel_config["height"] + panel_config["padding"]
        draw.rectangle([panel_config["x0"], panel_config["y0"], panel_x1, panel_y1], fill = "white")
    
    def add_calendar_panel(self, image, panel_config, calendar_items):
        draw = ImageDraw.Draw(image)
        panel_height = panel_config["height"]
        font_text = self.fonts[panel_config["font_text"]]
        font_title = self.fonts[panel_config["font_title"]]
        padding = panel_config["padding"]
        panel_x1 = panel_config["x0"] + panel_config["width"] + padding
        title_y = panel_config["y0"] + padding
        calendar_icon = Image.open(os.path.join(self.path_to_icons, "calendar.png"))
        icon_size = 40
        resized_icon = calendar_icon.resize((icon_size, icon_size))

        draw = self.add_title_with_background(draw, panel_config, font_title, padding, panel_x1)

        # Add calendar item info
        panel_y1 = panel_config["y0"] + title_y + font_title.size
        max_number_of_calendar_items = math.floor((panel_height-panel_y1)/icon_size)
        for index, item in enumerate(calendar_items):
            image.paste(resized_icon, (panel_config["x0"]+padding, panel_y1))
            draw.text((panel_config["x0"]+2*padding+icon_size, panel_y1), f"{item['start_date']} {item['start_time']} - {item['end_date']} {item['end_time']}", font=font_text, fill="black")
            draw.text((panel_config["x0"]+2*padding+icon_size, panel_y1 + font_text.size), f"{item['content']}", font=font_text, fill="black")
            panel_y1 += icon_size + padding
            if index >= max_number_of_calendar_items - 1:
                break
        
        self.add_panel_border(draw, panel_config["x0"], panel_config["y0"], panel_x1, panel_config["y0"] + panel_height + padding)

    def add_weather_panel(self, image, panel_config, weather_data, forecast_data):
        draw = ImageDraw.Draw(image)
        panel_height = panel_config["y0"] + panel_config["height"]
        font_title = self.fonts[panel_config["font_title"]]
        padding = panel_config["padding"]
        panel_x1 = panel_config["x0"] + panel_config["width"] + padding
        icon_size = 70
        weather_icon = Image.open(os.path.join(self.path_to_icons, weather_data["icon"] + ".png"))
        resized_weather_icon = weather_icon.resize((icon_size, icon_size))
        humidity_icon = Image.open(os.path.join(self.path_to_icons, "humidity.png"))
        resized_humidity_icon = humidity_icon.resize((font_title.size, font_title.size))
        wind_icon = Image.open(os.path.join(self.path_to_icons, "wind.png"))
        resized_wind_icon = wind_icon.resize((font_title.size, font_title.size))

        draw = self.add_title_with_background(draw, panel_config, font_title, padding, panel_x1)

        # Add weather info
        panel_y1 = panel_config["y0"] + font_title.size + 3*padding
        cur_temp_text = f"{weather_data['temp_cur']}°C"
        feels_like_temp_text = f"Gefühlt {weather_data['temp_feels_like']}°C"
        min_max_text = f"{round(min(forecast_data['temp']))}°C | {round(max(forecast_data['temp']))}°C"
        humidity_text = f" {weather_data['humidity']}%"
        wind_text = f" {weather_data['wind']['speed']}m/s [{weather_data['wind']['dir']}]"
        image.paste(resized_humidity_icon, (panel_config["x0"] + padding, panel_y1), resized_humidity_icon)
        draw.text((panel_config["x0"] + padding + font_title.size, panel_y1), humidity_text, font=font_title, fill="black")
        image.paste(resized_wind_icon, (panel_config["x0"] + padding, panel_y1 + font_title.size), resized_wind_icon)
        draw.text((panel_config["x0"] + padding + font_title.size, panel_y1 + font_title.size), wind_text, font=font_title, fill="black")
        draw.text((panel_config["x0"] + padding, panel_y1 + 2*font_title.size), feels_like_temp_text, font=font_title, fill="black")
        icon_x = panel_config["x0"] + (panel_x1 - panel_config["x0"] + padding - icon_size) // 2
        image.paste(resized_weather_icon, (icon_x, panel_y1), resized_weather_icon)
        draw.text((icon_x + icon_size + 5*padding, panel_y1 - 2*padding), cur_temp_text, font=self.fonts["robotoBlack54"], fill="black")
        draw.text((icon_x + icon_size + 5*padding, panel_y1 + 2*font_title.size), min_max_text, font=font_title, fill="black")

        weather_forecast_output_filename = os.path.join(os.path.dirname(image.filename), "current_weather_forecast.png")
        self.create_weather_forecast_graph(panel_config=panel_config, forecast_data=forecast_data, output_filename=weather_forecast_output_filename)
        weather_forecast_graph = Image.open(weather_forecast_output_filename)
        image.paste(weather_forecast_graph, (panel_config["x0"] + padding, panel_y1 + icon_size), weather_forecast_graph)
        
        self.add_panel_border(draw, panel_config["x0"], panel_config["y0"], panel_x1, panel_height + padding)

    def create_weather_forecast_graph(self, panel_config, forecast_data, output_filename=""):
        now = datetime.now()
        current_hour = int(now.strftime("%H"))
        num_hours = 24
        
        # Create a time range in hours
        time_range = (np.arange(current_hour, current_hour + num_hours, step=3) % num_hours)
        
        x = np.arange(len(forecast_data["temp"]))

        # Create a figure and axis
        px = 1/plt.rcParams['figure.dpi']
        print(px)
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, gridspec_kw={'height_ratios': [1, 3]}, figsize=(panel_config["width"]*px*1.2, (panel_config["height"])/1.8*px))

        # Add weather icons
        img_width = 500
        img_height = 500
        gap = 315
        for i, icon in enumerate(forecast_data["icon"]):
            weather_icon = mpimg.imread(os.path.join(self.path_to_icons, icon + ".png"))
            left_x = i * (img_width + gap)
            right_x = left_x + img_width
            ax1.imshow(weather_icon, aspect="equal", origin="upper", extent=[left_x, right_x, 0, img_height])
        
        ax1.set_xlim(0, 8 * img_width + 7 * gap)
        ax1.set_ylim(0, img_height * 1.05)
        ax1.axis('off') 

        bars = ax2.bar(x, forecast_data["rain"], color="white", alpha=0.7, edgecolor="deepskyblue", linewidth=2, label="Niederschlag [mm]")
        ax2.set_yticks([])
        ax2.set_xlabel("Uhrzeit")
        ax2.set_xticks(x, labels=time_range)
        ax2.set_ylim([0, 5])

        # Add value labels to the bars
        for bar, value in zip(bars, forecast_data["rain"]):
            if value != 0:
                ax2.text(bar.get_x() + bar.get_width() / 2, 0, str(value),
                    ha="center", va="bottom", weight="bold", color="deepskyblue")
        
        # Move bars to zero in case rain forecast is all 0
        if not any(forecast_data["rain"]):
            ax2.set_ylim([0, 1])
        
        # Create a second y-axis on the right side
        ax3 = ax2.twinx()
        
        # Use a spline to smooth the line chart
        spl = make_interp_spline(x, forecast_data["temp"], k=3)
        x_smooth = np.linspace(x.min(), x.max(), 300)
        y2_smooth = spl(x_smooth)
        
        # Plot the line chart with a spline on the right axis
        ax3.plot(x_smooth, y2_smooth, color="indianred", label="Temp [°C]", linewidth=2)
        ax3.scatter(x, forecast_data["temp"], marker="o", color="indianred")
        
        # Add value labels to the line chart
        for i, txt in enumerate(forecast_data["temp"]):
            ax3.annotate(txt, (x[i], forecast_data["temp"][i]), textcoords="offset points", xytext=(0, 5), ha="center", color="indianred", weight="bold")

        # Offset spline by 1 to reduce overlap with bar annotation
        current_ylim = ax3.get_ylim()
        ax3.set_ylim([current_ylim[0] - 2.5, current_ylim[1] + 2.5])

        ax2.spines["top"].set_visible(False)
        ax2.spines["left"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.spines["top"].set_visible(False)
        ax2.spines["left"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        plt.axis("off")
        plt.savefig(output_filename, bbox_inches="tight")

    def add_date_info_panel(self, draw, panel_config, formatted_date):
        panel_height = panel_config["y0"] + panel_config["height"]
        font_text = self.fonts[panel_config["font_text"]]
        padding = panel_config["padding"]
        panel_x1 = panel_config["x0"] + panel_config["width"] + padding

        # Add date info
        date_width = draw.textlength(formatted_date, font=font_text)
        title_x = panel_config["x0"] + (panel_x1 - panel_config["x0"] + padding - date_width) // 2
        title_y = panel_config["y0"] + padding
        draw.text((title_x, title_y), formatted_date, font=font_text, fill="black")

        self.add_panel_border(draw, panel_config["x0"], panel_config["y0"], panel_x1, panel_height + padding)

    def get_current_image(self, width, height, white_hex_code):
        if os.path.exists(self.path_to_current_image):
            image = Image.open(self.path_to_current_image)
            return image
        else:
            new_empty_image = Image.new('RGB', (width, height), white_hex_code)
            new_empty_image.save(self.path_to_current_image)
            new_empty_image.filename = self.path_to_current_image
            return new_empty_image
    
    def add_title_with_background(self, draw, panel_config, font_title, padding, panel_x1):

        # Add title background
        draw.rectangle([panel_config["x0"], panel_config["y0"], panel_x1,
                         panel_config["y0"]+font_title.size+2*padding], fill=tuple(panel_config["title_background_color"]))
        
        # Add title
        title_width = draw.textlength(panel_config["title"], font=font_title)
        title_x = panel_config["x0"] + (panel_x1 - panel_config["x0"] + padding - title_width) // 2
        title_y = panel_config["y0"] + padding
        draw.text((title_x, title_y), panel_config["title"], font=font_title, fill="black")

        return draw
    
    def add_panel_border(self, draw, x0, y0, x1, y1, outline = "black"):
        draw.rectangle([x0, y0, x1, y1], outline = outline)

