"""
Simple Weather Forecast Panel using the free Open-Meteo API.

- No API key required.
- Fetches current temperature for a given latitude/longitude.
- Displays a colored ASCII panel that refreshes periodically.
"""

import os
import sys
import time
from typing import Any

import requests
from colorama import Fore, Style, init


def fetch_current_weather(lat: float, lon: float) -> dict[str, Any]:
    """Fetch current weather data from the Open-Meteo API."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def wind_direction_to_arrow(degrees: float | None) -> str:
    """
    Convert a wind direction in degrees to a compass arrow and label.
    0°/360° = North, 90° = East, 180° = South, 270° = West.
    """
    if degrees is None:
        return "N/A"

    deg = degrees % 360

    if 337.5 <= deg or deg < 22.5:
        return "↑ N"
    elif 22.5 <= deg < 67.5:
        return "↗ NE"
    elif 67.5 <= deg < 112.5:
        return "→ E"
    elif 112.5 <= deg < 157.5:
        return "↘ SE"
    elif 157.5 <= deg < 202.5:
        return "↓ S"
    elif 202.5 <= deg < 247.5:
        return "↙ SW"
    elif 247.5 <= deg < 292.5:
        return "← W"
    else:
        return "↖ NW"


def format_weather_panel(
    *,
    latitude: float,
    longitude: float,
    time: str | None,
    temperature: float | None,
    windspeed: float | None,
    winddirection: float | None,
) -> str:
    """
    Return an artistic ASCII panel with the weather information, with colors.
    """

    # Fallback strings if some values are missing
    time_str = time or "N/A"
    temp_str = f"{temperature:.1f} °C" if temperature is not None else "N/A"
    windspeed_str = f"{windspeed:.1f} km/h" if windspeed is not None else "N/A"
    winddir_str = wind_direction_to_arrow(winddirection)

    # Choose color for temperature (simple example)
    if temperature is None:
        temp_color = Fore.WHITE
    elif temperature < 10:
        temp_color = Fore.CYAN
    elif temperature < 25:
        temp_color = Fore.GREEN
    else:
        temp_color = Fore.RED

    border_color = Fore.BLUE
    label_color = Fore.YELLOW
    value_color = Fore.WHITE
    title_color = Fore.MAGENTA + Style.BRIGHT
    icon_color = Fore.CYAN

    lines: list[str] = []

    title = " PAINEL METEROLÓGICO"
    title_bar = f"{border_color}╔{title:═^48}╗{Style.RESET_ALL}"
    lines.append(title_bar)

    # Location line
    loc_text = f"Location: lat={latitude:.4f}, lon={longitude:.4f}"
    loc_line = (
        f"{border_color}║ {label_color}{loc_text:<46}{border_color}║{Style.RESET_ALL}"
    )
    lines.append(loc_line)

    # Time line
    time_text = f"Time: {time_str}"
    time_line = (
        f"{border_color}║ {label_color}{time_text:<46}{border_color}║{Style.RESET_ALL}"
    )
    lines.append(time_line)

    # Separator
    lines.append(f"{border_color}╠" + "═" * 48 + f"╣{Style.RESET_ALL}")

    # Temperature
    temp_label = "Temperature"
    temp_line = (
        f"{border_color}║ {label_color}{temp_label:<15}: "
        f"{temp_color}{temp_str:<26}{border_color}║{Style.RESET_ALL}"
    )
    lines.append(temp_line)

    # Wind speed
    wind_label = "Wind Speed"
    wind_line = (
        f"{border_color}║ {label_color}{wind_label:<15}: "
        f"{value_color}{windspeed_str:<26}{border_color}║{Style.RESET_ALL}"
    )
    lines.append(wind_line)

    # Wind direction
    winddir_label = "Wind Direction"
    winddir_line = (
        f"{border_color}║ {label_color}{winddir_label:<15}: "
        f"{value_color}{winddir_str:<26}{border_color}║{Style.RESET_ALL}"
    )
    lines.append(winddir_line)

    # Icons row
    icon_row = f"{icon_color}☁  ☀  ☂  ☃  🌈{Style.RESET_ALL}"
    icon_line = (
        f"{border_color}║ "
        + icon_row.center(46)
        + f"{border_color}║{Style.RESET_ALL}"
    )
    lines.append(f"{border_color}╠" + "─" * 48 + f"╣{Style.RESET_ALL}")
    lines.append(icon_line)

    lines.append(f"{border_color}╚" + "═" * 48 + f"╝{Style.RESET_ALL}")

    # Color the title text itself
    lines[0] = lines[0].replace(
        "WEATHER FORECAST PANEL",
        f"{title_color}WEATHER FORECAST PANEL{border_color}{Style.RESET_ALL}",
    )

    return "\n".join(lines)


def clear_screen() -> None:
    """Clear the terminal screen (works on Windows and Linux)."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def run_once(latitude: float, longitude: float) -> None:
    """Fetch data once and print the panel."""
    try:
        data = fetch_current_weather(latitude, longitude)
    except requests.RequestException as exc:
        print(f"{Fore.RED}Error fetching weather data: {exc}{Style.RESET_ALL}")
        return

    current = data.get("current_weather", {})
    temperature = current.get("temperature")
    windspeed = current.get("windspeed")
    winddirection = current.get("winddirection")
    time_str = current.get("time")

    panel = format_weather_panel(
        latitude=latitude,
        longitude=longitude,
        time=time_str,
        temperature=temperature,
        windspeed=windspeed,
        winddirection=winddirection,
    )

    clear_screen()
    print(panel)
    print()
    print(f"{Fore.CYAN}Updated just now. Press Ctrl+C to exit.{Style.RESET_ALL}")


def main() -> None:
    # Initialize color handling (needed on Windows; also fine on Pi)
    init(autoreset=True)

    # Example: Sintra, Portugal
    latitude = 38.8028687
    longitude = -9.3816589

    refresh_seconds = 300  # 5 minutes; change as you like

    print(f"{Fore.CYAN}Starting Weather Panel (refresh every {refresh_seconds}s)...{Style.RESET_ALL}")
    time.sleep(1)

    try:
        while True:
            run_once(latitude, longitude)
            time.sleep(refresh_seconds)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Shutting down weather panel. Goodbye!{Style.RESET_ALL}")
        sys.exit(0)


if __name__ == "__main__":

    main()
