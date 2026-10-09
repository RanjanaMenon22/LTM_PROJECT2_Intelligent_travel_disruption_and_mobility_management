import pandas as pd
import json
import os


# ============================================================
# FILES TO INSPECT
# ============================================================

files = [
    "C:/Users/T10004/Desktop/Travel_disruption/Data/Attractions/places.csv",

    "C:/Users/T10004/Desktop/Travel_disruption/Data/Hotels/booking_com-travel_sample.csv",
    "C:/Users/T10004/Desktop/Travel_disruption/Data/Hotels/goibibo_com-travel_sample.csv",
    "C:/Users/T10004/Desktop/Travel_disruption/Data/Hotels/google_hotel_data_clean_v2.csv",
    "C:/Users/T10004/Desktop/Travel_disruption/Data/Hotels/hotel_details.csv",

    "C:/Users/T10004/Desktop/Travel_disruption/Data/Reviews/Review_db.csv",

    "C:/Users/T10004/Desktop/Travel_disruption/Data/transportation/Air_full-Raw.csv",
    "C:/Users/T10004/Desktop/Travel_disruption/Data/transportation/Air-Clean.csv",
    "C:/Users/T10004/Desktop/Travel_disruption/Data/transportation/Pan-India_Bus_Routes.csv",

    "C:/Users/T10004/Desktop/Travel_disruption/Data/transportation/schedules.json",
    "C:/Users/T10004/Desktop/Travel_disruption/Data/transportation/stations.json",
    "C:/Users/T10004/Desktop/Travel_disruption/Data/transportation/trains.json"
]


# ============================================================
# SAFE CSV READER
# ============================================================

def read_csv_safely(file):

    encodings = [
        "utf-8",
        "utf-8-sig",
        "cp1252",
        "latin1"
    ]

    for encoding in encodings:

        try:
            df = pd.read_csv(
                file,
                encoding=encoding
            )

            print(f"Encoding used: {encoding}")

            return df

        except UnicodeDecodeError:
            continue

    raise ValueError(
        "Could not read CSV because of encoding."
    )


# ============================================================
# INSPECT FILES
# ============================================================

for file in files:

    print("\n" + "=" * 60)
    print(file)
    print("=" * 60)

    # --------------------------------------------------------
    # Check whether file exists
    # --------------------------------------------------------

    if not os.path.exists(file):

        print("❌ FILE NOT FOUND")

        continue

    try:

        # ====================================================
        # CSV
        # ====================================================

        if file.lower().endswith(".csv"):

            df = read_csv_safely(file)

            print("✅ CSV loaded successfully")

            print("Rows:", len(df))

            print("Columns:", len(df.columns))

            print("\nColumn names:")

            for column in df.columns:

                print(" -", column)

            print("\nFirst 3 rows:")

            print(
                df.head(3).to_string()
            )

        # ====================================================
        # JSON
        # ====================================================

        elif file.lower().endswith(".json"):

            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            print("✅ JSON loaded successfully")

            print(
                "Data type:",
                type(data)
            )

            if isinstance(data, list):

                print(
                    "Number of records:",
                    len(data)
                )

                if len(data) > 0:

                    print(
                        "\nFirst record:"
                    )

                    print(data[0])

            elif isinstance(data, dict):

                print(
                    "\nDictionary keys:"
                )

                for key in list(data.keys())[:30]:

                    print(" -", key)

    except Exception as e:

        print("❌ ERROR:")
        print(e)


# ============================================================
# FINISHED
# ============================================================

print("\n")
print("=" * 60)
print("DATASET INSPECTION COMPLETED")
print("=" * 60)