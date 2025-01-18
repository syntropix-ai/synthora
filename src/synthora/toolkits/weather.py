import json
import os
from typing import Literal, Optional

from datetime import datetime
from synthora.toolkits.base import BaseToolkit
from synthora.toolkits.decorators import tool
from synthora.types.enums import Err, Ok, Result


class WeatherToolkit(BaseToolkit):

    def __init__(self, api_key: Optional[str] = None) -> None:
        super().__init__()
        try:
            import pyowm
        except ImportError:
            raise ImportError(
                "Please install `pyowm` first. You can install it by running "
                "`pip install pyowm`."
            )
        self.api_key = api_key or os.getenv("OPENWEATHERMAP_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key for weatherapi.com not provided. Please set the WEATHER_API_KEY environment variable."
            )

    @tool
    def get_weather_data(
        self,
        city: str,
        temp_units: Literal["kelvin", "celsius", "fahrenheit"] = "kelvin",
        units: Literal["meters", "miles"] = "meters",
    ) -> Result[str, Exception]:
        r"""Fetch and return a comprehensive weather report for a given city
        as a string. The report includes current weather conditions,
        temperature, wind details, visibility, and sunrise/sunset times,
        all formatted as a readable string.

        The function interacts with the OpenWeatherMap API to
        retrieve the data.

        Args:
            city (str): The name of the city for which the weather information
                is desired. Format "City, CountryCode" (e.g., "Paris, FR"
                for Paris, France). If the country code is not provided,
                the API will search for the city in all countries, which
                may yield incorrect results if multiple cities with the
                same name exist.
            temp_units (Literal['kelvin', 'celsius', 'fahrenheit']): Units for
                temperature. (default: :obj:`kelvin`)
            units (Literal['meters', 'miles']): Units for visibility
                distance. (default: :obj:`meters`)
        """
        import pyowm

        owm = pyowm.OWM(self.api_key)
        mgr = owm.weather_manager()

        try:
            wind_units = "meters_sec" if units == "meters" else "miles_hour"
            observation = mgr.weather_at_place(city)
            weather = observation.weather
            temperature = weather.temperature(temp_units)
            wind_data = observation.weather.wind(unit=wind_units)
            visibility_distance = observation.weather.visibility_distance
            visibility = (
                str(visibility_distance)
                if units == "meters"
                else str(observation.weather.visibility(unit="miles"))
            )
            sunrise_time = datetime.fromtimestamp(
                weather.sunrise_time(timeformat="unix")
            ).strftime("%H:%M:%S")
            sunset_time = datetime.fromtimestamp(
                weather.sunset_time(timeformat="unix")
            ).strftime("%H:%M:%S")
            weather_report = (
                f"Weather in {city}: "
                f"{temperature['temp']}°{temp_units.title()}, "
                f"feels like "
                f"{temperature['feels_like']}°{temp_units.title()}. "
                f"Max temp: {temperature['temp_max']}°{temp_units.title()}, "
                f"Min temp: {temperature['temp_min']}°{temp_units.title()}. "
                f"Wind: {wind_data.get("speed")} {wind_units} at {wind_data.get("deg", "N/A")} degrees. "
                f"Visibility: {visibility} {units}. "
                f"Sunrise at {sunrise_time}, Sunset at {sunset_time}."
            )

            return Ok(weather_report)

        except Exception as e:
            return Err(e, f"An exception occurred during the search: {e}")
