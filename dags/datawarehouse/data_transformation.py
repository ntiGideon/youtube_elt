from datetime import timedelta, datetime


# use video's duration to determine the type of video whether short or long video
def parse_duration(duration_str):
    duration_str = duration_str.replace("P", "").replace("T", "")
    components = ["D", "H", "M", "S"]
    values = {"D": 0, "H": 0, "M": 0, "S": 0}

    for component in components:
        if component in duration_str:
            value, duration_str = duration_str.split(component)
            values[component] = int(value)

    total_duration = timedelta(
        days=values["D"], hours=values["H"], minutes=values["M"], seconds=values["S"]
    )
    return total_duration


def transform_data(row):
    duration_timedelta = parse_duration(row["Duration"])
    row["Duration"] = (datetime.min + duration_timedelta).time()
    row["Video_Type"] = "Shorts" if duration_timedelta.total_seconds() <= 60 else "Normal"

    return row
