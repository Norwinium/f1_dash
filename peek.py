import requests

# 1. Fetch the raw data from the OpenF1 meetings endpoint
response = requests.get("https://api.openf1.org/v1/meetings?year=2026")
meetings = response.json()

# 2. Extract and store meeting_key and location
# We store them as a tuple (key, location) in a list to maintain the pairing
meeting_data = []
for m in meetings:
    key = m.get("meeting_key")
    loc = m.get("location")
    if key and loc:
        meeting_data.append((key, loc))

# Sort by location name for better readability
meeting_data.sort(key=lambda x: x[1])

print(f"{'Meeting Key':<15} | {'Location'}")
print("-" * 35)
for key, loc in meeting_data:
    print(f"{key:<15} | {loc}")
