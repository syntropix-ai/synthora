# LICENSE HEADER MANAGED BY add-license-header
#
# Copyright 2024-2025 Syntropix
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
from datetime import datetime
from typing import Literal, Optional

from synthora.toolkits.base import BaseToolkit
from synthora.toolkits.decorators import tool
from synthora.types.enums import Err, Ok, Result


class WeatherToolkit(BaseToolkit):
    r"""A toolkit for fetching weather data"""

    def __init__(self, api_key: Optional[str] = None) -> None:
        super().__init__()
        self.api_key = api_key or os.getenv("OPENWEATHERMAP_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key for weatherapi.com not provided."
                + "Please set the WEATHER_API_KEY environment variable."
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
        try:
            import pyowm

            owm = pyowm.OWM(self.api_key)
            mgr = owm.weather_manager()

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
                f"Wind: {wind_data.get("speed")} {wind_units} "
                f"at {wind_data.get("deg", "N/A")} degrees. "
                f"Visibility: {visibility} {units}. "
                f"Sunrise at {sunrise_time}, Sunset at {sunset_time}."
            )

            return Ok(weather_report)
        except ImportError:
            raise ImportError(
                "Please install `pyowm` first. You can install it by running "
                "`pip install pyowm`."
            )
        except Exception as e:
            return Err(e, f"An exception occurred during the search: {e}")
