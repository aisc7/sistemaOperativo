import os
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
import folium


class WeatherMapWindow(QWidget):
    def __init__(self, city="Manizales", api_key="b8ba6c5b502f1e5886a05432bca9928e", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mapa del Clima")
        self.setGeometry(200, 200, 800, 600)

        self.city = city
        self.api_key = api_key

        # Coordenadas de la ciudad principal
        self.city_coords = {"lat": 5.0703, "lon": -75.5138}  # Coordenadas de Manizales

        # Lista de ciudades cercanas (latitud, longitud, nombre)
        self.nearby_cities = [
            {"lat": 4.8124, "lon": -75.6961, "name": "Pereira"},
            {"lat": 5.3378, "lon": -72.3939, "name": "Villavicencio"},
            {"lat": 4.6790, "lon": -74.0493, "name": "Bogotá"},
        ]

        # Crear el layout principal
        layout = QVBoxLayout(self)

        # Crear visor web
        self.map_view = QWebEngineView(self)
        layout.addWidget(self.map_view)

        # Generar el mapa dinámicamente y cargarlo en el visor
        self.load_weather_map()

    def load_weather_map(self):
        """Generar y cargar el mapa en el visor web."""
        # URL para las capas del clima usando la API de OpenWeatherMap
        temp_layer_url = (
            f"https://tile.openweathermap.org/map/temp_new/{{z}}/{{x}}/{{y}}.png?appid={self.api_key}"
        )
        precip_layer_url = (
            f"https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid={self.api_key}"
        )

        # Crear el mapa usando Folium
        folium_map = folium.Map(
            location=[self.city_coords["lat"], self.city_coords["lon"]],
            zoom_start=9,
            tiles="OpenStreetMap",  # Fondo base para el mapa
        )

        # Agregar la capa de temperatura al mapa
        folium.TileLayer(
            tiles=temp_layer_url,
            attr="OpenWeatherMap",
            name="Temperatura",
            overlay=True,
            control=True,
        ).add_to(folium_map)

        # Agregar la capa de precipitaciones al mapa
        folium.TileLayer(
            tiles=precip_layer_url,
            attr="OpenWeatherMap",
            name="Precipitaciones",
            overlay=True,
            control=True,
        ).add_to(folium_map)

        # Agregar un marcador en la ubicación principal de la ciudad
        folium.Marker(
            [self.city_coords["lat"], self.city_coords["lon"]],
            popup=f"<b>Ciudad:</b> {self.city}<br><b>Lat:</b> {self.city_coords['lat']}<br><b>Lon:</b> {self.city_coords['lon']}",
            tooltip=f"{self.city} (Haga clic para más info)",
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(folium_map)

        # Agregar marcadores para ciudades cercanas
        for city in self.nearby_cities:
            folium.Marker(
                [city["lat"], city["lon"]],
                popup=f"<b>Ciudad:</b> {city['name']}<br><b>Lat:</b> {city['lat']}<br><b>Lon:</b> {city['lon']}",
                tooltip=f"{city['name']} (Haga clic para más info)",
                icon=folium.Icon(color="green", icon="info-sign"),
            ).add_to(folium_map)

        # Agregar controles de capas
        folium.LayerControl().add_to(folium_map)

        # Renderizar el HTML del mapa
        map_html = folium_map.get_root().render()

        # Cargar el HTML directamente en el visor
        self.map_view.setHtml(map_html)


if __name__ == "__main__":
    import sys

    # Crear la aplicación Qt
    app = QApplication(sys.argv)

    # Crear y mostrar la ventana del mapa
    window = WeatherMapWindow()
    window.show()

    # Ejecutar la aplicación
    sys.exit(app.exec())
