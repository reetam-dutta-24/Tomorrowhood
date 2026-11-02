"""Amenity taxonomy: maps OSM (class, subtype) pairs to feature groups.
Edit this file to change what counts as what. Unlisted pairs are ignored.
Each (class, subtype) pair may appear in ONE group only."""
import pandas as pd

TAXONOMY = {
    "daily_services": {
        "amenity": {"bank", "atm", "post_office", "library", "community_centre", "townhall",
                    "police", "fire_station", "veterinary", "social_facility", "marketplace"},
        "shop": {"hairdresser", "beauty", "laundry", "dry_cleaning", "copyshop", "tailor", "optician"},
    },
    "healthcare": {"amenity": {"hospital", "clinic", "doctors", "dentist", "pharmacy"}},
    "education": {"amenity": {"school", "kindergarten", "college", "university", "language_school",
                              "music_school", "driving_school", "childcare"}},
    "food_drink": {"amenity": {"restaurant", "cafe", "fast_food", "food_court", "ice_cream", "biergarten"}},
    "nightlife": {"amenity": {"bar", "pub", "nightclub", "casino", "stripclub"}},
    "culture_leisure": {
        "amenity": {"cinema", "theatre", "arts_centre", "events_venue", "planetarium"},
        "leisure": {"bowling_alley", "amusement_arcade", "escape_game", "miniature_golf", "dance",
                    "water_park", "ice_rink", "trampoline_park"},
        "tourism": {"museum", "gallery", "attraction", "theme_park", "zoo", "aquarium"},
    },
    "wellness_fitness": {"leisure": {"fitness_centre", "sports_centre", "swimming_pool", "sauna", "spa"}},
    "green_outdoor": {"leisure": {"park", "garden", "playground", "pitch", "nature_reserve", "dog_park"}},
    "modern_tech": {
        "amenity": {"charging_station", "bicycle_rental", "car_sharing", "parcel_locker",
                    "coworking_space", "vending_machine"},
        "office": {"coworking"},
    },
    "upscale_retail": {"shop": {"jewelry", "art", "antiques", "wine", "deli", "cheese", "perfumery",
                                "boutique", "watches", "interior_decoration", "chocolate", "tea",
                                "florist", "fashion_accessories", "cosmetics"}},
    "upscale_leisure": {"leisure": {"golf_course", "marina"}},
    "everyday_retail": {"shop": {"supermarket", "convenience", "greengrocer", "bakery", "butcher",
                                 "clothes", "shoes", "department_store", "mall", "kiosk",
                                 "variety_store", "hardware", "chemist", "electronics",
                                 "mobile_phone", "books", "stationery", "gift", "pet"}},
    "worship": {"amenity": {"place_of_worship"}},
    "transport": {"transit": {"bus_stop", "station", "tram_stop", "subway_entrance"},
                  "amenity": {"taxi", "bus_station", "ferry_terminal"}},
    "stay": {"tourism": {"hotel", "hostel", "motel", "guest_house", "apartment"}},
    "trees": {"tree": {"tree"}},
    # Street furniture is kept apart on purpose: it is NOT amenity richness.
    "street_furniture": {"amenity": {"parking", "parking_space", "parking_entrance", "bench",
                                     "waste_basket", "bicycle_parking", "recycling", "post_box",
                                     "toilets", "shelter", "drinking_water", "fountain", "telephone",
                                     "motorcycle_parking", "bicycle_repair_station",
                                     "waste_disposal", "clock"}},
}

# Transparent composites: sums of group (or special) columns. Not final scores.
COMPOSITES = {
    "leisure_modern_upscale": ["culture_leisure", "nightlife", "wellness_fitness", "modern_tech",
                               "upscale_retail", "upscale_leisure", "upscale_hotels"],
    "everyday_services": ["daily_services", "healthcare", "education", "food_drink", "everyday_retail"],
}


def taxonomy_frame():
    rows = [(cls, sub, grp)
            for grp, by_cls in TAXONOMY.items()
            for cls, subs in by_cls.items()
            for sub in sorted(subs)]
    df = pd.DataFrame(rows, columns=["cls", "sub", "grp"])
    dup = df[df.duplicated(["cls", "sub"], keep=False)]
    if not dup.empty:
        raise ValueError(f"A (class, subtype) pair is in two groups:\n{dup}")
    return df