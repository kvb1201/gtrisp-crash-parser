from rapidfuzz import fuzz


FIELD_ALIASES = {

    "accident_id": [
        "Accident ID"
    ],

    "fir_number": [
        "FIR/CSR Number"
    ],

    "district_name": [
        "District Name"
    ],

    "severity": [
        "Severity"
    ],

    "road_classification": [
        "Road Classification"
    ],

    "road_name": [
        "Road Name / Street Name"
    ],

    "collision_type": [
        "Collision Type"
    ],

    "traffic_violation": [
        "Traffic Violation"
    ],

    "weather_condition": [
        "Weather Condition"
    ],

    "light_condition": [
        "Light Condition"
    ],

    "accident_spot": [
        "Accident Spot"
    ],

    "vehicle_type": [
        "Vehicle Type"
    ],

    "vehicle_category": [
        "Vehicle Category"
    ],

    "driver_gender": [
        "Gender"
    ],

    "driver_age": [
        "Age"
    ],

    "speed_limit": [
        "Vehicle Max. Speed Limit"
    ]
}


def fuzzy_match_label(line):

    best_field = None

    best_score = 0

    for field, aliases in FIELD_ALIASES.items():

        for alias in aliases:

            score = fuzz.partial_ratio(
                alias.lower(),
                line.lower()
            )

            if score > best_score:

                best_score = score

                best_field = field

    if best_score >= 85:
        return best_field

    return None