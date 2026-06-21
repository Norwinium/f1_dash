import time
from datetime import datetime, timedelta
import requests
from flask import Flask, render_template, request, redirect
import helpers
import services


# 2026 Grand Prix calendar — round numbers + OpenF1 meeting keys.
GP_CALENDAR_2026 = [
    {"round": 1,  "name": "Australian GP",        "location": "Melbourne",        "meeting_key": 1279},
    {"round": 2,  "name": "Chinese GP",           "location": "Shanghai",         "meeting_key": 1280},
    {"round": 3,  "name": "Japanese GP",          "location": "Suzuka",           "meeting_key": 1281},
    {"round": 4,  "name": "Bahrain GP",           "location": "Bahrain",          "meeting_key": 1305},
    {"round": 5,  "name": "Saudi Arabian GP",     "location": "Jeddah",           "meeting_key": 1283},
    {"round": 6,  "name": "Miami GP",             "location": "Miami Gardens",    "meeting_key": 1284},
    {"round": 7,  "name": "Canadian GP",          "location": "Montréal",         "meeting_key": 1285},
    {"round": 8,  "name": "Monaco GP",            "location": "Monte Carlo",      "meeting_key": 1286},
    {"round": 9,  "name": "Barcelona GP",         "location": "Barcelona",        "meeting_key": 1287},
    {"round": 10, "name": "Austrian GP",          "location": "Spielberg",        "meeting_key": 1288},
    {"round": 11, "name": "British GP",           "location": "Silverstone",      "meeting_key": 1289},
    {"round": 12, "name": "Belgian GP",           "location": "Spa-Francorchamps","meeting_key": 1290},
    {"round": 13, "name": "Hungarian GP",         "location": "Budapest",         "meeting_key": 1291},
    {"round": 14, "name": "Dutch GP",             "location": "Zandvoort",        "meeting_key": 1292},
    {"round": 15, "name": "Italian GP",           "location": "Monza",            "meeting_key": 1293},
    {"round": 16, "name": "Spanish GP",           "location": "Madrid",           "meeting_key": 1294},
    {"round": 17, "name": "Azerbaijan GP",        "location": "Baku",             "meeting_key": 1295},
    {"round": 18, "name": "Singapore GP",         "location": "Marina Bay",       "meeting_key": 1296},
    {"round": 19, "name": "United States GP",     "location": "Austin",           "meeting_key": 1297},
    {"round": 20, "name": "Mexico City GP",       "location": "Mexico City",      "meeting_key": 1298},
    {"round": 21, "name": "São Paulo GP",         "location": "São Paulo",        "meeting_key": 1299},
    {"round": 22, "name": "Las Vegas GP",         "location": "Las Vegas",        "meeting_key": 1300},
    {"round": 23, "name": "Qatar GP",             "location": "Lusail",           "meeting_key": 1301},
    {"round": 24, "name": "Abu Dhabi GP",         "location": "Yas Marina",       "meeting_key": 1302},
]


# Build a key-indexed lookup: "australian_gp" → calendar entry
_GP_KEY_MAP = {
    gp["name"].lower().replace(" ", "_"): gp for gp in GP_CALENDAR_2026
}


app = Flask(__name__)


@app.route("/")
def index():
    """
    This code defines a route for the home page ("/") of a web application
    using the Flask framework. When a user visits the home page, the
    index() function is executed.
    """
    try:
        # The function first tries to get the current year and fetches
        # session data for that year from an external API.
        current_year = datetime.now().year
        url = f"https://api.openf1.org/v1/sessions?year={current_year}"
        all_sessions = requests.get(url, timeout=5).json()

        # It sorts the sessions by their start date.
        all_sessions.sort(key=lambda x: x['date_start'])

        # It then determines the next session and the next race session
        # that will occur after the current time.
        now_utc = datetime.utcnow().isoformat() + "Z"
        next_session = None
        next_race_session = None
        for s in all_sessions:
            if s['date_start'] > now_utc:
                if next_session is None:
                    next_session = s
                if "race" in s.get("session_name", "").lower():
                    next_race_session = s
                    break

        # If there is no upcoming race session, it uses the next session as a fallback.
        if not next_race_session:
            next_race_session = next_session

        # If there are no upcoming sessions, it uses the last session in the list as a fallback.
        if not next_session and all_sessions:
            next_session = all_sessions[-1]
        if not next_race_session and all_sessions:
            next_race_session = all_sessions[-1]

        # The function then initializes variables for weather data, circuit data, and strategy statistics.
        weather_data = None
        circuit_data = None
        strategy_stats = None

        # If there is a next race session, it fetches circuit details and strategy statistics for the session's location.
        if next_race_session:
            circuit_data = services.get_circuit_details(next_race_session.get("meeting_key"))
            location_name = helpers.clean_location_string(next_race_session.get("location"))

            # Seed our baseline fallback directly
            strategy_stats = helpers.TRACK_STRATEGY_STATS.get(location_name) or helpers.TRACK_STRATEGY_STATS["default"]

            # Attach IANA timezone so JS can display Summer Time / Winter Time label
            if circuit_data:
                gp_name = next((gp["name"] for gp in GP_CALENDAR_2026 if gp["meeting_key"] == next_race_session.get("meeting_key")), None)
                circuit_data["timezone"] = helpers.CIRCUIT_TIMEZONES.get(gp_name, "UTC")

            # If the location has known coordinates, it fetches weather data for the days leading up to the session.
            if location_name in helpers.CIRCUIT_COORDINATES:
                coords = helpers.CIRCUIT_COORDINATES[location_name]
                session_date_str = next_race_session['date_start'][:10]
                session_date = datetime.strptime(session_date_str, "%Y-%m-%d")

                start_date = session_date - timedelta(days=2)
                start_date_str = start_date.strftime("%Y-%m-%d")

                weather_data = services.get_weather_forecast(
                    coords["lat"],
                    coords["lon"],
                    start_date_str=start_date_str,
                    end_date_str=session_date_str
                )

        # Finally, the function renders the "index.html" template, passing in the session,
        # next session, weather data, circuit data, and strategy statistics as context variables.
        return render_template(
            "index.html",
            session=next_race_session,
            next_session=next_session,
            weather=weather_data,
            circuit=circuit_data,
            strategy=strategy_stats
        )
    except Exception as e:
        # If any errors occur during this process, the function prints an error message
        # and renders the template with empty context variables.
        print(f"Global backend fault: {e}")
        return render_template("index.html", session=None, weather=None, circuit=None, strategy=None)




@app.route("/Results")
def results_center():
    """
    Defines a Flask route for the URL "/Results". When a user visits this URL,
    the results_center function is executed.
    """
    try:
        # It gets the current year and retrieves a list of season meetings.
        current_year = datetime.now().year
        season_meetings = services.get_season_meetings()

        # It checks if the user has selected a specific round or session using query parameters.
        selected_round = request.args.get("round")
        selected_key = request.args.get("session")

        all_sessions = None
        weekend_sessions = []

        # INCREASED ROBUSTNESS: We loop the entire collection matrix
        # to guarantee the specific header data array populates successfully.
        # It tries to fetch session data from an external API, retrying up to five times if there are errors.
        max_retries = 5
        retry_delay = 2.0  # Gives OpenF1 two full seconds to clear concurrent database blocks

        for attempt in range(max_retries):
            try:
                of1_url = f"https://api.openf1.org/v1/sessions?year={current_year}"
                response = requests.get(of1_url, timeout=12)

                if response.status_code == 200:
                    temp_sessions = response.json()

                    if isinstance(temp_sessions, list) and len(temp_sessions) > 0:
                        temp_sessions.sort(key=lambda x: x['date_start'])
                        now_utc = datetime.utcnow().isoformat() + "Z"

                        # It processes the session data to find sessions that have already happened.
                        past_sessions = [s for s in temp_sessions if s.get('date_start', '') < now_utc]

                        if past_sessions:
                            # If a round is selected, it finds the sessions for that round.
                            if selected_round:
                                # Process selected round matching
                                selected_meeting = next(
                                    (m for m in season_meetings if str(m["round"]) == str(selected_round)), None
                                )

                                if selected_meeting:
                                    race_date = selected_meeting["date"]
                                    race_dt = datetime.strptime(race_date, "%Y-%m-%d")
                                    window_start = (race_dt - timedelta(days=5)).isoformat() + "Z"
                                    window_end = (race_dt + timedelta(days=1)).isoformat() + "Z"

                                    sessions_in_window = [
                                        s for s in past_sessions
                                        if window_start <= s.get("date_start", "") <= window_end
                                    ]

                                    if sessions_in_window:
                                        target_meeting_key = sessions_in_window[0].get("meeting_key")
                                        weekend_sessions = [
                                            s for s in past_sessions
                                            if s.get("meeting_key") == target_meeting_key
                                        ]
                            # If not, it defaults to the most recent session.
                            else:
                                # Process default fallback matching
                                latest_meeting_key = past_sessions[-1].get("meeting_key")
                                weekend_sessions = [
                                    s for s in past_sessions
                                    if s.get("meeting_key") == latest_meeting_key
                                ]

                # VALIDATION CHECKPOINT: Did we successfully parse and populate our target header list?
                if weekend_sessions and len(weekend_sessions) > 0:
                    # Success state reached
                    all_sessions = temp_sessions
                    break

                print(f"Header resolution warning: weekend_sessions unpopulated. Retrying data pull (Attempt {attempt + 1}/{max_retries})...")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)

            except (requests.exceptions.RequestException, ValueError) as err:
                print(f"OpenF1 connection warning (Attempt {attempt + 1}/{max_retries}): {err}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise err

        # Safe fallback check if everything failed after max retries
        if not all_sessions or not weekend_sessions:
            return render_template("results.html", weekend_sessions=[], current_session=None,
                                   results=[], season_meetings=season_meetings, selected_round=selected_round)

        # It sorts the sessions by date
        weekend_sessions.sort(key=lambda x: x['date_start'])

        # It determines the current session based on the selected session or defaults to the last session of the weekend.
        current_session = None
        if selected_key:
            for s in weekend_sessions:
                if str(s.get("session_key")) == str(selected_key):
                    current_session = s
                    break
        if not current_session and weekend_sessions:
            current_session = weekend_sessions[-1]

        # It retrieves the results for the current session.
        grid_results = []
        if current_session:
            grid_results = services.get_complete_session_results(
                current_session.get("session_key"),
                current_session.get("session_name")
            )

        # It renders the "results.html" template, passing in the relevant data for display.
        return render_template(
            "results.html",
            weekend_sessions=weekend_sessions,
            current_session=current_session,
            results=grid_results,
            session=current_session,
            circuit=services.get_circuit_details(current_session.get("meeting_key")) if current_session else None,
            season_meetings=season_meetings,
            selected_round=selected_round
        )

    # If there are any errors, it prints an error message and renders the template with empty data.
    except Exception as e:
        print(f"Server-Side results component fault: {e}")
        return render_template("results.html", weekend_sessions=[], current_session=None,
                               results=[], season_meetings=[], selected_round=None)


@app.route('/Standings')
def standings_page():
    """
    This code defines a route in a Flask web application for the URL path /Standings.
    When a user visits this page, the function standings_page() is executed.
    """
    try:
        # The function first checks if the user has specified a particular view
        # (either 'drivers' or 'constructors') through the URL query parameters.
        # If not, it defaults to 'drivers'.
        current_view = request.args.get('view', 'drivers').lower()

        # If the user specifies an invalid view, it also defaults to 'drivers'.
        if current_view not in ['drivers', 'constructors']:
            current_view = 'drivers'

        # Depending on the selected view, the function fetches the appropriate
        # standings data by calling either services.get_constructor_standings()
        # or services.get_championship_standings().
        if current_view == 'constructors':
            standings_board = services.get_constructor_standings()
        else:
            standings_board = services.get_championship_standings()

        # Finally, the function renders the standings.html template,
        # passing the standings data and the current view as context variables.
        return render_template(
            'standings.html',
            standings=standings_board,
            current_view=current_view
        )

    except Exception as e:
        # If an error occurs, it prints an error message and renders the
        # template with an empty standings list and the default view.
        print(f"Server-Side standings component fault: {e}")
        return render_template("standings.html", standings=[], current_view='drivers')



@app.route("/TrackStats")
def track_stats():
    """
    This code defines a route in a Flask web application that handles requests to the
    "/TrackStats" URL. When a user visits this URL, the function track_stats() is called.
    """
    # First, the function creates a list of Grand Prix (GP) events from a calendar for the year 2026.
    # Each GP is represented as a dictionary with a key, round number, and name.
    gp_list = [
        {"key": gp["name"].lower().replace(" ", "_"), "round": gp["round"], "name": gp["name"]}
        for gp in GP_CALENDAR_2026
    ]

    # Next, the function checks if a specific GP has been selected by the user through a query parameter in the URL.
    selected_key = request.args.get("gp", "").strip()
    selected_entry = _GP_KEY_MAP.get(selected_key)

    track = None
    circuit_data = None
    strategy_stats = None

    # If a GP is selected, the function retrieves details about the track, static circuit data,
    # and historical strategy statistics for that GP.
    if selected_entry:
        # ── Live circuit details from OpenF1 ──────────────────────────
        track = services.get_circuit_details(selected_entry["meeting_key"])

        # Fallback: build a minimal track object from the calendar if API is slow
        if not track:
            track = {
                "official_name": selected_entry["name"],
                "circuit_name": selected_entry["location"],
                "flag_url": None,
                "circuit_map": None,
                "gmt_offset": None,
            }

        # ── Static circuit data from helpers.CIRCUIT_DATA ─────────────
        circuit_data = helpers.CIRCUIT_DATA.get(selected_entry["name"])

        # ── Historical strategy stats from helpers.TRACK_STRATEGY_STATS ─
        clean_loc = helpers.clean_location_string(selected_entry["location"])
        strategy_stats = helpers.TRACK_STRATEGY_STATS.get(clean_loc)

    # Finally, the function renders an HTML template called "track_stats.html" and passes the relevant data
    # to the template for display. This includes the list of GPs, the selected GP, track details,
    # circuit data, and strategy statistics.
    return render_template(
        "track_stats.html",
        gp_list=gp_list,
        selected_gp=selected_key,
        track=track,
        circuit_data=circuit_data,
        strategy_stats=strategy_stats,
        # Pass a dummy session/circuit for the layout.html hero block
        current_session=None,
        circuit=track,
        session=None,
    )


if __name__ == "__main__":
    services.populate_driver_cache()
    app.run(debug=True)
