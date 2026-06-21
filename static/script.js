// Wait for the page to fully load before executing the script
document.addEventListener("DOMContentLoaded", () => {
    // --- 1. COUNTDOWN MATH LOGIC ---
    const card = document.getElementById("session-card");

    // Check if the session card and countdown elements exist before running the logic
    const daysEl = document.getElementById("days");
    if (card && daysEl) {

        // Retrieve the session's start time from the card's data attributes
        const utcString = card.dataset.utc;
        const targetTime = new Date(utcString).getTime();
        const options = { weekday: 'long', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
        const nextUtcString = card.dataset.nextUtc || utcString;

        // Display the session's local time in a readable format
        const localTimeEl = document.getElementById("local-time");
        if (localTimeEl) {
            localTimeEl.innerText = new Date(nextUtcString).toLocaleString(undefined, options);
        }

        // Display the grand prix start time in a readable format
        const grandPrixStartEl = document.getElementById("grand-prix-start");
        if (grandPrixStartEl) {
            grandPrixStartEl.innerText = new Date(utcString).toLocaleString(undefined, options);
        }

        // --- SUMMER TIME / WINTER TIME LABEL (index.html) ---
        // Retrieve the timezone from the card's data attributes, determine whether
        // the session falls in summer or winter time, and display the appropriate label.
        const dstLabelEl = document.getElementById("dst-label");
        const timezone = card.dataset.timezone;
        if (dstLabelEl && timezone && timezone !== 'UTC') {
            const tzName = new Intl.DateTimeFormat('en', {
                timeZone: timezone,
                timeZoneName: 'long'  // e.g. "Central European Summer Time"
            }).formatToParts(new Date(utcString))
                .find(p => p.type === 'timeZoneName')?.value || '';
            dstLabelEl.innerText = tzName.includes('Summer') ? 'Summer Time' : 'Winter Time';
        }

        // Cache references to DOM elements so we aren't looking them up every single second
        const hoursEl = document.getElementById("hours");
        const minutesEl = document.getElementById("minutes");
        const secondsEl = document.getElementById("seconds");

        // Define the function that calculates the time remaining until the session starts
        function updateCountdown() {
            const now = new Date().getTime();
            const difference = targetTime - now;

            // If the session is live, display a "SESSION IS LIVE!" message and stop the timer
            if (difference <= 0) {
                card.innerHTML = `
                    <div class="text-center py-6">
                        <span class="animate-ping inline-flex h-3 w-3 rounded-full bg-green-400 opacity-75 mr-2"></span>
                        <span class="text-xl font-bold text-green-400">SESSION IS LIVE!</span>
                    </div>`;
                clearInterval(timerInterval);
                return;
            }

            // Calculate the remaining days, hours, minutes, and seconds
            const days = Math.floor(difference / (1000 * 60 * 60 * 24));
            const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((difference % (1000 * 60)) / 1000);

            // Safely update the countdown elements with the remaining time values
            daysEl.innerText = String(days).padStart(2, '0');
            if (hoursEl) hoursEl.innerText = String(hours).padStart(2, '0');
            if (minutesEl) minutesEl.innerText = String(minutes).padStart(2, '0');
            if (secondsEl) secondsEl.innerText = String(seconds).padStart(2, '0');
        }

        // Run the initial countdown calculation immediately
        updateCountdown();

        // Set up the countdown timer to update every second (1000ms)
        const timerInterval = setInterval(updateCountdown, 1000);
    }
});
