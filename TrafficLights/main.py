import json
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy_garden.mapview import MapView, MapMarker
from kivy.config import Config

from kivy_garden.mapview.clustered_marker_layer import ClusteredMarkerLayer

from MapApp import MapApp

TIMISOARA_LAT = 45.747231774279214
TIMISOARA_LON = 21.231679569701775
TIMISOARA_RADIUS = 10000

class CustomMapMarker(MapMarker):
    def __init__(self, id_tl, id_cross, **kwargs):
        super().__init__(**kwargs)
        self.id_tl = id_tl
        self.id_cross = id_cross
        self.bind(on_release=self.on_marker_click)
        print(self.id_tl, self.id_cross, self.lon)

    def on_marker_click(self, *args):
        # Create input fields
        intersection_id_input = TextInput(multiline=False, height=40, font_size=12)
        traffic_light_id_input = TextInput(multiline=False, height=40, font_size=12)

        # Create save button
        save_button = Button(text='Save')
        save_button.bind(
            on_release=lambda button: self.update_ids(self.lon, intersection_id_input.text,
                                                      traffic_light_id_input.text))
        delete_button = Button(text='Delete')
        delete_button.bind(on_release=lambda button: self.delete_marker(self.lon))
        # Create layout for pop-up content
        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(Label(text=str(self.id_cross) + ";" + str(self.id_tl) + "      Lon:" + str(self.lon)))
        print("From label:")
        print(self.id_tl, self.id_cross, self.lon)
        popup_content.add_widget(Label(text='Insert Intersection ID:'))
        popup_content.add_widget(intersection_id_input)
        popup_content.add_widget(Label(text='Insert Traffic Light ID:'))
        popup_content.add_widget(traffic_light_id_input)
        popup_content.add_widget(save_button)
        popup_content.add_widget(delete_button)

        # Create and open the pop-up
        popup = Popup(title="Marker Info", content=popup_content, size_hint=(None, None), size=(400, 300))
        popup.open()

    def update_ids(self, lon, intersection_id, traffic_light_id):
        for feature in MapManager.trafficlight_data['features']:
            # Extract longitude value from coordinates
            # lon_value = feature['geometry']['coordinates'][0]

            # Check if longitude matches
            if feature['geometry']['coordinates'][0] == lon:
                feature['properties']['intersection_id'] = intersection_id
                feature['properties']['traffic_light_id'] = traffic_light_id

                # Break loop once found and updated
                break

    def delete_marker(self, lon):
        for feature in MapManager.trafficlight_data['features']:
            if feature['geometry']['coordinates'][0] == lon:
                MapManager.trafficlight_data["features"].remove(feature)
        # Delete the marker or perform any other deletion logic
        pass


def save_json_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


class MapManager(App):
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tl_dict = {}
    trafficlight_data = None
    id_cross = None
    id_tl = None

    def build(self):
        # mapview = MapView(zoom=10, lat=TIMISOARA_LAT, lon=TIMISOARA_LON)
        mapview = MapView(zoom=10, lat=TIMISOARA_LAT, lon=TIMISOARA_LON)
        black_tl_png = os.path.join(MapManager.script_dir, 'venv', 'icons', 'BlackTL3.png')
        constr_tl_png = os.path.join(MapManager.script_dir, 'venv', 'icons', 'ConstructTL.png')

        with open('filtered_trafficlight_response.json', 'r') as f:
            trafficlight_data = json.load(f)
        MapManager.trafficlight_data = trafficlight_data
        # iterate from json
        clustered_layer = ClusteredMarkerLayer()
        for feature in trafficlight_data["features"]:
            if "geometry" in feature and "coordinates" in feature["geometry"]:
                coordinates = feature["geometry"]["coordinates"]
                if len(coordinates) == 2:
                    parent_id_cross = feature["properties"]["intersection_id"]
                    parent_id_tl = feature["properties"]["traffic_light_id"]
                    marker = CustomMapMarker(lat=coordinates[1], lon=coordinates[0], source=black_tl_png,
                                             id_tl=parent_id_tl, id_cross=parent_id_cross)
                    marker.id_tl = parent_id_tl
                    marker.id_cross = parent_id_cross
                    clustered_layer.add_marker(marker.lon, marker.lat, cls=CustomMapMarker,
                                               options={'source': marker.source, 'id_tl': marker.id_tl,
                                                        'id_cross': marker.id_cross})
        mapview.add_layer(clustered_layer)

        # Creating buttons
        create_tl = Button(text="Create TrafficLight", size_hint_y=0.3)
        save_json = Button(text="Save Json", size_hint_y=0.3)
        save_json.bind(
            on_release=lambda button: save_json_data('filtered_trafficlight_response.json', trafficlight_data))
        delete_marker = Button(text="Delete Marker", size_hint_y=0.3)
        delete_marker.bind(on_release=self.delete_marker)
        haha = Button(text="Bafta Rosu!", size_hint_y=0.3)

        button_layout = BoxLayout(orientation='vertical', size=(200, 500))
        button_layout.add_widget(create_tl)
        button_layout.add_widget(save_json)
        button_layout.add_widget(haha)

        mapview.add_widget(button_layout)
        mapview.bind(on_touch_down=self.on_touch_down)

        return mapview

    def on_touch_down(self,instance, touch):
        if touch.button == 'right':
            self.show_popup(touch.pos)
            return True

    #mapview.bind(on_touch_down=on_touch_down)

    def show_popup(self, pos):
        # Create input fields
        mapview = self.root
        lat, lon = mapview.get_latlon_at(*pos)

        lat = round(pos[1], 6)
        lon = round(pos[0], 6)

        intersection_id_input = TextInput(multiline=False, height=40, font_size=12)
        traffic_light_id_input = TextInput(multiline=False, height=40, font_size=12)

        # Create OK and Cancel buttons
        ok_button = Button(text='OK')
        cancel_button = Button(text='Cancel')

        # Create layout for pop-up content
        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(Label(text='Latitude: ' + str(lat)))
        popup_content.add_widget(Label(text='Longitude: ' + str(lon)))
        popup_content.add_widget(Label(text='Insert Intersection ID:'))
        popup_content.add_widget(intersection_id_input)
        popup_content.add_widget(Label(text='Insert Traffic Light ID:'))
        popup_content.add_widget(traffic_light_id_input)
        popup_content.add_widget(ok_button)
        popup_content.add_widget(cancel_button)

        # Create the pop-up
        popup = Popup(title="Add Traffic Light", content=popup_content, size_hint=(None, None), size=(400, 300),
                      auto_dismiss=False)

        # Define OK and Cancel button behaviors
        def on_ok(instance):
            # Perform action on OK button press
            self.add_traffic_light(lat, lon, intersection_id_input.text, traffic_light_id_input.text)
            popup.dismiss()

        def on_cancel(instance):
            # Close the pop-up on Cancel button press
            popup.dismiss()

        ok_button.bind(on_release=on_ok)
        cancel_button.bind(on_release=on_cancel)

        # Open the pop-up
        popup.open()

    def add_traffic_light(self, lat, lon, intersection_id, traffic_light_id):
        # Add your logic to add the traffic light here
        pass

    def delete_marker(self, instance):
        # Add your deletion logic here
        pass


if __name__ == '__main__':
    # MapApp().run()
    MapManager().run()
