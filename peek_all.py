import json
import requests

# This code is a Python script that helps explore the structure of data
# returned by various APIs, specifically related to Formula 1 racing data.
# It uses the requests library to make HTTP GET requests to different endpoints
# and the json library to format and print the data in a readable way.

def peek_endpoint(title, url, is_list=True):
    # The main function, peek_endpoint, takes in a title, a URL, and a boolean
    # flag is_list (defaulting to True). It prints out the title and URL...
    print("\n" + "="*80)
    print(f"📡 TARGET: {title}")
    print(f"🔗 URL: {url}")
    print("="*80)

    try:
        # ...then tries to fetch data from the URL. If the request is successful
        # and the data is not empty...
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            print(f"❌ Failed to fetch data. HTTP Status: {response.status_code}")
            return None

        data = response.json()

        if not data:
            print("⚠️ Endpoint returned an empty dataset [].")
            return None

        # ...it checks if the data is a list or a dictionary. If it's a list,
        # it prints the structure of the first item.
        if is_list and isinstance(data, list):
            print(f"💡 Contains a list of {len(data)} items. Printing the structure of item[0]:")
            print(json.dumps(data[0], indent=4))
            return data[0]

        # If it's a dictionary, it prints the top-level structure, and if it
        # contains a specific key ("MRData"), it tries to print a more detailed structure.
        else:
            print("💡 Printing the top-level object structure:")
            if "MRData" in data:
                print("Showing pruned structure (StandingsLists -> DriverStandings[0]):")
                try:
                    lists = data["MRData"]["StandingsTable"]["StandingsLists"][0]
                    sample_standing = lists["DriverStandings"][0]
                    print(json.dumps({"SeasonInfo": {k:v for k,v in lists.items() if k != 'DriverStandings'}, "SampleDriverStanding": sample_standing}, indent=4))
                except Exception:
                    print(json.dumps(data, indent=4)[:1000] + "\n...[Truncated for length]...")
            return data

    except Exception as e:
        print(f"💥 Error inspecting data structural maps: {e}")
        return None

def main():
    # The main function orchestrates the exploration by calling peek_endpoint
    # with different URLs and titles.
    print("🏎️ F1 DATA STRUCTURE MAPPER (PEEK MODE) 🏎️")
    print("Discovering active production baseline schema variables...")

    # It starts by peeking at a "Sessions Registry" endpoint...
    session_sample = peek_endpoint(
        "OpenF1 - Sessions Registry",
        "https://api.openf1.org/v1/sessions?year=2024&session_name=Race"
    )

    if not session_sample:
        print("Could not retrieve baseline keys. Exiting peek engine.")
        return

    # ...then uses keys from the returned data to peek at related endpoints.
    session_key = session_sample.get("session_key")
    meeting_key = session_sample.get("meeting_key")

    if meeting_key:
        peek_endpoint(
            "OpenF1 - Meeting / Circuit Parameters",
            f"https://api.openf1.org/v1/meetings?meeting_key={meeting_key}"
        )

    if session_key:
        peek_endpoint(
            "OpenF1 - Drivers Lineup Data Map",
            f"https://api.openf1.org/v1/drivers?session_key={session_key}"
        )

        peek_endpoint(
            "OpenF1 - Raw Lap Timing Metrics",
            f"https://api.openf1.org/v1/laps?session_key={session_key}"
        )

        peek_endpoint(
            "OpenF1 - Computed Session Final Results",
            f"https://api.openf1.org/v1/session_result?session_key={session_key}"
        )

    # Finally, it peeks at a "Seasonal Driver Standings" endpoint.
    peek_endpoint(
        "Jolpica (Ergast API Mirror) - Seasonal Driver Standings",
        "https://api.jolpi.ca/ergast/f1/2024/driverStandings.json",
        is_list=False
    )

# The script is designed to be run as a standalone program, and it prints
# out information about the data structures it encounters, helping you
# understand the layout of the data returned by these APIs.
if __name__ == "__main__":
    main()
