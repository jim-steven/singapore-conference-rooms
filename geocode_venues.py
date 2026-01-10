#!/usr/bin/env python3
"""
Geocode all venues in data.json using Nominatim (OpenStreetMap).
Adds lat/lng coordinates to each venue.
"""

import json
import time
import urllib.request
import urllib.parse

DATA_FILE = "data.json"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

def geocode_address(address: str) -> tuple[float, float] | None:
    """Geocode an address using Nominatim. Returns (lat, lng) or None."""
    if not address or address == "NA":
        return None
    
    # Append Singapore if not already present
    if "singapore" not in address.lower():
        address = f"{address}, Singapore"
    
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
        print(f"  Error geocoding '{address}': {e}")
    
    return None

def main():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    
    total_venues = 0
    geocoded_count = 0
    failed_addresses = []
    
    for section in data["sections"]:
        for venue in section["venues"]:
            total_venues += 1
            address = venue.get("address", "")
            name = venue.get("name", "Unknown")
            
            print(f"[{total_venues}] Geocoding: {name}")
            print(f"    Address: {address}")
            
            result = geocode_address(address)
            
            if result:
                venue["lat"] = result[0]
                venue["lng"] = result[1]
                geocoded_count += 1
                print(f"    ✓ Found: {result[0]:.6f}, {result[1]:.6f}")
            else:
                venue["lat"] = None
                venue["lng"] = None
                failed_addresses.append((name, address))
                print(f"    ✗ Not found")
            
            # Nominatim rate limit: 1 request per second
            time.sleep(1.1)
    
    # Save updated data
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"Geocoding complete!")
    print(f"  Total venues: {total_venues}")
    print(f"  Successfully geocoded: {geocoded_count}")
    print(f"  Failed: {len(failed_addresses)}")
    
    if failed_addresses:
        print(f"\nFailed addresses (may need manual lookup):")
        for name, addr in failed_addresses:
            print(f"  - {name}: {addr}")

if __name__ == "__main__":
    main()
