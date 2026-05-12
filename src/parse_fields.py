import re

from src.fusion_engine import (
    fuzzy_match_label
)


def clean_value(value):

    if value is None:
        return None

    value = value.strip()

    value = re.sub(r"\s+", " ", value)

    value = value.replace("\n", " ")

    value = value.replace("|", "")

    return value


def normalize_key(label):

    label = label.lower()

    label = re.sub(r"[^a-z0-9]+", "_", label)

    label = re.sub(r"_+", "_", label)

    label = label.strip("_")

    return label


CANONICAL_FIELDS = {
    "accident_id",
    "fir_number",
    "district_name",
    "station_name",
    "investigating_officer",
    "severity",
    "road_classification",
    "road_name",
    "collision_type",
    "collision_nature",
    "traffic_violation",
    "weather_condition",
    "light_condition",
    "accident_spot",
    "visibility",
    "property_damage",
    "damage_value",
    "vehicle_reg_no",
    "vehicle_type",
    "vehicle_category",
    "vehicle_class",
    "vehicle_color",
    "make_model",
    "fuel_type",
    "seating_capacity",
    "vehicle_damage",
    "speed_limit",
    "driver_gender",
    "driver_age",
    "education",
    "occupation",
    "nationality",
    "license_type",
    "license_status",
    "injury_type",
    "brake_condition",
    "steering_condition",
    "tyre_condition",
    "mechanical_failure",
}

CANONICAL_LABEL_ALIASES = {
    "fir_csr_number": "fir_number",
    "fir_number": "fir_number",
    "district_name": "district_name",
    "station_name": "station_name",
    "vehicle_type": "vehicle_type",
    "vehicle_category": "vehicle_category",
    "vehicle_class": "vehicle_class",
    "weather_condition": "weather_condition",
    "light_condition": "light_condition",
    "collision_type": "collision_type",
    "collision_nature": "collision_nature",
    "traffic_violation": "traffic_violation",
    "road_name_street_name": "road_name",
    "road_name": "road_name",
    "severity": "severity",
    "fuel_type": "fuel_type",
    "occupation": "occupation",
    "education": "education",
    "nationality": "nationality",
}


def resolve_canonical_alias(key):

    normalized = normalize_key(key)

    return CANONICAL_LABEL_ALIASES.get(
        normalized,
        normalized
    )


GENERIC_LABEL_PATTERNS = [

    r"^([A-Z][A-Za-z /&().?-]{3,50})\s*:\s*(.+)$",

    r"^([A-Z][A-Za-z /&().?-]{3,50})\s{2,}(.+)$",
]


IGNORE_GENERIC_KEYS = {
    "accident",
    "driver",
    "passenger",
    "pedestrian",
    "total",
    "station",
    "transport",
    "vehicle details",
    "driver details",
    "road details",
}

INVALID_LABEL_ENDINGS = {
    "of",
    "in",
    "to",
    "by",
    "and",
    "or",
    "with",
    "from",
    "for",
}


INVALID_VALUE_PREFIXES = {
    "details",
    "report",
    "summary",
}


MIN_LABEL_WORDS = 2
MAX_LABEL_WORDS = 8
MAX_LABEL_LENGTH = 60
MAX_VALUE_LENGTH = 120


SECTION_HEADERS = {
    "accident details",
    "vehicle details",
    "driver details",
    "transport",
    "road details",
    "mechanical",
}

SECTION_RESET_PATTERNS = {
    "number of persons involved",
    "number of animals involved",
    "killed grievous injury",
}


MULTILINE_CONTINUATION_PREFIXES = {
    "name",
    "type",
    "validity",
    "details",
    "address",
    "status",
    "condition",
}


CANONICAL_VALUE_MAPS = {

    "severity": {
        "fatal injury": "Fatal",
        "fatal": "Fatal",
        "grievous injury": "Grievous Injury",
        "minor injury": "Minor Injury",
        "no injury": "No Injury",
    },

    "property_damage": {
        "yes": "Yes",
        "no": "No",
    },

    "mechanical_failure": {
        "yes": "yes",
        "no": "no",
    }
}


def normalize_field_value(field, value):

    if value is None:
        return None

    mapping = CANONICAL_VALUE_MAPS.get(field)

    if mapping is None:
        return value

    value_lower = value.lower().strip()

    return mapping.get(value_lower, value)


def is_valid_label(label):

    if label is None:
        return False

    label = clean_value(label)

    if not label:
        return False

    if len(label) > MAX_LABEL_LENGTH:
        return False

    words = label.lower().split()

    if len(words) < MIN_LABEL_WORDS:
        return False

    if len(words) > MAX_LABEL_WORDS:
        return False

    if words[-1] in INVALID_LABEL_ENDINGS:
        return False

    if label.lower() in IGNORE_GENERIC_KEYS:
        return False

    if any(char.isdigit() for char in label):
        return False

    return True



def is_valid_value(value):

    if value is None:
        return False

    value = clean_value(value)

    if not value:
        return False

    if len(value) <= 1:
        return False

    value_lower = value.lower()

    for invalid_prefix in INVALID_VALUE_PREFIXES:

        if value_lower.startswith(invalid_prefix):
            return False

    if value_lower in SECTION_HEADERS:
        return False

    if len(value) > MAX_VALUE_LENGTH:
        return False

    if value.endswith(":"):
        return False

    return True


FIELD_PATTERNS = {

    # -----------------------------
    # CORE ACCIDENT METADATA
    # -----------------------------

    "accident_id":
        r"Accident ID\s*:\s*([A-Z0-9]+)",

    "fir_number":
        r"FIR/CSR Number\s*:\s*([A-Z0-9]+)",

    "district_name":
        r"District Name\s*:\s*([A-Za-z ]+)",

    "station_name":
        r"Station Name\s*:\s*([A-Za-z ]+)",

    "investigating_officer":
        r"Investigating Officer\s*:\s*([A-Za-z ]+)",

    "severity":
        r"Severity\s+(Fatal|Minor Injury|Grievous Injury|No Injury)",

    # -----------------------------
    # ROAD + ENVIRONMENT
    # -----------------------------

    "road_classification":
        r"Road Classification\s+([A-Za-z ]+)",

    "road_name":
        r"Road Name / Street Name\s*(.+)",

    "collision_type":
        r"Collision Type\s+([A-Za-z ]+)",

    "collision_nature":
        r"Collision Nature\s+([A-Za-z ]+)",

    "traffic_violation":
        r"\nTraffic Violation\s+([A-Za-z ]+)",

    "weather_condition":
        r"Weather Condition\s+([A-Za-z /]+)",

    "light_condition":
        r"Light Condition\s+([A-Za-z ]+)",

    "accident_spot":
        r"Accident Spot\s+([A-Za-z ]+)",

    "visibility":
        r"Visibility\s+(\d+)",

    "property_damage":
        r"Property Damage\s+(Yes|No)",

    "damage_value":
        r"Approximate Damage Value\s+(\d+)",

    # -----------------------------
    # VEHICLE DETAILS
    # -----------------------------

    "vehicle_reg_no":
        r"Vehicle Regn\. No\s+([A-Z0-9]+)",

    "vehicle_type":
        r"Vehicle Type\s*(.+)",

    "vehicle_category":
        r"Vehicle Category\s*(.+)",

    "vehicle_class":
        r"Vehicle Class\s+([A-Za-z() ]+)",

    "vehicle_color":
        r"Colour\s+([A-Z_]+)",

    "make_model":
        r"Make & Model\s+(.+)",

    "fuel_type":
        r"Fuel Type\s+([A-Za-z]+)",

    "seating_capacity":
        r"Seating Capacity\s+(\d+)",

    "vehicle_damage":
        r"Vehicle Damage\s+([A-Za-z, ]+)",

    "speed_limit":
        r"Vehicle Max\. Speed Limit\s+(\d+)",

    # -----------------------------
    # DRIVER DETAILS
    # -----------------------------

    "driver_gender":
        r"Gender\s+(Male|Female|Other)",

    "driver_age":
        r"Age\s+(\d+)",

    "education":
        r"Education\s+([A-Za-z ]+)",

    "occupation":
        r"Occupation\s+([A-Za-z ]+)",

    "nationality":
        r"Nationality\s+([A-Za-z ]+)",

    "license_type":
        r"Driving License Type\s+([A-Za-z ]+)",

    "license_status":
        r"Driving License Status\s+([A-Za-z. ]+)",

    "injury_type":
        r"Injury Type\s+([A-Za-z ]+)",

    # -----------------------------
    # VEHICLE CONDITION
    # -----------------------------

    "brake_condition":
        r"Condition of Brake\s+([A-Za-z ]+)",

    "steering_condition":
        r"Handle/Steering Condition\s+([A-Za-z ]+)",

    "tyre_condition":
        r"Tyre Condition\s+([A-Za-z ]+)",

    "mechanical_failure":
        r"Mechanical Failure Status\s+(yes|no)",
}


def merge_multiline_entries(text):

    lines = text.split("\n")

    merged_lines = []

    i = 0

    while i < len(lines):

        current_line = clean_value(lines[i])

        if not current_line:
            i += 1
            continue

        if i + 1 < len(lines):

            next_line = clean_value(lines[i + 1])

            if next_line:

                next_words = next_line.lower().split()

                current_words = current_line.split()

                if next_words and current_words:

                    first_word = next_words[0]

                    should_merge = (
                        current_line.endswith("/")
                        or (
                            len(current_words) <= 6
                            and current_line.endswith("Name")
                        )
                        or (
                            len(current_words) <= 6
                            and current_line.endswith("Type")
                        )
                        or (
                            first_word in MULTILINE_CONTINUATION_PREFIXES
                            and ":" not in next_line
                        )
                    )

                    next_line_has_new_field = (
                        re.match(
                            r"^[A-Z][A-Za-z /&().?-]{2,40}\s*:",
                            next_line
                        )
                        is not None
                    )

                    if should_merge and not next_line_has_new_field:

                        current_line = (
                            current_line
                            + " "
                            + next_line
                        )

                        i += 1

        merged_lines.append(current_line)

        i += 1

    return "\n".join(merged_lines)


def parse_crash_fields(text):

    extracted = {}

    text = merge_multiline_entries(text)

    detected_section = None

    for field, pattern in FIELD_PATTERNS.items():

        match = re.search(
            pattern,
            text
        )

        if match:

            extracted[field] = clean_value(
                match.group(1)
            )

        else:

            extracted[field] = None

    lines = text.split("\n")

    for line in lines:

        line = clean_value(line)

        if not line:
            continue

        lower_line = line.lower()

        reset_section = False

        for reset_pattern in SECTION_RESET_PATTERNS:

            if reset_pattern in lower_line:
                reset_section = True
                break

        if reset_section:
            detected_section = None

        if lower_line in SECTION_HEADERS:
            detected_section = lower_line
            continue

        matched_field = fuzzy_match_label(line)

        if matched_field is not None:

            if not extracted.get(matched_field):

                field_label = matched_field.replace("_", " ")

                lower_field_label = field_label.lower()

                lower_original_line = line.lower()

                if lower_field_label in lower_original_line:

                    split_index = lower_original_line.find(
                        lower_field_label
                    )

                    value = line[
                        split_index + len(field_label):
                    ].strip(" :-")

                    if is_valid_value(value):

                        extracted[matched_field] = clean_value(value)

        for generic_pattern in GENERIC_LABEL_PATTERNS:

            generic_match = re.match(
                generic_pattern,
                line
            )

            if generic_match is None:
                continue

            label = clean_value(
                generic_match.group(1)
            )

            value = clean_value(
                generic_match.group(2)
            )

            if not is_valid_label(label):
                continue

            if not is_valid_value(value):
                continue

            if value.lower() == label.lower():
                continue

            if len(value.split()) > 15:
                continue

            normalized_key = resolve_canonical_alias(label)

            if normalized_key in CANONICAL_FIELDS:
                continue

            if detected_section:
                normalized_key = (
                    normalize_key(detected_section)
                    + "__"
                    + normalized_key
                )

            key_suffix = normalized_key.split("__")[-1]

            resolved_suffix = resolve_canonical_alias(
                key_suffix
            )

            if resolved_suffix in CANONICAL_FIELDS:
                continue

            duplicate_found = False

            for existing_key, existing_value in extracted.items():

                if existing_value is None:
                    continue

                existing_clean = clean_value(
                    str(existing_value)
                ).lower()

                current_clean = clean_value(
                    str(value)
                ).lower()

                if existing_clean == current_clean:
                    duplicate_found = True
                    break

            if duplicate_found:
                continue

            existing_value = extracted.get(normalized_key)

            if existing_value:

                if len(existing_value) >= len(value):
                    continue

            extracted[normalized_key] = value

            break

    for key, value in extracted.items():

        if value is None:
            continue

        value = clean_value(value)

        if value.lower() in SECTION_HEADERS:
            extracted[key] = None
            continue

        if value.upper() == "NA":
            extracted[key] = None
            continue

        if not is_valid_value(value):
            extracted[key] = None
            continue

        if "__" in key:

            key_suffix = key.split("__")[-1]

            resolved_suffix = resolve_canonical_alias(
                key_suffix
            )

            if resolved_suffix in CANONICAL_FIELDS:
                extracted[key] = None
                continue

        value = value.strip("-:,. ")

        extracted[key] = normalize_field_value(
            key,
            value
        )

    cleaned_output = {}

    for key, value in extracted.items():

        if value is None:
            continue

        if isinstance(value, str):

            value = clean_value(value)

            if not value:
                continue

        cleaned_output[key] = value

    extracted = cleaned_output

    return extracted