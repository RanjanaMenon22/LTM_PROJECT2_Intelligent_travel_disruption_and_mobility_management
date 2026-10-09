import pandas as pd
import os


# ============================================================
# CREATE PROCESSED DIRECTORIES
# ============================================================

folders = [
    "Data/processed/attractions",
    "Data/processed/hotels",
    "Data/processed/reviews",
    "Data/processed/transportation",
    "Data/processed/weather"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)


# ============================================================
# FUNCTION TO READ CSV SAFELY
# ============================================================

def read_csv_safely(path):

    encodings = [
        "utf-8",
        "utf-8-sig",
        "cp1252",
        "latin1"
    ]

    for encoding in encodings:

        try:
            df = pd.read_csv(
                path,
                encoding=encoding
            )

            print(f"Loaded: {path}")
            print(f"Encoding: {encoding}")

            return df

        except UnicodeDecodeError:
            continue

    raise Exception(
        f"Unable to read: {path}"
    )


# ============================================================
# 1. ATTRACTIONS
# ============================================================

print("\n" + "=" * 60)
print("PROCESSING ATTRACTIONS")
print("=" * 60)

attractions_path = (
    "Data/Attractions/places.csv"
)

if os.path.exists(attractions_path):

    df = read_csv_safely(
        attractions_path
    )

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove rows without place name
    if "Name" in df.columns:
        df = df.dropna(subset=["Name"])

    output = (
        "Data/processed/"
        "attractions/attractions_clean.csv"
    )

    df.to_csv(
        output,
        index=False
    )

    print("Saved:", output)
    print("Rows:", len(df))

else:

    print("Attractions file not found")


# ============================================================
# 2. HOTELS
# ============================================================

print("\n" + "=" * 60)
print("PROCESSING HOTELS")
print("=" * 60)

hotel_path = (
    "Data/Hotels/"
    "google_hotel_data_clean_v2.csv"
)

if os.path.exists(hotel_path):

    df = read_csv_safely(
        hotel_path
    )

    df = df.drop_duplicates()
    df = df.dropna(how="all")

    # Remove hotels without names
    if "Hotel_Name" in df.columns:
        df = df.dropna(
            subset=["Hotel_Name"]
        )

    # Convert price to numeric if available
    if "Hotel_Price" in df.columns:

        df["Hotel_Price"] = pd.to_numeric(
            df["Hotel_Price"],
            errors="coerce"
        )

    output = (
        "Data/processed/"
        "hotels/hotels_clean.csv"
    )

    df.to_csv(
        output,
        index=False
    )

    print("Saved:", output)
    print("Rows:", len(df))

else:

    print("Hotel file not found")


# ============================================================
# 3. REVIEWS
# ============================================================

print("\n" + "=" * 60)
print("PROCESSING REVIEWS")
print("=" * 60)

review_path = (
    "Data/Reviews/Review_db.csv"
)

if os.path.exists(review_path):

    df = read_csv_safely(
        review_path
    )

    print(
        "Original review rows:",
        len(df)
    )

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove empty reviews
    if "Review" in df.columns:

        df = df.dropna(
            subset=["Review"]
        )

        df["Review"] = (
            df["Review"]
            .astype(str)
            .str.strip()
        )

        df = df[
            df["Review"] != ""
        ]

    # --------------------------------------------------------
    # IMPORTANT
    # Don't create embeddings for 1.4M+ reviews initially.
    # Sample a manageable amount.
    # --------------------------------------------------------

    max_reviews = 100000

    if len(df) > max_reviews:

        df = df.sample(
            n=max_reviews,
            random_state=42
        )

    output = (
        "Data/processed/"
        "reviews/reviews_clean.csv"
    )

    df.to_csv(
        output,
        index=False
    )

    print("Saved:", output)
    print(
        "Final review rows:",
        len(df)
    )

else:

    print("Review file not found")


# ============================================================
# 4. FLIGHTS
# ============================================================

print("\n" + "=" * 60)
print("PROCESSING FLIGHTS")
print("=" * 60)

flight_path = (
    "Data/transportation/"
    "Air-Clean.csv"
)

if os.path.exists(flight_path):

    df = read_csv_safely(
        flight_path
    )

    df = df.drop_duplicates()
    df = df.dropna(how="all")

    # Remove records without origin/destination
    required = [
        "origin",
        "destination"
    ]

    existing = [
        col for col in required
        if col in df.columns
    ]

    if existing:

        df = df.dropna(
            subset=existing
        )

    output = (
        "Data/processed/"
        "transportation/flights_clean.csv"
    )

    df.to_csv(
        output,
        index=False
    )

    print("Saved:", output)
    print("Rows:", len(df))

else:

    print("Flight file not found")


# ============================================================
# 5. BUS
# ============================================================

print("\n" + "=" * 60)
print("PROCESSING BUS ROUTES")
print("=" * 60)

bus_path = (
    "Data/transportation/"
    "Pan-India_Bus_Routes.csv"
)

if os.path.exists(bus_path):

    df = read_csv_safely(
        bus_path
    )

    df = df.drop_duplicates()
    df = df.dropna(how="all")

    output = (
        "Data/processed/"
        "transportation/bus_routes_clean.csv"
    )

    df.to_csv(
        output,
        index=False
    )

    print("Saved:", output)
    print("Rows:", len(df))

else:

    print("Bus file not found")


# ============================================================
# FINISHED
# ============================================================

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED")
print("=" * 60)