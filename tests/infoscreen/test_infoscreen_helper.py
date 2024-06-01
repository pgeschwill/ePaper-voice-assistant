import pytest
from PIL import Image, ImageDraw, ImageChops
from services.infoscreen import infoscreen_helper as ish
from os import path, listdir, remove

PATH_TO_THIS_FILE = path.dirname(path.abspath(__file__))
INFOSCREEN_HELPER = ish.InfoScreenHelper()
PATH_TO_WHITE_BASE = path.join(PATH_TO_THIS_FILE, "white_base.bmp")

class TestInfoscreenHelper:

    def teardown_method(self, method):
        file_list = listdir(PATH_TO_THIS_FILE)
        for file_name in file_list:
            if file_name.startswith("actual") or file_name.startswith("current"):
                file_path = path.join(PATH_TO_THIS_FILE, file_name)
                try:
                    remove(file_path)
                    print(f"Deleted: {file_path}")
                except OSError as e:
                    print(f"Error deleting {file_path}: {e}")

    def test_add_panel_with_text(self):
        # ARRANGE
        path_to_white_base = path.join(PATH_TO_THIS_FILE, "white_base.bmp")
        path_to_actual_output_file = path.join(PATH_TO_THIS_FILE, "actual_output_add_panel_with_text.bmp")
        path_to_expected_output_file = path.join(PATH_TO_THIS_FILE, "expected_output_add_panel_with_text.bmp")
        image = Image.open(path_to_white_base)
        draw = ImageDraw.Draw(image)
        text = "This is a very long text that should be broken with newlines and is getting even longer. This is even more text that should be broken down."
        panel_config = {
            "x0": 10,
            "y0": 10,
            "width": 390,
            "height": 190,
            "title": "Einkaufsliste",
            "title_background_color": [52, 143, 235],
            "font_text": "robotoBlack14",
            "font_title": "robotoBold22",
            "padding": 5
        }

        # ACT
        INFOSCREEN_HELPER.add_panel_with_text(draw, panel_config=panel_config, text=text)
        image.save(path_to_actual_output_file)
    
        # ASSERT
        diff = ImageChops.difference(Image.open(path_to_actual_output_file), Image.open(path_to_expected_output_file))
        assert diff.getbbox() is None
    
    def test_add_panel_with_text_cut_off(self):
        # ARRANGE
        path_to_white_base = path.join(PATH_TO_THIS_FILE, "white_base.bmp")
        path_to_actual_output_file = path.join(PATH_TO_THIS_FILE, "actual_output_add_panel_with_text_cut_off.bmp")
        path_to_expected_output_file = path.join(PATH_TO_THIS_FILE, "expected_output_add_panel_with_text_cut_off.bmp")
        image = Image.open(path_to_white_base)
        draw = ImageDraw.Draw(image)
        text = "This is a very long text that should be broken with newlines and is getting even longer. This is even more text that should be broken down."
        panel_config = {
            "x0": 10,
            "y0": 10,
            "width": 390,
            "height": 70,
            "title": "Einkaufsliste",
            "title_background_color": [52, 143, 235],
            "font_text": "robotoBlack14",
            "font_title": "robotoBold22",
            "padding": 5
        }

        # ACT
        with pytest.warns(UserWarning, match="Text is cut off because it exceeds the given panel height."):
            INFOSCREEN_HELPER.add_panel_with_text(draw, panel_config=panel_config, text=text)
            image.save(path_to_actual_output_file)
    
        # ASSERT
        diff = ImageChops.difference(Image.open(path_to_actual_output_file), Image.open(path_to_expected_output_file))
        assert diff.getbbox() is None
    
    def test_clear_panel(self):
        # ARRANGE
        path_to_white_base = path.join(PATH_TO_THIS_FILE, "white_base.bmp")
        path_to_actual_output_file = path.join(PATH_TO_THIS_FILE, "actual_output_clear_panel.bmp")
        image = Image.open(path_to_white_base)
        draw = ImageDraw.Draw(image)
        text = "Dummy text"
        panel_config = {
            "x0": 10,
            "y0": 10,
            "width": 390,
            "height": 100,
            "title": "Einkaufsliste",
            "title_background_color": [52, 143, 235],
            "font_text": "robotoBlack14",
            "font_title": "robotoBold22",
            "padding": 5
        }
        INFOSCREEN_HELPER.add_panel_with_text(draw, panel_config=panel_config, text=text)

        # ACT
        INFOSCREEN_HELPER.clear_panel(draw, panel_config)
        image.save(path_to_actual_output_file)
    
        # ASSERT
        diff = ImageChops.difference(Image.open(path_to_actual_output_file), Image.open(path_to_white_base))
        assert diff.getbbox() is None
    
    def test_partial_update(self):
        # ARRANGE
        path_to_white_base = path.join(PATH_TO_THIS_FILE, "white_base.bmp")
        path_to_actual_output_file = path.join(PATH_TO_THIS_FILE, "actual_output_partial_update.bmp")
        path_to_expected_output_file = path.join(PATH_TO_THIS_FILE, "expected_output_partial_update.bmp")
        image = Image.open(path_to_white_base)
        draw = ImageDraw.Draw(image)
        text = "Dummy text"
        panel_config_left = {
            "x0": 10,
            "y0": 10,
            "width": 380,
            "height": 100,
            "title": "Einkaufsliste",
            "title_background_color": [52, 143, 235],
            "font_text": "robotoBlack14",
            "font_title": "robotoBold22",
            "padding": 5
        }
        panel_config_right = {
            "x0": 400,
            "y0": 10,
            "width": 380,
            "height": 100,
            "title": "Dummy Title",
            "title_background_color": [52, 143, 235],
            "font_text": "robotoBlack14",
            "font_title": "robotoBold22",
            "padding": 5
        }
        INFOSCREEN_HELPER.add_panel_with_text(draw, panel_config=panel_config_left, text=text)
        INFOSCREEN_HELPER.add_panel_with_text(draw, panel_config=panel_config_right, text=text)

        # ACT
        INFOSCREEN_HELPER.clear_panel(draw, panel_config_left)
        INFOSCREEN_HELPER.add_panel_with_text(draw, panel_config=panel_config_left, text="New text")
        image.save(path_to_actual_output_file)
    
        # ASSERT
        diff = ImageChops.difference(Image.open(path_to_actual_output_file), Image.open(path_to_expected_output_file))
        assert diff.getbbox() is None

    def test_add_calendar_panel(self):
        # ARRANGE
        path_to_white_base = path.join(PATH_TO_THIS_FILE, "white_base.bmp")
        path_to_actual_output_file = path.join(PATH_TO_THIS_FILE, "actual_output_add_calendar_panel.bmp")
        path_to_expected_output_file = path.join(PATH_TO_THIS_FILE, "expected_output_add_calendar_panel.bmp")
        image = Image.open(path_to_white_base)
        panel_config = {
            "x0": 10,
            "y0": 10,
            "width": 390,
            "height": 150,
            "title": "Kalender",
            "title_background_color": [168, 58, 50],
            "font_text": "robotoBlack14",
            "font_title": "robotoBold22",
            "padding": 5
        }
        calendar_items = [
            {
                "content": "Test_item1",
                "start_date": "24.12.",
                "start_time": "16:00",
                "end_date": "24.12.",
                "end_time": "17:00"
            },
            {
                "content": "Test_item2",
                "start_date": "01.12.",
                "start_time": "11:00",
                "end_date": "03.12.",
                "end_time": "17:00"
            },
            {
                "content": "Test_item3",
                "start_date": "01.10.",
                "start_time": "11:30",
                "end_date": "02.12.",
                "end_time": "17:00"
            }
        ]

        # ACT
        INFOSCREEN_HELPER.add_calendar_panel(image, panel_config=panel_config, calendar_items=calendar_items)
        image.save(path_to_actual_output_file)
    
        # ASSERT
        diff = ImageChops.difference(Image.open(path_to_actual_output_file), Image.open(path_to_expected_output_file))
        assert diff.getbbox() is None

    def test_add_weather_panel(self):
        # ARRANGE
        path_to_white_base = path.join(PATH_TO_THIS_FILE, "white_base.bmp")
        path_to_actual_output_file = path.join(PATH_TO_THIS_FILE, "actual_output_add_weather_panel.bmp")
        path_to_expected_output_file = path.join(PATH_TO_THIS_FILE, "expected_output_add_weather_panel.bmp")
        image = Image.open(path_to_white_base)
        panel_config = {
            "x0": 400,
            "y0": 190,
            "width": 390,
            "height": 280,
            "title": "Wetter",
            "title_background_color": [168, 58, 50],
            "font_text": "robotoBlack14",
            "font_title": "robotoBold22",
            "padding": 5
        }
        weather_data = {
            "description":"scattered clouds",
            "humidity":85,
            "icon":"03n",
            "rain":{},
            "snow":{},
            "sunrise":"07:06",
            "sunset":"15:26",
            "temp_cur":2,
            "temp_feels_like":2,
            "temp_max":3,
            "temp_min":-1,
            "wind":{
                "dir":"N",
                "speed":1
                }
        }
        forecast_data = {
            "temp": [5, 6, 8.2, 9, 5, 12, 4.4 , 5],
            "precip": [23, 15, 0, 0, 88, 42, 69, 71],
            "rain": [2.1, 0.3, 0, 0, 0, 0.9, 0, 0.1]
        }

        # ACT
        INFOSCREEN_HELPER.add_weather_panel(image, panel_config=panel_config, weather_data=weather_data, forecast_data=forecast_data)
        cropped_image = image.crop((0, 0, 800, 430))
        cropped_image.save(path_to_actual_output_file)
    
        # ASSERT
        diff = ImageChops.difference(Image.open(path_to_actual_output_file), Image.open(path_to_expected_output_file))
        assert diff.getbbox() is None

    def test_add_weather_panel_with_empty_rain_data(self):
        # ARRANGE
        path_to_white_base = path.join(PATH_TO_THIS_FILE, "white_base.bmp")
        path_to_actual_output_file = path.join(PATH_TO_THIS_FILE, "actual_output_add_weather_panel_no_rain.bmp")
        path_to_expected_output_file = path.join(PATH_TO_THIS_FILE, "expected_output_add_weather_panel_no_rain.bmp")
        image = Image.open(path_to_white_base)
        panel_config = {
            "x0": 400,
            "y0": 190,
            "width": 390,
            "height": 280,
            "title": "Wetter",
            "title_background_color": [168, 58, 50],
            "font_text": "robotoBlack14",
            "font_title": "robotoBold22",
            "padding": 5
        }
        weather_data = {
            "description":"scattered clouds",
            "humidity":85,
            "icon":"03n",
            "rain":{},
            "snow":{},
            "sunrise":"07:06",
            "sunset":"15:26",
            "temp_cur":2,
            "temp_feels_like":2,
            "temp_max":3,
            "temp_min":-1,
            "wind":{
                "dir":"N",
                "speed":1
                }
        }
        forecast_data = {
            "temp": [5, 6, 8.2, 9, 5, 12, 4.4 , 5],
            "precip": [23, 15, 0, 0, 88, 42, 69, 71],
            "rain": [0, 0, 0, 0, 0, 0, 0, 0]
        }

        # ACT
        INFOSCREEN_HELPER.add_weather_panel(image, panel_config=panel_config, weather_data=weather_data, forecast_data=forecast_data)
        cropped_image = image.crop((0, 0, 800, 430))
        cropped_image.save(path_to_actual_output_file)
    
        # ASSERT
        diff = ImageChops.difference(Image.open(path_to_actual_output_file), Image.open(path_to_expected_output_file))
        assert diff.getbbox() is None