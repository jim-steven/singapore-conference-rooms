#!/usr/bin/env python3
"""
Fix failed geocoding by using simplified addresses or known coordinates.
"""

import json
import time
import urllib.request
import urllib.parse
import re

DATA_FILE = "data.json"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

# Manual coordinates for venues that need them (from Google Maps)
MANUAL_COORDS = {
    "huone-cottage": (1.2901, 103.8455),  # HUONE Clarke Quay
    "huone-nest": (1.2901, 103.8455),
    "huone-time": (1.2901, 103.8455),
    "expo-opal": (1.3350, 103.9617),  # Singapore EXPO
    "hometeamns": (1.2914, 103.8494),  # Funan Mall
}

# Simplified addresses for retry
SIMPLIFIED_ADDRESSES = {
    "queserser": "1 Upper Circular Road, Singapore",
    "national-library-pod": "100 Victoria Street, Singapore",
    "lionsworld": "111 North Bridge Road, Singapore",
    "mit-space-city-hall": "111 North Bridge Road, Singapore",
    "great-room-raffles": "328 North Bridge Road, Singapore",
    "o2work-odeon": "331 North Bridge Road, Singapore",
    "justco-marina-sq": "6 Raffles Boulevard, Singapore",
    "mindchamps-marina": "6 Raffles Boulevard, Singapore",
    "exec-centre-mbfc": "8 Marina Boulevard, Singapore",
    "justco-central-plaza": "Central Boulevard, Singapore",
    "regus-cbd": "1 Raffles Place, Singapore",  # Fallback to central CBD
    "rnn-ces": "171 Chin Swee Road, Singapore",
    "rnn-gb": "143 Cecil Street, Singapore",
    "venuesquare-cecil": "137 Cecil Street, Singapore",
    "exec-centre-raffles-quay": "1 Raffles Quay, Singapore",
    "workcentral": "190 Clemenceau Avenue, Singapore",
}

def geocode_address(address: str) -> tuple[float, float] | None:
    if not address:
        return None
    
    params = urllib.parse.urlencode({
        "q": address,
        "format": "json",
        "limit": 1,
        "countrycodes": "sg"
    })
    
    url = f"{NOMINATIM_URL}?{params}"
    headers = {"User-Agent": "SingaporeConferenceRooms/1.0"}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception as e:
        print(f"  Error: {e}")
    
    return None

def main():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    
    fixed_count = 0
    still_failed = []
    
    for section in data["sections"]:
        for venue in section["venues"]:
            venue_id = venue.get("id", "")
            name = venue.get("name", "Unknown")
            
            # Skip if already has coordinates
            if venue.get("lat") is not None:
                continue
            
            print(f"Fixing: {name} ({venue_id})")
            
            # Try manual coordinates first
            if venue_id in MANUAL_COORDS:
                lat, lng = MANUAL_COORDS[venue_id]
                venue["lat"] = lat
                venue["lng"] = lng
                print(f"  ✓ Manual: {lat}, {lng}")
                fixed_count += 1
                continue
            
            # Try simplified address
            if venue_id in SIMPLIFIED_ADDRESSES:
                result = geocode_address(SIMPLIFIED_ADDRESSES[venue_id])
                if result:
                    venue["lat"] = result[0]
                    venue["lng"] = result[1]
                    print(f"  ✓ Simplified: {result[0]:.6f}, {result[1]:.6f}")
                    fixed_count += 1
                    time.sleep(1.1)
                    continue
            
            # Try stripping unit numbers from original address
            original = venue.get("address", "")
            simplified = re.sub(r'#\d+-\d+|#\d+', '', original)
            simplified = re.sub(r'\s+', ' ', simplified).strip()
            
            if simplified != original:
                result = geocode_address(simplified + ", Singapore")
                if result:
                    venue["lat"] = result[0]
                    venue["lng"] = result[1]
                    print(f"  ✓ Stripped: {result[0]:.6f}, {result[1]:.6f}")
                    fixed_count += 1
                    time.sleep(1.1)
                    continue
            
            still_failed.append((name, venue.get("address", "")))
            print(f"  ✗ Still failed")
            time.sleep(1.1)
    
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"Fixed: {fixed_count}")
    print(f"Still failed: {len(still_failed)}")
    
    if still_failed:
        print("\nStill need manual coordinates:")
        for name, addr in still_failed:
            print(f"  - {name}: {addr}")

if __name__ == "__main__":
    main()
