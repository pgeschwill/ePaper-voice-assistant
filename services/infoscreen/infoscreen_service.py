from datetime import datetime
from urllib.parse import unquote
from flask import Flask, request, jsonify
from PIL import  ImageDraw
import json
import signal
import infoscreen_helper as ish
import infoscreen_driver as isd

app = Flask(__name__)
with open("../../config/config.json") as config_file:
        config = json.load(config_file)
ROTATION = config["infoscreen"]["rotation"]
INFOSCREEN_HELPER = ish.InfoScreenHelper()
DRIVER = isd.InfoscreenDriver(INFOSCREEN_HELPER)

def clear_display_on_shutdown(sig, frame):
    DRIVER.clear_display_on_shutdown(sig)

signal.signal(signal.SIGTERM, clear_display_on_shutdown)
signal.signal(signal.SIGINT, clear_display_on_shutdown)

@app.route("/health", methods=['GET'])
def health():
    return jsonify(success=True)

@app.route("/update_calendar_panel", methods=['POST'])
def update_calendar_panel():
    data = request.json
    calendar_items = json.loads(unquote(data.get("calendar_items")))
    panel_config = data.get("panel_config")
    clear_display_sleep = data.get("clear_display_sleep")
    current_image = DRIVER.get_current_image()
    draw = ImageDraw.Draw(current_image)
    INFOSCREEN_HELPER.clear_panel(draw, panel_config)
    INFOSCREEN_HELPER.add_calendar_panel(current_image, panel_config=panel_config, calendar_items=calendar_items)
    current_image.save(current_image.filename)
    if clear_display_sleep:
        DRIVER.clear_display_sleep(current_image, ROTATION)
    return jsonify(success=True)

@app.route("/update_weather_panel", methods=['POST'])
def update_weather_panel():
    data = request.json
    weather_data = json.loads(unquote(data.get("weather_data")))
    forecast_data = json.loads(unquote(data.get("forecast_data")))
    panel_config = data.get("panel_config")
    clear_display_sleep = data.get("clear_display_sleep")
    current_image = DRIVER.get_current_image()
    draw = ImageDraw.Draw(current_image)
    INFOSCREEN_HELPER.clear_panel(draw, panel_config)
    INFOSCREEN_HELPER.add_weather_panel(current_image, panel_config=panel_config, weather_data=weather_data, forecast_data=forecast_data)
    current_image.save(current_image.filename)
    if clear_display_sleep:
        DRIVER.clear_display_sleep(current_image, ROTATION)
    return jsonify(success=True)

@app.route("/update_shopping_list_panel", methods=['POST'])
def update_shopping_list_panel():
    data = request.json
    shopping_list_content = unquote(data.get("shopping_list_content"))
    panel_config = data.get("panel_config")
    clear_display_sleep = data.get("clear_display_sleep")
    current_image = DRIVER.get_current_image()
    draw = ImageDraw.Draw(current_image)
    INFOSCREEN_HELPER.clear_panel(draw, panel_config)
    INFOSCREEN_HELPER.add_panel_with_text(draw, panel_config=panel_config, text=shopping_list_content)
    current_image.save(current_image.filename)
    if clear_display_sleep:
        DRIVER.clear_display_sleep(current_image, ROTATION)
    return jsonify(success=True)

@app.route("/update_mental_load_panel", methods=['POST'])
def update_mental_load_panel():
    data = request.json
    mental_load_content = unquote(data.get("mental_load_content"))
    panel_config = data.get("panel_config")
    clear_display_sleep = data.get("clear_display_sleep")
    current_image = DRIVER.get_current_image()
    draw = ImageDraw.Draw(current_image)
    INFOSCREEN_HELPER.clear_panel(draw, panel_config)
    INFOSCREEN_HELPER.add_panel_with_text(draw, panel_config=panel_config, text=mental_load_content)
    current_image.save(current_image.filename)
    if clear_display_sleep:
        DRIVER.clear_display_sleep(current_image, ROTATION)
    return jsonify(success=True)

@app.route("/update_date_info_panel", methods=['POST'])
def update_date_info_panel():
    data = request.json
    panel_config = data.get("panel_config")
    clear_display_sleep = data.get("clear_display_sleep")
    formatted_date = datetime.now().strftime('%A, %d.%m.%Y')
    current_image = DRIVER.get_current_image()
    draw = ImageDraw.Draw(current_image)
    INFOSCREEN_HELPER.clear_panel(draw, panel_config)
    INFOSCREEN_HELPER.add_date_info_panel(draw, panel_config=panel_config, formatted_date=formatted_date)
    current_image.save(current_image.filename)
    if clear_display_sleep:
        DRIVER.clear_display_sleep(current_image, ROTATION)
    return jsonify(success=True)

@app.route("/display_screensaver", methods=['GET'])
def display_screensaver():
    DRIVER.run_screensaver()
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)