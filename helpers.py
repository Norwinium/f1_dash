"""
Shared constants and small, side-effect-free utility functions used across
the F1 dashboard app.
"""
import unicodedata

# Master Global Cache for Formula 1 Driver Details.
# Populated by services.populate_driver_cache() at startup.
DRIVER_CACHE = {}


# IANA timezone identifiers per circuit — used to display Summer/Winter time label in the UI.
# Keys must match the "name" field in GP_CALENDAR_2026 exactly.
CIRCUIT_TIMEZONES = {
    "Australian GP":    "Australia/Melbourne",
    "Chinese GP":       "Asia/Shanghai",
    "Japanese GP":      "Asia/Tokyo",
    "Bahrain GP":       "Asia/Bahrain",
    "Saudi Arabian GP": "Asia/Riyadh",
    "Miami GP":         "America/New_York",
    "Canadian GP":      "America/Toronto",
    "Monaco GP":        "Europe/Monaco",
    "Barcelona GP":     "Europe/Madrid",
    "Austrian GP":      "Europe/Vienna",
    "British GP":       "Europe/London",
    "Belgian GP":       "Europe/Brussels",
    "Hungarian GP":     "Europe/Budapest",
    "Dutch GP":         "Europe/Amsterdam",
    "Italian GP":       "Europe/Rome",
    "Spanish GP":       "Europe/Madrid",
    "Azerbaijan GP":    "Asia/Baku",
    "Singapore GP":     "Asia/Singapore",
    "United States GP": "America/Chicago",
    "Mexico City GP":   "America/Mexico_City",
    "São Paulo GP":     "America/Sao_Paulo",
    "Las Vegas GP":     "America/Los_Angeles",
    "Qatar GP":         "Asia/Qatar",
    "Abu Dhabi GP":     "Asia/Dubai",
}


# Track historical statistics including safety cars, tyre strategies and podiums
TRACK_STRATEGY_STATS = {
    "bahrain": {
        "safety_car": 75, "strategy": "Medium ➔ Hard (1 Stop)", "pit_loss": "23s", "vsc_pit_loss": "13s",
    },
    "jeddah": {
        "safety_car": 67, "strategy": "Soft ➔ Medium (1 Stop)", "pit_loss": "20s", "vsc_pit_loss": "10s",
    },
    "melbourne": {
        "safety_car": 50, "strategy": "Medium ➔ Hard (1 Stop)", "pit_loss": "19s", "vsc_pit_loss": "9s",
    },
    "suzuka": {
        "safety_car": 50, "strategy": "Soft ➔ Medium ➔ Soft (2 Stops)", "pit_loss": "23s", "vsc_pit_loss": "13s",
    },
    "shanghai": {
        "safety_car": 50, "strategy": "Medium ➔ Hard ➔ Medium (2 Stops)", "pit_loss": "25s", "vsc_pit_loss": "15s",
    },
    "miami gardens": {
        "safety_car": 50, "strategy": "Medium ➔ Hard (1 Stop)", "pit_loss": "21s", "vsc_pit_loss": "11s",
    },
    "monte carlo": {
        "safety_car": 36, "strategy": "Soft ➔ Hard (1 Stop)", "pit_loss": "20s", "vsc_pit_loss": "10s",
    },
    "montreal": {
        "safety_car": 60, "strategy": "Soft ➔ Hard (1 Stop)", "pit_loss": "22s", "vsc_pit_loss": "12s",
    },
    "barcelona": {
        "safety_car": 37, "strategy": "Soft ➔ Medium ➔ Soft (2 Stops)", "pit_loss": "23s", "vsc_pit_loss": "23s",
    },
    "spielberg": {
        "safety_car": 50, "strategy": "Soft ➔ Medium ➔ Soft (2 Stops)", "pit_loss": "22s", "vsc_pit_loss": "12s",
    },
    "silverstone": {
        "safety_car": 55, "strategy": "Soft ➔ Medium ➔ Soft (2 Stops)", "pit_loss": "22s", "vsc_pit_loss": "12s",
    },
    "budapest": {
        "safety_car": 34, "strategy": "Soft ➔ Medium ➔ Hard (2 Stops)", "pit_loss": "21s", "vsc_pit_loss": "11s",
    },
    "spa-francorchamps": {
        "safety_car": 63, "strategy": "Soft ➔ Medium (1 Stop)", "pit_loss": "17s", "vsc_pit_loss": "7s",
    },
    "zandvoort": {
        "safety_car": 50, "strategy": "Soft ➔ Medium ➔ Soft (2 Stops)", "pit_loss": "21s", "vsc_pit_loss": "11s",
    },
    "monza": {
        "safety_car": 47, "strategy": "Medium ➔ Hard (1 Stop)", "pit_loss": "25s", "vsc_pit_loss": "15s",
    },
    "baku": {
        "safety_car": 62, "strategy": "Medium ➔ Hard (1 Stop)", "pit_loss": "19s", "vsc_pit_loss": "9s",
    },
    "marina bay": {
        "safety_car": 67, "strategy": "Soft ➔ Medium ➔ Soft (2 Stops)", "pit_loss": "28s", "vsc_pit_loss": "18s",
    },
    "austin": {
        "safety_car": 48, "strategy": "Medium ➔ Medium ➔ Hard (2 Stops)", "pit_loss": "21s", "vsc_pit_loss": "11s",
    },
    "mexico city": {
        "safety_car": 65, "strategy": "Medium ➔ Hard (1 Stop)", "pit_loss": "25s", "vsc_pit_loss": "15s",
    },
    "sao paulo": {
        "safety_car": 53, "strategy": "Soft ➔ Medium ➔ Soft (2 Stops)", "pit_loss": "23s", "vsc_pit_loss": "13s",
    },
    "las vegas": {
        "safety_car": 50, "strategy": "Medium ➔ Hard (1 Stop)", "pit_loss": "17s", "vsc_pit_loss": "7s",
    },
    "lusail": {
        "safety_car": 57, "strategy": "Medium ➔ Hard ➔ Medium (2 Stops)", "pit_loss": "24s", "vsc_pit_loss": "14s",
    },
    "yas marina": {
        "safety_car": 44, "strategy": "Soft ➔ Hard ➔ Medium (2 Stops)", "pit_loss": "21s", "vsc_pit_loss": "11s",
    },
    "madrid": {
        "safety_car": 0, "strategy": "? ➔ ? (? Stops)", "pit_loss": "??.?s", "vsc_pit_loss": "??.?s",
    },
}


# Coordinates lookup dictionary
CIRCUIT_COORDINATES = {
    "austin": {"lat": 30.1323, "lon": -97.6411},
    "bahrain": {"lat": 26.0325, "lon": 50.5106},
    "baku": {"lat": 40.3725, "lon": 49.8533},
    "barcelona": {"lat": 41.57, "lon": 2.2611},
    "budapest": {"lat": 47.5822, "lon": 19.2511},
    "jeddah": {"lat": 21.6319, "lon": 39.1044},
    "las vegas": {"lat": 36.11, "lon": -115.1622},
    "lusail": {"lat": 25.49, "lon": 51.4542},
    "madrid": {"lat": 40.4653, "lon": -3.6153},
    "marina bay": {"lat": 1.2915, "lon": 103.8638},
    "melbourne": {"lat": -37.8497, "lon": 144.9683},
    "mexico city": {"lat": 19.4061, "lon": -99.0925},
    "miami gardens": {"lat": 25.9580, "lon": -80.2389},
    "monte carlo": {"lat": 43.7347, "lon": 7.4206},
    "montréal": {"lat": 45.5005, "lon": -73.5225},
    "monza": {"lat": 45.6205, "lon": 9.2894},
    "sakhir": {"lat": 26.0325, "lon": 50.5106},
    "shanghai": {"lat": 31.3388, "lon": 121.2197},
    "silverstone": {"lat": 52.0711, "lon": -1.0161},
    "spa-francorchamps": {"lat": 50.4372, "lon": 5.9714},
    "spielberg": {"lat": 47.2197, "lon": 14.7647},
    "suzuka": {"lat": 34.8417, "lon": 136.5389},
    "são paulo": {"lat": -23.7011, "lon": -46.6972},
    "yas marina": {"lat": 24.4672, "lon": 54.6031},
    "zandvoort": {"lat": 52.3889, "lon": 4.5408}
}


def clean_location_string(text):
    """Normalize a location string for dictionary lookups (strip accents, lowercase)."""

    # The function clean_location_string takes a string input called text
    # and returns a normalized version of it.

    # If the input is empty or None, it returns an empty string.
    if not text:
        return ""

    # Otherwise, it removes any accents from the characters...
    clean_text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

    # ...strips leading and trailing whitespace, and converts the string to lowercase.
    # This is useful for standardizing location names for dictionary lookups.
    return clean_text.strip().lower()


# ──────────────────────────────────────────────────────────────────────────
# All fields are optional — the template handles missing values
# gracefully with '—' fallbacks.
#
# Aim to update at least annually.
# Last update: dd/mm/yyyy
# ──────────────────────────────────────────────────────────────────────────

CIRCUIT_DATA = {

    # KEY must match the "name" field in GP_CALENDAR_2026 exactly.
    "Australian GP": {
        "first_gp": 1996,               # int  — year of first F1 race here
        "laps": 58,                     # int  — scheduled race laps
        "length_km": 5.278,             # float — circuit length in km (miles auto-calculated)
        "lap_record": "1:19.813 (C. Leclerc, 2024)",  # str

        # Narrative expected strategy shown in the Strategy section.
        # Leave absent to fall back to TRACK_STRATEGY_STATS.strategy.
        "option_strategy": "1-Stop (Medium → Hard)",  # str
        "alternate_strategy": "1-Stop (Soft → Hard)",
        "alternate_strategy_2": "2-Stop (Soft → Hard → Medium)",

        # Compound performance windows — list of dicts, one per compound used.
        # optimal_laps: realistic competitive window before degradation cliff.
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 19, "max_laps": 33},
            {"name": "MEDIUM", "optimal_laps": 25, "max_laps": 44},
            {"name": "HARD",   "optimal_laps": 34, "max_laps": 61},
        ],

        # Time lost per lap due to tyre degradation (in seconds).
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.10},
            {"name": "MEDIUM", "loss_s": 0.07},
            {"name": "HARD",   "loss_s": 0.05},
        ],
    },

    "Chinese GP": {
        "first_gp": 2004,
        "laps": 56,
        "length_km": 5.451,
        "lap_record": "1:32.238 (M. Schumacher, 2004)",
        "option_strategy": "2-Stop (Medium → Hard → Medium)",
        "alternate_strategy": "2-Stop (Medium → Hard → Hard)",
        "alternate_strategy_2": "2-Stop (Soft → Hard → Hard)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 20, "max_laps": 35},
            {"name": "MEDIUM", "optimal_laps": 27, "max_laps": 48},
            {"name": "HARD",   "optimal_laps": 38, "max_laps": 68},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.11},
            {"name": "MEDIUM", "loss_s": 0.08},
            {"name": "HARD",   "loss_s": 0.05},
        ],
    },

    "Japanese GP": {
        "first_gp": 1987,
        "laps": 53,
        "length_km": 5.807,
        "lap_record": "1:30.965 (A. Antonelli, 2025)",
        "option_strategy": "2-Stop (Soft → Medium → Soft)",
        "alternate_strategy": "2-Stop (Soft → Soft → Medium)",
        "alternate_strategy_2": "1-Stop (Soft → Hard)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 20, "max_laps": 35},
            {"name": "MEDIUM", "optimal_laps": 28, "max_laps": 49},
            {"name": "HARD",   "optimal_laps": 32, "max_laps": 57},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.09},
            {"name": "MEDIUM", "loss_s": 0.06},
            {"name": "HARD",   "loss_s": 0.05},
        ],
    },

    "Bahrain GP": {
        "first_gp": 2004,
        "laps": 57,
        "length_km": 5.412,
        "lap_record": "1:31.447 (P. de la Rosa, 2005)",
        "option_strategy": "2-Stop (Soft → Soft → Medium)",
        "alternate_strategy": "2-Stop (Medium → Soft → Soft)",
        "alternate_strategy_2": "2-Stop (Soft → Medium → Soft)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 27, "max_laps": 47},
            {"name": "MEDIUM", "optimal_laps": 37, "max_laps": 66},
            {"name": "HARD",   "optimal_laps": 43, "max_laps": 77},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.09},
            {"name": "MEDIUM", "loss_s": 0.06},
            {"name": "HARD",   "loss_s": 0.05},
        ],
    },

    "Saudi Arabian GP": {
        "first_gp": 2021,
        "laps": 50,
        "length_km": 6.174,
        "lap_record": "1:30.734 (L. Hamilton, 2021)",
        "option_strategy": "1-Stop (Soft → Medium)",
        "alternate_strategy": "1-Stop (Medium → Soft)",
        "alternate_strategy_2": "1-Stop (Soft → Hard)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 24, "max_laps": 42},
            {"name": "MEDIUM", "optimal_laps": 33, "max_laps": 58},
            {"name": "HARD",   "optimal_laps": 46, "max_laps": 81},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.08},
            {"name": "MEDIUM", "loss_s": 0.05},
            {"name": "HARD",   "loss_s": 0.04},
        ],
    },

    "Miami GP": {
        "first_gp": 2022,
        "laps": 57,
        "length_km": 5.412,
        "lap_record": "1:29.708 (M. Verstappen, 2023)",
        "option_strategy": "1-Stop (Medium → Hard)",
        "alternate_strategy": "2-Stop (Soft → Medium → Soft)",
        "alternate_strategy_2": "1-Stop (Hard → Medium)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 23, "max_laps": 40},
            {"name": "MEDIUM", "optimal_laps": 32, "max_laps": 56},
            {"name": "HARD",   "optimal_laps": 44, "max_laps": 78},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.09},
            {"name": "MEDIUM", "loss_s": 0.06},
            {"name": "HARD",   "loss_s": 0.04},
        ],
    },

    "Canadian GP": {
        "first_gp": 1978,
        "laps": 70,
        "length_km": 4.361,
        "lap_record": "1:13.078 (V. Bottas, 2019)",
        "option_strategy": "1-Stop (Soft → Hard)",
        "alternate_strategy": "1-Stop (Medium → Hard)",
        "alternate_strategy_2": "2-Stop (Soft → Hard → Soft)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 35, "max_laps": 61},
            {"name": "MEDIUM", "optimal_laps": 47, "max_laps": 82},
            {"name": "HARD",   "optimal_laps": 64, "max_laps": 113},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.05},
            {"name": "MEDIUM", "loss_s": 0.04},
            {"name": "HARD",   "loss_s": 0.02},
        ],
    },

    "Monaco GP": {
        "first_gp": 1950,
        "laps": 78,
        "length_km": 3.337,
        "lap_record": "1:12.909 (L. Hamilton, 2021)",
        "option_strategy": "1-Stop (Soft → Hard)",
        "alternate_strategy": "1-Stop (Medium → Hard)",
        "alternate_strategy_2": "1-Stop (Hard → Medium)",
        # Below fix doesn't bypass API image request successfully
        # "circuit_map_url": "https://www.pngkey.com/png/detail/217-2174998_circuit-de-monaco-2018-fia-formula-one-world.png",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 29, "max_laps": 52},
            {"name": "MEDIUM", "optimal_laps": 39, "max_laps": 69},
            {"name": "HARD",   "optimal_laps": 54, "max_laps": 95},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.06},
            {"name": "MEDIUM", "loss_s": 0.05},
            {"name": "HARD",   "loss_s": 0.03},
        ],
    },

    "Barcelona GP": {
        "first_gp": 1991,
        "laps": 66,
        "length_km": 4.657,
        "lap_record": "1:15.743 (O. Piastri, 2025)",
        "option_strategy": "2-Stop (Soft → Medium → Soft)",
        "alternate_strategy": "2-Stop (Soft → Hard → Medium)",
        "alternate_strategy_2": "2-Stop (Soft → Hard → Soft)",
        # Below fix doesn't bypass API image request successfully
        # "circuit_map_url": "https://media.formula1.com/image/upload/f_auto,c_limit,w_1440,q_auto/f_auto/q_auto/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Spain%20carbon",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 19, "max_laps": 33},
            {"name": "MEDIUM", "optimal_laps": 26, "max_laps": 46},
            {"name": "HARD",   "optimal_laps": 30, "max_laps": 54},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.09},
            {"name": "MEDIUM", "loss_s": 0.06},
            {"name": "HARD",   "loss_s": 0.05},
        ],
    },

    "Austrian GP": {
        "first_gp": 1970,
        "laps": 71,
        "length_km": 4.326,
        "lap_record": "1:07.924 (O. Piastri, 2025)",
        "option_strategy": "2-Stop (Soft → Medium → Soft)",
        "alternate_strategy": "1-Stop (Medium → Hard)",
        "alternate_strategy_2": "2-Stop (Medium → Hard → Medium)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 12, "max_laps": 38},
            {"name": "MEDIUM", "optimal_laps": 29, "max_laps": 51},
            {"name": "HARD",   "optimal_laps": 40, "max_laps": 70},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.07},
            {"name": "MEDIUM", "loss_s": 0.05},
            {"name": "HARD",   "loss_s": 0.04},
        ],
    },

    "British GP": {
        "first_gp": 1950,
        "laps": 52,
        "length_km": 5.891,
        "lap_record": "1:27.097 (M. Verstappen, 2020)",
        "option_strategy": "2-Stop (Soft → Medium → Soft)",
        "alternate_strategy": "1-Stop (Medium → Hard)",
        "alternate_strategy_2": "2-Stop (Soft → Soft → Medium)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 18, "max_laps": 32},
            {"name": "MEDIUM", "optimal_laps": 25, "max_laps": 45},
            {"name": "HARD",   "optimal_laps": 30, "max_laps": 52},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.09},
            {"name": "MEDIUM", "loss_s": 0.06},
            {"name": "HARD",   "loss_s": 0.05},
        ],
    },

    "Belgian GP": {
        "first_gp": 1950,
        "laps": 44,
        "length_km": 7.0004,
        "lap_record": "1:44.701 (S. Perez, 2024)",
        "option_strategy": "1-Stop (Soft → Medium)",
        "alternate_strategy": "2-Stop (Soft → Medium → Soft)",
        "alternate_strategy_2": "1-Stop (Medium → Hard)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 22, "max_laps": 38},
            {"name": "MEDIUM", "optimal_laps": 30, "max_laps": 53},
            {"name": "HARD",   "optimal_laps": 42, "max_laps": 74},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.10},
            {"name": "MEDIUM", "loss_s": 0.07},
            {"name": "HARD",   "loss_s": 0.04},
        ],
    },

    "Hungarian GP": {
        "first_gp": 1986,
        "laps": 70,
        "length_km": 4.381,
        "lap_record": "1:16.627 (L. Hamilton, 2020)",
        "option_strategy": "2-Stop (Soft → Medium → Hard)",
        "alternate_strategy": "2-Stop (Medium → Hard → Soft)",
        "alternate_strategy_2": "2-Stop (Soft → Hard → Soft)",
        # Below fix doesn't bypass API image request successfully
        # "circuit_map_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Hungaroring.svg/500px-Hungaroring.svg.png",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 19, "max_laps": 34},
            {"name": "MEDIUM", "optimal_laps": 26, "max_laps": 46},
            {"name": "HARD",   "optimal_laps": 36, "max_laps": 63},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.10},
            {"name": "MEDIUM", "loss_s": 0.07},
            {"name": "HARD",   "loss_s": 0.05},
        ],
    },

    "Dutch GP": {
        "first_gp": 1952,
        "laps": 72,
        "length_km": 4.259,
        "lap_record": "1:11.097 (L. Hamilton, 2021)",
        "option_strategy": "2-Stop (Soft → Medium → Soft)",
        "alternate_strategy": "2-Stop (Medium → Soft → Soft)",
        "alternate_strategy_2": "1-Stop (Medium → Hard)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 24, "max_laps": 42},
            {"name": "MEDIUM", "optimal_laps": 33, "max_laps": 59},
            {"name": "HARD",   "optimal_laps": 39, "max_laps": 68},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.07},
            {"name": "MEDIUM", "loss_s": 0.04},
            {"name": "HARD",   "loss_s": 0.03},
        ],
    },

    "Italian GP": {
        "first_gp": 1950,
        "laps": 53,
        "length_km": 5.793,
        "lap_record": "1:20.901 (L. Norris, 2025)",
        "option_strategy": "1-Stop (Medium → Hard)",
        "alternate_strategy": "1-Stop (Soft → Medium)",
        "alternate_strategy_2": "2-Stop (Soft → Medium → Soft)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 21, "max_laps": 38},
            {"name": "MEDIUM", "optimal_laps": 29, "max_laps": 51},
            {"name": "HARD",   "optimal_laps": 40, "max_laps": 70},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.08},
            {"name": "MEDIUM", "loss_s": 0.06},
            {"name": "HARD",   "loss_s": 0.04},
        ],
    },

    "Spanish GP": {
        "first_gp": 2026,
        "laps": 57,
        "length_km": 5.416,
        "lap_record": "...",
        "option_strategy": "...",
        "alternate_strategy": "...",
        "alternate_strategy_2": "...",
        # Below fix doesn't bypass API image request successfully
        # "circuit_map_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/...",
        # "compound_performance": [
        #     {"name": "SOFT",   "optimal_laps": , "max_laps": },
        #     {"name": "MEDIUM", "optimal_laps": , "max_laps": },
        #     {"name": "HARD",   "optimal_laps": , "max_laps": },
        # ],
        # "deg_loss_per_lap": [
        #     {"name": "SOFT",   "loss_s": },
        #     {"name": "MEDIUM", "loss_s": },
        #     {"name": "HARD",   "loss_s": },
        # ],
    },

    "Azerbaijan GP": {
        "first_gp": 2016,
        "laps": 51,
        "length_km": 6.003,
        "lap_record": "1:43.009 (C. Leclerc, 2019)",
        "option_strategy": "1-Stop (Medium → Hard)",
        "alternate_strategy": "1-Stop (Soft → Hard)",
        "alternate_strategy_2": "2-Stop (Medium → Hard → Soft)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 30, "max_laps": 53},
            {"name": "MEDIUM", "optimal_laps": 40, "max_laps": 71},
            {"name": "HARD",   "optimal_laps": 56, "max_laps": 98},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.09},
            {"name": "MEDIUM", "loss_s": 0.06},
            {"name": "HARD",   "loss_s": 0.04},
        ],
    },

    "Singapore GP": {
        "first_gp": 2008,
        "laps": 62,
        "length_km": 4.927,
        "lap_record": "1:33.808 (L. Hamilton, 2025)",
        "option_strategy": "2-Stop (Soft → Medium → Soft)",
        "alternate_strategy": "2-Stop (Soft → Soft → Hard)",
        "alternate_strategy_2": "1-Stop (Medium → Hard)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 19, "max_laps": 33},
            {"name": "MEDIUM", "optimal_laps": 25, "max_laps": 44},
            {"name": "HARD",   "optimal_laps": 35, "max_laps": 62},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.14},
            {"name": "MEDIUM", "loss_s": 0.10},
            {"name": "HARD",   "loss_s": 0.06},
        ],
    },

    "United States GP": {
        "first_gp": 2012,
        "laps": 56,
        "length_km": 5.513,
        "lap_record": "1:36.169 (C. Leclerc, 2019)",
        "option_strategy": "2-Stop (Medium → Medium → Hard)",
        "alternate_strategy": "2-Stop (Soft → Medium → Hard)",
        "alternate_strategy_2": "2-Stop (Medium → Hard → Medium)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 15, "max_laps": 26},
            {"name": "MEDIUM", "optimal_laps": 21, "max_laps": 37},
            {"name": "HARD",   "optimal_laps": 29, "max_laps": 51},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.14},
            {"name": "MEDIUM", "loss_s": 0.09},
            {"name": "HARD",   "loss_s": 0.06},
        ],
    },

    "Mexico City GP": {
        "first_gp": 1963,
        "laps": 71,
        "length_km": 4.304,
        "lap_record": "1:17.774 (V. Bottas, 2021)",
        "option_strategy": "1-Stop (Medium → Hard)",
        "alternate_strategy": "2-Stop (Soft → Hard → Soft)",
        "alternate_strategy_2": "1-Stop (Soft → Hard)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 21, "max_laps": 37},
            {"name": "MEDIUM", "optimal_laps": 28, "max_laps": 49},
            {"name": "HARD",   "optimal_laps": 38, "max_laps": 68},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.10},
            {"name": "MEDIUM", "loss_s": 0.7},
            {"name": "HARD",   "loss_s": 0.5},
        ],
    },

    "São Paulo GP": {
        "first_gp": 1973,
        "laps": 71,
        "length_km": 4.309,
        "lap_record": "1:10.540 (V. Bottas, 2018)",
        "option_strategy": "2-Stop (Soft → Medium → Soft)",
        "alternate_strategy": "1-Stop (Medium → Hard)",
        "alternate_strategy_2": "2-Stop (Medium → Medium → Hard)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 22, "max_laps": 39},
            {"name": "MEDIUM", "optimal_laps": 30, "max_laps": 54},
            {"name": "HARD",   "optimal_laps": 42, "max_laps": 75},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.06},
            {"name": "MEDIUM", "loss_s": 0.04},
            {"name": "HARD",   "loss_s": 0.03},
        ],
    },

    "Las Vegas GP": {
        "first_gp": 2023,
        "laps": 50,
        "length_km": 6.201,
        "lap_record": "1:33.365 (M. Verstappen, 2025)",
        "option_strategy": "1-Stop (Medium → Hard)",
        "alternate_strategy": "1-Stop (Soft → Hard)",
        "alternate_strategy_2": "2-Stop (Soft → Medium → Soft)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 18, "max_laps": 33},
            {"name": "MEDIUM", "optimal_laps": 25, "max_laps": 44},
            {"name": "HARD",   "optimal_laps": 34, "max_laps": 61},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.12},
            {"name": "MEDIUM", "loss_s": 0.08},
            {"name": "HARD",   "loss_s": 0.06},
        ],
    },

    "Qatar GP": {
        "first_gp": 2023,
        "laps": 57,
        "length_km": 5.419,
        "lap_record": "1:22.384 (L. Norris, 2024)",
        "option_strategy": "2-Stop (Medium → Hard → Medium)",
        "alternate_strategy": "2-Stop (Soft → Medium → Medium)",
        "alternate_strategy_2": "2-Stop (Soft → Hard → Medium)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 17, "max_laps": 30},
            {"name": "MEDIUM", "optimal_laps": 24, "max_laps": 43},
            {"name": "HARD",   "optimal_laps": 28, "max_laps": 49},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.10},
            {"name": "MEDIUM", "loss_s": 0.07},
            {"name": "HARD",   "loss_s": 0.05},
        ],
    },

    "Abu Dhabi GP": {
        "first_gp": 2009,
        "laps": 58,
        "length_km": 5.281,
        "lap_record": "1:25.637 (K. Magnussen, 2024)",
        "option_strategy": "1-Stop (Medium → Hard)",
        "alternate_strategy": "2-Stop (Soft → Hard → Medium)",
        "alternate_strategy_2": "2-Stop (Soft → Hard → Soft)",
        "compound_performance": [
            {"name": "SOFT",   "optimal_laps": 19, "max_laps": 33},
            {"name": "MEDIUM", "optimal_laps": 25, "max_laps": 44},
            {"name": "HARD",   "optimal_laps": 35, "max_laps": 61},
        ],
        "deg_loss_per_lap": [
            {"name": "SOFT",   "loss_s": 0.10},
            {"name": "MEDIUM", "loss_s": 0.08},
            {"name": "HARD",   "loss_s": 0.05},
        ],
    },
}
