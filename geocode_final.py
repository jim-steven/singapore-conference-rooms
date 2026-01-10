#!/usr/bin/env python3
"""
Final fix: Add remaining manual coordinates from Google Maps.
"""

import json

DATA_FILE = "data.json"

# Coordinates from Google Maps
FINAL_COORDS = {
    "national-library": (1.2975, 103.8545),     # National Library Building
    "mit-space": (1.2923, 103.8508),            # Peninsula Plaza
    "o2work": (1.2961, 103.8540),               # Odeon Towers
    "justco-marina": (1.2912, 103.8571),        # Marina Square
    "mindchamps": (1.2912, 103.8571),           # Marina Square
    "justco-central": (1.2794, 103.8534),       # Central Boulevard area
    "exec-centre-orq": (1.2807, 103.8520),      # One Raffles Quay
}

def main():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    
    fixed = 0
    
    for section in data["sections"]:
        for venue in section["venues"]:
            venue_id = venue.get("id", "")
            
            if venue.get("lat") is None and venue_id in FINAL_COORDS:
                lat, lng = FINAL_COORDS[venue_id]
                venue["lat"] = lat
                venue["lng"] = lng
                print(f"✓ {venue['name']}: {lat}, {lng}")
                fixed += 1
    
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    
    # Verify all venues have coordinates
    missing = []
    for section in data["sections"]:
        for venue in section["venues"]:
            if venue.get("lat") is None:
                missing.append(venue["name"])
    
    print(f"\nFixed: {fixed}")
    print(f"Still missing: {len(missing)}")
    if missing:
        for name in missing:
            print(f"  - {name}")

if __name__ == "__main__":
    main()
