
import re

from src.fusion_engine import (
    fuzzy_match_label
)


FIELD_PATTERNS = {

    "accident_id":
        r"Accident ID\s*:\s*(.+)",

    "fir_number":
        r"FIR/CSR Number\s*:\s*([A-Z0-9]+)",

    "district_name":
        r"District Name\s*:\s*([A-Za-z ]+)",

    "severity":
        r"Severity\s+(Fatal|Minor Injury|Grievous Injury|No Injury)",

    "road_classification":
        r"Road Classification\s+([A-Za-z ]+)",

    "road_name":
        r"Road Name / Street Name\s*(.+)",

    "collision_type":
        r"Collision Type\s+([A-Za-z ]+)",

    "traffic_violation":
        r"\nTraffic Violation\s+([A-Za-z ]+)",

    "weather_condition":
        r"Weather Condition\s+([A-Za-z /]+)",

    "light_condition":
        r"Light Condition\s+([A-Za-z ]+)",

    "accident_spot":
        r"Accident Spot\s+([A-Za-z ]+)",

    "vehicle_type":
        r"Vehicle Type\s*(.+)",

    "vehicle_category":
        r"Vehicle Category\s*(.+)",

    "driver_gender":
        r"Gender\s+(Male|Female|Other)",

    "driver_age":
        r"Age\s+(\d+)",

    "speed_limit":
        r"Vehicle Max\. Speed Limit\s+(\d+)"
}


def parse_crash_fields(text):

    extracted = {}

    for field, pattern in FIELD_PATTERNS.items():

        match = re.search(
            pattern,
            text
        )

        if match:

            extracted[field] = (
                match.group(1)
                .strip()
            )

        else:

            extracted[field] = None

    lines = text.split("\n")

    for line in lines:

        matched_field = fuzzy_match_label(line)

        if matched_field is None:
            continue

        if extracted.get(matched_field):
            continue

        parts = line.split()

        if len(parts) < 2:
            continue

        value = " ".join(parts[-3:])

        extracted[matched_field] = value

    return extracted