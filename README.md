# F1 Dashboard

#### Video Demo: https://youtu.be/3bLehXZkPDI

#### Description:

# The project:

    My F1 Dashboard is a Flask-based web app that pulls live and historical Formula 1 data
    from the OpenF1 and Jolpica APIs (using Open-Meteo API). The home page shows the upcoming
    race weekend, including a multi-day weather forecast, circuit details, and typical race
    strategy statistics for that track.

    The Results page lets you browse every completed race weekend of the 2026 season via
    a dropdown, then switch between sessions (Practice, (Sprint) Qualifying, Sprint or Race)
    using a tab bar. The classification table shows finishing position, constructor colour,
    best lap time, and gap to the leader — with DNF drivers flagged and dimmed at the bottom.

    The Standings page displays the current Driver's and Constructor's Championship
    standings with team colours and points totals, sourced from the Jolpica Ergast mirror
    rather than OpenF1 for reliability.

    The Track Stats page lets you select any 2026 Grand Prix and view detailed circuit
    information — including the circuit map, lap record, race distance, pit stop time loss,
    and VSC pit loss. It also displays historical race strategy recommendations, safety car
    probability with a visual progress bar, tyre compound performance windows,
    and per-compound degradation rates across Soft, Medium, and Hard tyres. For performance
    and reliability reasons, a local model has been created to be used in lieu of
    (un-)official telemetry.


# File descriptions:

    - app.py
        The Flask application entry point for the F1 Dashboard. It defines the full
        2026 Grand Prix calendar as a hardcoded list of 24 rounds with their OpenF1
        meeting keys, and builds a key-indexed lookup dictionary for fast access by URL
        parameter. Four routes power the application. The home page (/) fetches the current
        year's sessions from OpenF1, identifies the next upcoming race, and passes circuit
        details, a multi-day weather forecast, and historical strategy statistics to the
        template. The Results page (/Results) accepts optional round and session query
        parameters, uses a date-window approach to match rounds to OpenF1 session data,
        and retries the API up to five times for reliability before rendering the
        classification table. The Standings page (/Standings) serves either driver or
        constructor championship tables sourced from the Jolpica Ergast mirror, toggled
        via a view query parameter. The Track Stats page (/TrackStats) maps a selected
        GP key to its calendar entry and pulls live circuit details from OpenF1, static
        circuit data, and historical strategy statistics from helpers.py. All external API
        calls and data processing logic are delegated to services.py and helpers.py,
        keeping the route handlers clean and focused on request handling and
        template rendering.

    - helpers.py
        helpers.py is a constants and utilities module for the F1 Dashboard, containing
        no API calls or side effects — only static data and one small helper function.
        It holds three major data structures. DRIVER_CACHE is a global dictionary populated
        at startup by services.py to avoid repeated driver lookup API calls during requests.
        TRACK_STRATEGY_STATS is a hand-curated dictionary keyed by lowercase location name
        covering all twenty-four 2026 race venues, storing historical safety car probability,
        recommended tyre strategy, pit stop time loss, and VSC pit loss for each circuit.
        CIRCUIT_COORDINATES maps the same location names to latitude and longitude pairs,
        used by the weather forecast feature on the home page. CIRCUIT_DATA is the largest
        structure — a per-Grand Prix dictionary keyed by the exact race name from the 2026
        calendar, storing first Grand Prix year, scheduled race laps, circuit length in
        kilometres, lap record, up to three tyre strategy options, compound performance
        windows showing optimal and maximum lap ranges for Soft, Medium, and Hard tyres,
        and per-compound degradation time loss per lap. All 24 rounds have entries, with
        Madrid left intentionally sparse as a brand-new venue with no historical data. The
        single utility function, clean_location_string, strips unicode accents and lowercases
        location names for consistent dictionary lookups across the app.

    - services.py
        services.py is the data access layer of the F1 Dashboard, responsible for all
        communication with external APIs and converting raw responses into application-ready
        data. It integrates with OpenF1 for live motorsport information, Open-Meteo for
        weather forecasts, and the Jolpica Ergast mirror for championship standings and race
        calendars. At startup it populates a global driver cache to reduce repeated API calls
        and improve performance. The module includes resilient weather retrieval with retry
        logic to minimise failures, functions to fetch circuit metadata, and routines that
        process lap, pit stop, and driver data into complete session classifications.
        Race results are reconstructed by calculating total times, best laps, gaps to the
        leader, tyre usage, pit stops, and automatically identifying DNFs based on completed
        lap counts. Additional functions retrieve and format both Driver’s and Constructor’s
        Championship standings with associated team colours, as well as the list of completed
        race weekends for the current season.

    - peek.py
        A lightweight stand-alone utility script that queries the OpenF1 meetings API for a
        given season, extracts each event’s meeting_key and location, and displays them in a
        neatly formatted table. It filters out incomplete records, preserves the key–location
        relationship, sorts the results alphabetically by location, and prints them for easy
        reference. The script is useful for quickly identifying meeting
        identifiers needed when working with other OpenF1 endpoints.

    - peek_all.py
        A diagnostic tool for exploring the structure of Formula 1 data returned by the OpenF1
        and Jolpica APIs. It fetches sample datasets from multiple endpoints, validates
        responses, and prints formatted JSON to reveal available fields and nested objects.
        By automatically chaining related API calls using retrieved session and meeting keys,
        it provides a convenient way to inspect schemas, verify endpoint contents, and
        understand the data available for use when developing or debugging F1 applications.

    - f1_metrics_sources.md
        This document explains the authoritative sources behind Formula 1 strategy and track
        metrics. (Although not actually utilized in the project. It was helpful in the ultimate
        decision to create a local model. The file remains in the directory in case of future
        ambitions to update the app.) It describes how official pre-race data from Formula 1,
        Pirelli, and Brembo (brakes supplier) provide statistics such as Safety Car and Virtual
        Safety Car probabilities, pit lane time loss, tyre strategies, and undercut performance.
        It also highlights notable track-specific patterns, such as Jeddah’s consistently high
        Safety Car likelihood, and identifies where these metrics can be updated during
        each race weekend.

    - layout.html
        This Jinja2 base template defines the shared layout for the F1 Dashboard. It includes a
        responsive Tailwind-powered header, navigation bar, dynamic session banner with circuit
        details, content injection blocks, smooth scrolling, and a footer disclaimer. The
        template uses safe fallbacks to display session information reliably across all pages.

    - index.html
        This Jinja2/HTML template renders the main F1 Dashboard homepage, presenting the
        upcoming Grand Prix countdown, next session timing, circuit information, weather
        forecast, and historical strategy insights. It uses responsive Tailwind CSS panels,
        dynamically populates data from Flask variables (such as session, weather, circuit,
        and strategy), and loads a JavaScript file to update countdown and local time displays.

    - results.html
        This Jinja2/Flask template renders a Formula 1 session results page with a race weekend
        selector, chronological session navigation, and a classification table showing positions,
        drivers, constructors, best laps, and gaps. It includes a telemetry disclaimer,
        responsive styling, DNF handling, team color indicators, and informative empty states
        when no event or data is available.

    - standings.html
        This Jinja2/Flask template displays the 2026 Formula 1 championship standings with a
        seasonal header and toggle between driver and constructor views. It renders a responsive
        table showing positions, competitors, teams, and points, styled with team color
        indicators and (attempted) mobile-friendly layouts, while providing a fallback message
        when standings data is unavailable.

    - track_stats.html
        This Jinja2 template renders the Track Stats page of the F1 Dashboard. It provides a
        Grand Prix selector and, once a race is chosen, displays circuit details including the
        track name, flag, map, GMT offset, lap record, race distance, circuit length, and
        pit stop time loss. It also presents strategy-focused information such as recommended
        tyre strategies, Safety Car probability, compound performance windows, and tyre
        degradation estimates. If data is unavailable, the page shows informative fallback
        messages and prompts for adding missing circuit information.

    - script.js
        This JavaScript script runs after the DOM loads to manage an interactive Grand Prix
        countdown timer. It reads UTC timestamps and timezone data from HTML data attributes,
        converts them, and displays localized start times. It also detects whether the event
        occurs during Summer or Winter time to update seasonal UI labels. Finally, a cached
        setInterval function calculates the remaining days, hours, minutes, and seconds and
        updates accordingly. When the countdown reaches zero, it stops the timer and replaces
        the element's inner HTML with a flashing "SESSION IS LIVE!" notification.

    - styles.css
        This CSS code creates a retro, 1990s-style look for a website. It uses a dark color
        scheme with a black background and light gray text. Borders are solid and light gray,
        and there are no rounded corners or shadows, giving a blocky, flat appearance. Text
        and images are rendered in a pixelated style to enhance the retro feel. Interactive
        elements like links and buttons have a light gray color and a black background, with
        a slight text shadow. Headers are white, and h2 elements have a yellow background with
        black text. Paragraphs under h2 elements have a light gray background and black text.
        Tables have solid light gray borders. Focus outlines are more visible for better
        accessibility. The body has a glow and scanline effect to mimic old CRT monitors.
        Active session links have a yellow background and black text.

# Design choices:

    - I initially used only the OpenF1 and Open-Meteo APIs for effiency. However, historical data
        was tricky to implement and as such the use of Jolpica API (F1 data) became a necessity.

    - At first, weather API requests frequently failed. As such, I had to bake in a fail safe such
        that the page is (almost) certain to load the weather forecast. This, at the cost of
        performance. It became clear early on, that reliability had to be chosen over speed if I
        was to frequently use this dashboard in the build-up to an F1 weekend. Which, in light of
        the project's ambition to outlive the scope of CS50, was a no-brainer. Track coordinates
        have been taken from the track's wikipedia page and manually translated into the correct
        format.

    - I would have much preferred to take historical track statistics from an API request.
        However, it became difficult and unreliable to implement so I chose to create a local model
        instead. Being as the index is slow as it is, a more performant track statistics page became
        appealing. I used a combination of F1's official documentation on their website, wikipedia
        and video game F1 Manager 2024 to populate my TRACK_STRATEGY_STATS and CIRCUIT_DATA.

    - Initial app.py contained all the functions and lists/dictionaries. Once it became unwieldy,
        I split it into app.py, services.py and helpers.py. The process of building this web app
        has provided invaluable experience in prioritization of file management and the splitting
        thereof.

# Reflection:

    - After finishing the C$50 Financo problem set, I thought I wouldn't use Flask in a rush as I
        found it to be a tedious and time-consuming task. Upon brainstorming ideas for my final
        project, a friend suggested an F1 web app. As an avid F1 fan, it seemed an exciting idea to
        design my own data and telemetry app for use in the build-up to an F1 weekend. Once I
        started the project. I quickly realized, during the prototype phase, how exciting the
        possibilities were. At first, I simply wanted to display a weather forecast with the expected
        tyre strategies. Once I realized the power that lays within API requests and the databases
        therein, I doubled down and struggled to keep the concept to a "Minimal Viable Product".
        As a consequence, I added features that forced me to think about efficiency vs. reliability.
        In so doing, I learnt much more about the power of, as well as the limitations of,
        API requests than I otherwise would have. I'm very pleased with the end product despite
        some glitches in the Track Stats page and the frequently missing header in the Results page.

        I used a combination of Gemini, Claude and ChatGPT models to achieve in days what would
        otherwise have taken weeks, if not, months. For a student's final assignment, I am proud of
        what I have achieved. Even though I would like to have achieved more data accuracy from the
        API requests. I learnt that third-party databases have limitations of their own upon feeling
        the need to create my own local model. In future, I might consider creating a local SQL
        database that intermittently pulls data from an API. Which is a valuable lesson in itself.
        Considering how much more was achieved than initially set out for. I think the outcome is
        great, though far from perfect. Especially the UI on mobile isn't as good as I had hoped.
        That's something I will consider sooner in the design process next time. Designing for
        mobile using Chrome dev tools was okay but I did find that it looked a lot better on my
        phone than might be expected from Chrome (iPhone SE model view).

        Hosting the Flask application proved a difficult task. Providing many more troubleshooting
        tasks than anticipated. Plenty of API requests loaded fine while locally hosted but stopped
        working while hosting for free. Eventually, I opted for Google Cloud.
