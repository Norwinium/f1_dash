"""
External API integration layer for the F1 dashboard app.

Wraps OpenF1 (live session/driver/lap data), Open-Meteo (weather), and
Jolpica / Ergast mirror (championship standings + season calendar).
"""
import time
from datetime import datetime, timedelta
import requests

import helpers


# The function populate_driver_cache() fetches a list of driver profiles
# from a specified URL using an HTTP GET request.
def populate_driver_cache():
    """Fetches all global driver profiles to eliminate real-time API bottlenecks."""
    try:
        url = "https://api.openf1.org/v1/drivers"
        response = requests.get(url, timeout=6)

        # If the request is successful, it processes the list of drivers
        # and creates a cache dictionary.
        if response.status_code == 200:
            drivers_list = response.json()
            cache = {}

            # Each driver is stored in the cache with their driver number as the key
            # and a dictionary containing their name, team, and team color as the value.
            for driver in drivers_list:
                num = str(driver.get("driver_number"))
                cache[num] = {
                    "name": driver.get("broadcast_name") or driver.get("full_name") or f"Driver #{num}",
                    "team": driver.get("team_name") or "Independent",
                    "color": driver.get("team_colour") or "6B7280"
                }

            # The cache is then assigned to a global variable DRIVER_CACHE
            # in the helpers module.
            helpers.DRIVER_CACHE = cache
            print(f"🏎️ Driver Cache successfully initialized with {len(helpers.DRIVER_CACHE)} records.")

    except Exception as e:
        # If any error occurs during this process, an error message is printed.
        print(f"⚠️ Warning: Driver Cache initialization failed: {e}")


# This code defines a function called get_weather_forecast that retrieves weather forecast data from the Open-Meteo API.
# The function takes four parameters: latitude (lat), longitude (lon), start date (start_date_str), and end date (end_date_str).
def get_weather_forecast(lat, lon, start_date_str, end_date_str):
    """Fetch standard weather forecast using Open-Meteo API."""

    # The function tries to fetch the weather data up to three times in case of a timeout.
    for attempt in range(3):
        try:
            # It constructs a URL for the API request using the provided parameters and sends a GET request to the API.
            weather_url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}&"
                f"start_date={start_date_str}&end_date={end_date_str}&"
                f"daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode&"
                f"timezone=auto"
            )
            response = requests.get(weather_url, timeout=5)
            response.raise_for_status()  # Check for HTTP errors

            # If the request is successful, it processes the JSON response to extract daily weather data
            # such as maximum and minimum temperatures, precipitation probability, and weather codes.
            data = response.json()

            # The weather codes are mapped to descriptive strings using a dictionary.
            code_map = {
                0: "☀️ Clear", 1: "🌤️ Mostly Clear", 2: "⛅ Partly Cloudy",
                3: "☁️ Overcast", 45: "🌫️ Foggy", 51: "🌦️ Drizzle",
                61: "🌧️ Light Rain", 63: "🌧️ Rain", 80: "🌦️ Showers"
            }

            # The function then creates a list of dictionaries, each representing the weather forecast for a specific day,
            # including the date, maximum and minimum temperatures, precipitation probability, and weather condition.
            forecast_list = []
            daily = data.get("daily", {})
            times = daily.get("time", [])

            # Safely extract standard API daily arrays
            temp_maxes = daily.get("temperature_2m_max", [])
            temp_mins = daily.get("temperature_2m_min", [])
            rain_probs = daily.get("precipitation_probability_max", [])
            w_codes = daily.get("weathercode", [])

            # Loop through each day in the response
            for i in range(len(times)):
                # Fallback to defaults if array sizes mismatch for any reason
                max_temp = temp_maxes[i] if i < len(temp_maxes) else 0
                min_temp = temp_mins[i] if i < len(temp_mins) else 0
                rain_prob = rain_probs[i] if i < len(rain_probs) else 0
                w_code = w_codes[i] if i < len(w_codes) else 0

                condition = code_map.get(w_code, "⛅ Variable")

                raw_date = datetime.strptime(times[i], "%Y-%m-%d")
                formatted_date = raw_date.strftime("%a, %b %d")

                forecast_list.append({
                    "date": formatted_date,
                    "max_temp": round(max_temp) if max_temp is not None else None,
                    "min_temp": round(min_temp) if min_temp is not None else None,
                    "rain_prob": int(rain_prob) if rain_prob is not None else 0,
                    "condition": condition
                })

            # If the data is successfully loaded, the function prints a message and returns the list of forecasts.
            print(f"✅ Weather forecast loaded: {len(forecast_list)} days")
            return forecast_list

        except requests.exceptions.Timeout:
            print(f"Weather API timed out on attempt {attempt + 1}... retrying.")
            continue
        except Exception as e:
            print(f"Weather forecast error: {e}")
            # If there is an error... the function returns None.
            return None

    # ...or the request times out three times, the function returns None.
    return None


# This code defines a function called get_circuit_details
# that takes a parameter called meeting_key.
def get_circuit_details(meeting_key):
    # The function tries to fetch circuit details...
    try:
        # ...from a URL that includes the meeting_key.
        url = f"https://api.openf1.org/v1/meetings?meeting_key={meeting_key}"

        # It sends a GET request to the URL and expects a JSON response.
        res = requests.get(url, timeout=4).json()

        # If the response is a list, it extracts the first item...
        if res and isinstance(res, list):
            track_info = res[0]

            # ...and retrieves specific details about the circuit, such as the official name,
            # circuit name, type, GMT offset, flag URL, and circuit map.
            # If any of these details are missing, it uses default values.
            return {
                "official_name": track_info.get("meeting_official_name", "Grand Prix"),
                "circuit_name": track_info.get("circuit_short_name", "Grand Prix Circuit"),
                "type": track_info.get("circuit_type", "Permanent Facility"),
                "gmt_offset": track_info.get("gmt_offset", "+00:00"),
                "flag_url": track_info.get("country_flag"),
                "circuit_map": track_info.get("circuit_image")
            }

    # If there is an error during this process, it prints an error message...
    except Exception as e:
        print(f"Circuit detail extraction failure: {e}")

    # ...and returns None.
    return None


# This code defines a function called get_complete_session_results that takes in a session_key and an optional session_name.
# The function retrieves and processes data from three different URLs (drivers, laps, and pits) using the session_key.
# It then processes the data to generate a list of results for each driver in the session.
def get_complete_session_results(session_key, session_name=""):
    """Generates classification metrics using the raw OpenF1 laps table maps."""
    try:
        # The function first retrieves the list of drivers and creates a mapping of
        # driver numbers to their names, teams, and team colors.
        dr_url = f"https://api.openf1.org/v1/drivers?session_key={session_key}"
        drivers_resp = requests.get(dr_url, timeout=5).json()
        drivers_list = drivers_resp if isinstance(drivers_resp, list) else []
        driver_map = {
            int(d['driver_number']): {
                'name': d.get('broadcast_name', d.get('last_name', 'Unknown')),
                'team': d.get('team_name', 'Independent'),
                'color': f"#{d.get('team_colour', '6B7280')}"
            } for d in drivers_list if isinstance(d, dict) and 'driver_number' in d
        }

        # It then retrieves the list of laps and processes the data to create a mapping
        # of driver numbers to their lap durations, maximum lap numbers, and compounds used.
        laps_url = f"https://api.openf1.org/v1/laps?session_key={session_key}"
        laps_resp = requests.get(laps_url, timeout=10).json()
        laps_data = laps_resp if isinstance(laps_resp, list) else []

        is_race = any(x in session_name.upper() for x in ["RACE", "SPRINT"])

        driver_laps = {}
        for lap in laps_data:
            if not isinstance(lap, dict):
                continue
            d_num = lap.get('driver_number')
            duration = lap.get('lap_duration')
            lap_num = lap.get('lap_number', 0)
            compound = lap.get('compound', None)
            if d_num is None:
                continue
            if d_num not in driver_laps:
                driver_laps[d_num] = {'durations': [], 'max_lap': 0, 'compounds': []}
            if duration is not None:
                driver_laps[d_num]['durations'].append(float(duration))
            if lap_num:
                driver_laps[d_num]['max_lap'] = max(driver_laps[d_num]['max_lap'], int(lap_num))
            if compound:
                driver_laps[d_num]['compounds'].append(compound.upper())

        # Next, it retrieves the list of pit stops and creates mappings of driver
        # numbers to their total pit stop times and number of pit stops.
        pits_url = f"https://api.openf1.org/v1/pit?session_key={session_key}"
        pits_resp = requests.get(pits_url, timeout=5).json()
        pits_data = pits_resp if isinstance(pits_resp, list) else []

        pit_time_map = {}
        pit_count_map = {}
        for pit in pits_data:
            if not isinstance(pit, dict):
                continue
            d_num = pit.get('driver_number')
            pit_duration = pit.get('pit_duration')
            if d_num is None:
                continue
            pit_count_map[d_num] = pit_count_map.get(d_num, 0) + 1
            if pit_duration is not None:
                pit_time_map[d_num] = pit_time_map.get(d_num, 0.0) + float(pit_duration)

        all_lap_counts = [info['max_lap'] for info in driver_laps.values() if info['durations']]
        race_lap_count = max(all_lap_counts) if all_lap_counts else 0
        dnf_threshold = race_lap_count * 0.90 if is_race else 0

        compound_colors = {
            'SOFT': 'text-red-400',
            'MEDIUM': 'text-yellow-400',
            'HARD': 'text-gray-300',
            'INTERMEDIATE': 'text-green-400',
            'WET': 'text-blue-400',
        }

        # The function then processes the data to generate a list of results for each driver,
        # including their best lap time, total time, number of laps completed, number of pit stops,
        # compounds used, and whether they did not finish (DNF) the race.
        processed_results = []
        for d_num, lap_info in driver_laps.items():
            durations = lap_info['durations']
            if not durations:
                continue
            meta = driver_map.get(int(d_num), {'name': f"Driver {d_num}", 'team': 'N/A', 'color': '#6B7280'})

            seen_compounds = []
            for c in lap_info['compounds']:
                if not seen_compounds or seen_compounds[-1] != c:
                    seen_compounds.append(c)

            laps_done = lap_info['max_lap']
            is_dnf = is_race and dnf_threshold > 0 and laps_done < dnf_threshold

            entry = {
                'driver_num': d_num,
                'driver': meta['name'],
                'team': meta['team'],
                'team_color': meta['color'],
                'best_lap_raw': min(durations),
                'total_time': sum(durations) + pit_time_map.get(d_num, 0.0),
                'laps_completed': laps_done,
                'pit_stops': pit_count_map.get(d_num, 0),
                'compounds': seen_compounds,
                'is_dnf': is_dnf,
                'compound_badges': [
                    {'label': c, 'css': compound_colors.get(c, 'text-gray-400')}
                    for c in seen_compounds
                ]
            }
            processed_results.append(entry)

        # The results are sorted based on the session type (race or non-race)
        # and additional information such as position and gap to the leader is added.
        if is_race:
            finishers = [r for r in processed_results if not r['is_dnf']]
            dnfs = [r for r in processed_results if r['is_dnf']]
            finishers.sort(key=lambda x: (-x['laps_completed'], x['total_time']))
            dnfs.sort(key=lambda x: -x['laps_completed'])
            processed_results = finishers + dnfs
        else:
            processed_results.sort(key=lambda x: x['best_lap_raw'])

        if not processed_results:
            return []

        leader = processed_results[0]

        for index, item in enumerate(processed_results, start=1):
            raw_time = item['best_lap_raw']
            minutes = int(raw_time // 60)
            seconds = raw_time % 60
            item['time_str'] = f"{minutes}:{seconds:06.3f}" if minutes > 0 else f"{seconds:.3f}"

            if item['is_dnf']:
                item['pos'] = 'DNF'
                item['gap_str'] = f"DNF · L{item['laps_completed']}"
            elif index == 1:
                item['pos'] = 1
                item['gap_str'] = "LEADER"
            elif is_race:
                item['pos'] = index
                laps_down = leader['laps_completed'] - item['laps_completed']
                if laps_down > 0:
                    item['gap_str'] = f"+{laps_down} LAP{'S' if laps_down > 1 else ''}"
                else:
                    gap = item['total_time'] - leader['total_time']
                    item['gap_str'] = f"+{gap:.3f}s"
            else:
                item['pos'] = index
                gap = raw_time - leader['best_lap_raw']
                item['gap_str'] = f"+{gap:.3f}s"

        # Finally, the function returns the list of processed results.
        return processed_results

    # If any errors occur during the process, the function prints an error message and returns an empty list.
    except Exception as e:
        print(f"Error computing session results matrix: {e}")
        return []


# This code defines a function called get_championship_standings.
# The function fetches constructor standings data from an external API, processes the data, and returns it in a specific format.
def get_championship_standings():
    """Fetches high-reliability, pre-calculated seasonal standings via Jolpica (Ergast Mirror)."""
    try:
        # The function gets the current year using datetime.now().year.
        current_year = datetime.now().year

        # It constructs a URL using the current year to fetch the driver standings.
        url = f"https://api.jolpi.ca/ergast/f1/{current_year}/driverStandings.json"

        # It sends a GET request to the URL...
        response = requests.get(url, timeout=2.5)

        # ...and checks if the response status code is 200 (OK). If not, it prints a warning and returns an empty list.
        if response.status_code != 200:
            print(f"⚠️ Jolpica API responded with status code: {response.status_code}")
            return []

        # It parses the JSON response and navigates through the nested dictionaries to get the list of driver standings.
        data = response.json()
        standings_lists = data.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
        if not standings_lists:
            return []

        driver_standings = standings_lists[0].get("DriverStandings", [])

        # It appends each processed driver’s data to a list called processed_board.
        # (Initializing the list here before processing the drivers)
        processed_board = []

        # Color palette directory matching Ergast data objects back to layouts
        constructors_hex = {
            "ferrari": "#E80020", "mercedes": "#27F4D2", "red_bull": "#3671C6",
            "mclaren": "#FF8000", "aston_martin": "#229971", "alpine": "#0093CC",
            "sauber": "#52E252", "haas": "#B6BABD", "williams": "#37BEDD", "rb": "#6692FF",
            "kick_sauber": "#52E252", "racing_bulls": "#6692FF"
        }

        # It processes each driver’s data, extracting the position, driver name, team name, team color, and points.
        for row in driver_standings:
            driver_data = row.get("Driver", {})
            constructors = row.get("Constructors", [{}])
            c_id = constructors[0].get("constructorId", "")

            processed_board.append({
                "pos": int(row.get("position")),
                "driver": f"{driver_data.get('givenName', '')} {driver_data.get('familyName', '')}".strip(),
                "team": constructors[0].get("name", "Independent"),
                "team_color": constructors_hex.get(c_id, "#6B7280"),
                "points": float(row.get("points", 0))
            })

        # Finally, it returns the processed_board list.
        return processed_board

    except Exception as e:
        # If any error occurs during the process, it prints an error message and returns an empty list.
        print(f"Error parsing Ergast standings grid components: {e}")
        return []


# This code defines a function called get_constructor_standings.
# The function fetches constructor standings data from an external API, processes the data, and returns it in a specific format.
def get_constructor_standings():
    """Fetches pre-calculated constructor standings via Jolpica (Ergast Mirror)."""
    try:
        # First, the function gets the current year and constructs a URL using this year.
        # It then sends a GET request to this URL.
        current_year = datetime.now().year
        url = f"https://api.jolpi.ca/ergast/f1/{current_year}/constructorStandings.json"
        response = requests.get(url, timeout=2.5)

        # If the request is unsuccessful, the function returns an empty list.
        if response.status_code != 200:
            print(f"⚠️ Jolpica API responded with status code: {response.status_code}")
            return []

        # If the request is successful, the function extracts the relevant data from the JSON response.
        data = response.json()
        standings_lists = data.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
        if not standings_lists:
            return []

        constructor_standings = standings_lists[0].get("ConstructorStandings", [])

        # (Helper dictionary mapping team IDs to their specific hex colors)
        constructors_hex = {
            "ferrari": "#E80020", "mercedes": "#27F4D2", "red_bull": "#3671C6",
            "mclaren": "#FF8000", "aston_martin": "#229971", "alpine": "#0093CC",
            "sauber": "#52E252", "haas": "#B6BABD", "williams": "#37BEDD", "rb": "#6692FF",
            "kick_sauber": "#52E252", "racing_bulls": "#6692FF"
        }

        # It then processes this data, creating a list of dictionaries.
        # Each dictionary contains information about a constructor, such as its position, name, color, and points.
        processed_board = []
        for row in constructor_standings:
            constructor = row.get("Constructor", {})
            c_id = constructor.get("constructorId", "")
            processed_board.append({
                "pos": int(row.get("position")),
                "driver": "",  # not used in constructor view
                "team": constructor.get("name", "Unknown"),
                "team_color": constructors_hex.get(c_id, "#6B7280"),
                "points": float(row.get("points", 0))
            })

        # The function returns this list.
        return processed_board

    # If any errors occur during this process, the function prints an error message and returns an empty list.
    except Exception as e:
        print(f"Error parsing constructor standings: {e}")
        return []


# This code defines a function called get_season_meetings.
# The function fetches data about completed race weekends for the current year from a remote server.
def get_season_meetings():
    """Fetches all completed race weekends for the current season via Jolpica."""
    try:
        # It does this by making an HTTP GET request to a specific URL, which includes the current year in its path.
        current_year = datetime.now().year
        url = f"https://api.jolpi.ca/ergast/f1/{current_year}/races.json"
        response = requests.get(url, timeout=5)

        # If the request is successful, the function processes the JSON response to extract information about each race.
        if response.status_code != 200:
            return []

        data = response.json()
        races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])

        # It checks if the race date is in the past, and if so, adds details about the race to a list called completed.
        now = datetime.utcnow()
        completed = []
        for race in races:
            race_date = race.get("date", "")
            try:
                if datetime.strptime(race_date, "%Y-%m-%d") < now:
                    completed.append({
                        "round": int(race.get("round", 0)),
                        "name": race.get("raceName", "Unknown Race"),
                        "circuit": race.get("Circuit", {}).get("circuitName", ""),
                        "date": race_date,
                    })
            except ValueError:
                continue

        # The function returns this list of completed races.
        return completed

    # If there is an error at any point, the function prints an error message and returns an empty list.
    except Exception as e:
        print(f"Error fetching season meetings: {e}")
        return []
