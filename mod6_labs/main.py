# main.py
"""Weather Application using Flet v0.28.3"""

import flet as ft
import json
import httpx
from pathlib import Path
from weather_service import WeatherService
from config import Config


class WeatherApp:
    """Main Weather Application class."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.history_file = Path("search_history.json")
        self.search_history = self.load_history()
        self.weather_service = WeatherService()
        self.current_unit = "metric"  
        self.current_temp = None
        self.setup_page()
        self.build_ui()
        self.page.run_task(self.get_current_location_weather)

        

    def add_to_history(self, city: str):
        """Add city to search history."""
        if city not in self.search_history:
            self.search_history.insert(0, city)
            self.search_history = self.search_history[:5]  # Keep last 5
    def load_history(self):
        """Load search history from file."""
        if self.history_file.exists():
            with open(self.history_file, "r") as f:
                return json.load(f)
        return []

    def save_history(self):
        """Save search history to file."""
        with open(self.history_file, "w") as f:
            json.dump(self.search_history, f)

    def add_to_history(self, city: str):
        """Add city to history and save."""
        if city not in self.search_history:
            self.search_history.insert(0, city)
            self.search_history = self.search_history[:10]  # Keep last 10
            self.save_history()

    def toggle_units(self, e):
        """Toggle between Celsius and Fahrenheit."""
        if self.current_unit == "metric":
            self.current_unit = "imperial"
            self.unit_button.icon = ft.Icons.THERMOSTAT
            if self.current_temp is not None:
                self.current_temp = (self.current_temp * 9/5) + 32
            self.update_display()
        else:
            self.current_unit = "metric"
            self.unit_button.icon = ft.Icons.ACQURTHERMOMETER
            if self.current_temp is not None:
                self.current_temp = (self.current_temp - 32) * 5/9
            self.update_display()

    def update_display(self):
        """Refresh UI after unit toggle."""
        if self.current_temp is not None:
            unit_symbol = "°F" if self.current_unit == "imperial" else "°C"
            self.weather_container.content.controls[2].value = f"{self.current_temp:.1f}{unit_symbol}"
            self.page.update()

    def build_history_dropdown(self):
        """Build dropdown with search history."""
        return ft.Dropdown(
            label="Recent Searches",
            expand = True,
            width=400,
            options=[ft.dropdown.Option(city) for city in self.search_history],
            on_change=lambda e: self.load_from_history(e.control.value),
        )
    
    def update_history_dropdown(self):
        """Refresh the history dropdown options."""
        self.history_dropdown.options = [
        ft.dropdown.Option(city) for city in self.search_history
    ]
        self.page.update()

    def load_from_history(self, city: str):
        """Load weather data from selected history city."""
        if not city:
            return
        self.city_input.value = city
        self.page.update()
        self.page.run_task(self.get_weather)

    def get_weather_style(self, description: str):
        """Return background color and emoji/icon based on weather."""
        desc = description.lower()
        if "rain" in desc:
            return ft.Colors.BLUE_600, "🌧️"
        elif "cloud" in desc:
            return ft.Colors.BLUE_GREY_400, "☁️"
        elif "clear" in desc:
            return ft.Colors.AMBER_300, "☀️"
        elif "snow" in desc:
            return ft.Colors.BLUE_100, "❄️"
        elif "thunder" in desc:
            return ft.Colors.DEEP_PURPLE_400, "⚡"
        else:
            return ft.Colors.LIGHT_BLUE_200, "🌤️"

    
    def setup_page(self):
        """Configure page settings."""
        self.page.title = Config.APP_TITLE
        
        # Add theme switcher
        self.page.theme_mode = ft.ThemeMode.SYSTEM  # Use system theme
        
        # Custom theme Colors
        self.page.theme = ft.Theme(
            color_scheme_seed=ft.Colors.BLUE,
        )
        
        self.page.padding = 20
        
        # Window properties are accessed via page.window object in Flet 0.28.3
        self.page.window.width = Config.APP_WIDTH
        self.page.window.height = Config.APP_HEIGHT
        self.page.window.resizable = False
        self.page.window.center()
        
    
    def build_ui(self):
        """Build the user interface."""

        # Title
        self.title = ft.Text(
            "Weather App",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_700
        )
        
        # City input field
        self.city_input = ft.TextField(
            label="Enter city name",
            hint_text="e.g., London, Tokyo, New York",
            border_color=ft.Colors.BLUE_400,
            prefix_icon=ft.Icons.LOCATION_CITY,
            autofocus=True,
            on_submit=self.on_search,
            expand= True
        )
        
        # Search button
        self.search_button = ft.ElevatedButton(
            "Search",
            icon=ft.Icons.SEARCH,
            on_click=self.on_search,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_700,
            ),
        )
        self.location_button = ft.IconButton(
            icon=ft.Icons.MY_LOCATION,
            tooltip="Get weather for current location",
            on_click=lambda e: self.page.run_task(self.get_location_weather),
        )



        
        # Weather display container (initially hidden)
        self.weather_container = ft.Container(
            visible=False,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            padding=25,
        )
            
        # Error message
        self.error_message = ft.Text(
            "",
            color=ft.Colors.RED_700,
            visible=False,
        )
        
        # Loading indicator
        self.loading = ft.ProgressRing(visible=False)
        # Theme toggle button
        self.theme_button = ft.IconButton(
            icon=ft.Icons.DARK_MODE,
            tooltip="Toggle theme",
            on_click=self.toggle_theme,
        )
       

        # Update the Column to include the theme button in the title row
        self.unit_button = ft.IconButton(
            icon=ft.Icons.DEVICE_THERMOSTAT,
            tooltip="Toggle °C / °F",
            on_click=self.toggle_units,
        )

        title_row = ft.Row(
            [
                self.title,
                ft.Row([self.unit_button, self.theme_button], spacing=10),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        search_row = ft.Row([
            self.city_input,
            self.search_button,
            self.location_button,
            ])

        self.history_dropdown = self.build_history_dropdown()
        
        # Add all components to page
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        title_row,
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        search_row,
                        self.history_dropdown,
                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                        self.loading,
                        self.error_message,
                        self.weather_container,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    spacing=25,
                ),
                padding=ft.padding.all(20),
                expand=True,
            )
        )
    
    def toggle_theme(self, e):
        """Toggle between light and dark theme."""
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.theme_button.icon = ft.Icons.LIGHT_MODE
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.theme_button.icon = ft.Icons.DARK_MODE
        self.page.update()
        
    def on_search(self, e):
        """Handle search button click or enter key press."""
        self.page.run_task(self.get_weather)
    
    async def get_weather(self):
        """Fetch and display weather data."""
        city = self.city_input.value.strip()
        
        # Validate input
        if not city:
            self.show_error("Please enter a city name")
            return
        
        # Show loading, hide previous results
        self.loading.visible = True
        self.error_message.visible = False
        self.weather_container.visible = False
        self.page.update()
        
        try:
            # Fetch weather data
            weather_data = await self.weather_service.get_weather(city)
            forecast_data = await self.weather_service.get_forecast(city)
            # Display weather
            self.add_to_history(city)
            self.update_history_dropdown()
            self.display_weather(weather_data,forecast_data)
            
        except Exception as e:
            self.show_error(str(e))
        
        finally:
            self.loading.visible = False
            self.page.update()
        # Use Flet's geolocation (if available)
    # Or use IP-based geolocation service

    async def get_location_weather(self):
        """Get weather for current location."""
        # This would require geolocation API
        # For now, use IP-based service
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://ipapi.co/json/")
                data = response.json()
                lat, lon = data['latitude'], data['longitude']
                weather = await self.weather_service.get_weather_by_coordinates(
                    lat, lon
                )
                self.display_weather(weather)
        except Exception as e:
            self.show_error("Could not get your location")
    async def get_current_location_weather(self):
        """Auto-detect current city and display its weather."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://ipapi.co/json/")
                data = response.json()
                city = data.get("city", "")

                if city:
                    self.city_input.value = city
                    await self.get_weather()
        except Exception:
            self.show_error("Could not detect your location")

    async def animate_location_fetch(self):
            """Animate location button while fetching location."""
            self.location_button.icon = ft.Icons.LOCATION_SEARCHING
            self.page.update()
            await self.get_location_weather()
            self.location_button.icon = ft.Icons.MY_LOCATION
            self.page.update()

    
    def display_weather(self, data: dict,forecast: dict):
        """Display weather information."""
        # Extract data
        city_name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        temp = data.get("main", {}).get("temp", 0)
        self.current_temp = temp
        feels_like = data.get("main", {}).get("feels_like", 0)
        humidity = data.get("main", {}).get("humidity", 0)
        description = data.get("weather", [{}])[0].get("description", "").title()
        icon_code = data.get("weather", [{}])[0].get("icon", "01d")
        wind_speed = data.get("wind", {}).get("speed", 0)
        # Determine dynamic style based on weather
        bg_color, emoji = self.get_weather_style(description)
        self.weather_container.animate = ft.Animation(500, "easeInOut")
        self.weather_container.bgcolor = bg_color
        
        # Build weather display
        forecast_cards = []
        if forecast:
            # Show 5 data points spaced by 8 (since forecast is every 3 hours)
            for i in range(0, len(forecast["list"]), 8):
                day = forecast["list"][i]
                date_txt = day["dt_txt"].split(" ")[0]
                icon = day["weather"][0]["icon"]
                temp_day = day["main"]["temp"]
                desc = day["weather"][0]["description"].title()

                forecast_cards.append(
                    ft.Container(
                        bgcolor=ft.Colors.BLUE_100,
                        border_radius=10,
                        padding=10,
                        width=100,
                        content=ft.Column(
                            [
                                ft.Text(date_txt, size=12, weight=ft.FontWeight.BOLD),
                                ft.Image(src=f"https://openweathermap.org/img/wn/{icon}.png", width=50, height=50),
                                ft.Text(f"{temp_day:.1f}°C", size=14),
                                ft.Text(desc, size=10, italic=True),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        )
                    )
                )
# Animate background color change
        self.weather_container.animate = ft.Animation(500, "easeInOut")
        self.weather_container.bgcolor = bg_color

        self.weather_container.content = ft.Column(
            [
                # Location
                ft.Text(
                    f"{city_name}, {country}",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                
                # Weather icon and description
                ft.Row(
                    [
                        ft.Image(
                            src=f"https://openweathermap.org/img/wn/{icon_code}@2x.png",
                            width=100,
                            height=100,
                        ),
                        ft.Text(
                            description,
                            size=20,
                            italic=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                
                # Temperature
                ft.Text(
                    f"{temp:.1f}°C",
                    size=48,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_900,
                ),
                
                ft.Text(
                    f"Feels like {feels_like:.1f}°C",
                    size=16,
                    color=ft.Colors.GREY_700 ,
                ),
                
                ft.Divider(),
                
                # Additional info
                ft.Row(
                    [
                        self.create_info_card(
                            ft.Icons.WATER_DROP,
                            "Humidity",
                            f"{humidity}%"
                        ),
                        self.create_info_card(
                            ft.Icons.AIR,
                            "Wind Speed",
                            f"{wind_speed} m/s"
                        ),
                        self.create_info_card(
                            ft.Icons.SPEED,
                            "Pressure",
                            f"{data['main']['pressure']} hPa"
                        ),
                        self.create_info_card(
                            ft.Icons.CLOUD,
                            "Cloudiness",
                            f"{data['clouds']['all']}%"
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    wrap=True,
                ),
                ft.Divider(),
                ft.Text("5-Day Forecast", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                ft.Row(forecast_cards, wrap=True, alignment=ft.MainAxisAlignment.CENTER)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
        
        self.weather_container.visible = True
        self.error_message.visible = False
        self.page.update()
    

    def create_info_card(self, icon, label, value):
        """Create an info card for weather details."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=30, color=ft.Colors.BLUE_700),
                    ft.Text(label, size=12, color=ft.Colors.GREY_900),
                    ft.Text(
                        value,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=15,
            width=150,
        )
    
    def show_error(self, message: str):
        """Display error message."""
        self.error_message.value = f"❌ {message}"
        self.error_message.visible = True
        self.weather_container.visible = False
        self.page.update()


def main(page: ft.Page):
    """Main entry point."""
    WeatherApp(page)


if __name__ == "__main__":
    ft.app(target=main)