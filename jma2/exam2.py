import sqlite3
import csv
import json

# ファイルパス
CSV_FILE = "/Users/hatakeyamaitsuki/dsprog2/jma2/japan_weather_forecast.csv"
AREA_JSON = "/Users/hatakeyamaitsuki/dsprog2/jma2/area.json"
DB_FILE = "/Users/hatakeyamaitsuki/dsprog2/jma2/weather_data.db"

# データベースを作成
def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # regionテーブル
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS region (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region_id TEXT UNIQUE NOT NULL,
            region_name TEXT NOT NULL
        )
    """)

    # prefectureテーブル
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prefecture (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region_id TEXT NOT NULL,
            prefecture_id TEXT UNIQUE NOT NULL,
            prefecture_name TEXT NOT NULL,
            FOREIGN KEY (region_id) REFERENCES region (region_id)
        )
    """)

    # areasテーブル
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS areas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prefecture_id TEXT NOT NULL,
            areas_id TEXT UNIQUE NOT NULL,
            area_name TEXT NOT NULL,
            FOREIGN KEY (prefecture_id) REFERENCES prefecture (prefecture_id)
        )
    """)

    # weatherテーブル
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            areas_id TEXT NOT NULL,
            weather_id TEXT UNIQUE NOT NULL,
            timeDefines TEXT NOT NULL,
            area_name TEXT NOT NULL,
            weatherCodes TEXT NOT NULL,
            weathers TEXT NOT NULL,
            winds TEXT NOT NULL,
            waves TEXT NOT NULL,
            FOREIGN KEY (areas_id) REFERENCES areas (areas_id)
        )
    """)

    conn.commit()
    conn.close()

# データを挿入
def populate_database():
    with open(AREA_JSON, "r", encoding="utf-8") as area_file:
        area_data = json.load(area_file)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # regionテーブルを埋める
    for region_id, region_info in area_data["centers"].items():
        cursor.execute("""
            INSERT OR IGNORE INTO region (region_id, region_name)
            VALUES (?, ?)
        """, (region_id, region_info["name"]))

    # prefectureテーブルを埋める
    for prefecture_id, prefecture_info in area_data["offices"].items():
        region_id = prefecture_info["parent"]
        cursor.execute("""
            INSERT OR IGNORE INTO prefecture (region_id, prefecture_id, prefecture_name)
            VALUES (?, ?, ?)
        """, (region_id, prefecture_id, prefecture_info["name"]))

    # areasテーブルを埋める
    for area_id, area_info in area_data["class10s"].items():
        prefecture_id = area_info["parent"]
        cursor.execute("""
            INSERT OR IGNORE INTO areas (prefecture_id, areas_id, area_name)
            VALUES (?, ?, ?)
        """, (prefecture_id, area_id, area_info["name"]))

    # weatherテーブルを埋める
    with open(CSV_FILE, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # weather_idを生成
            weather_id = f"{row['areas']}_{row['timeDefines']}"
            cursor.execute("""
                INSERT OR IGNORE INTO weather (
                    areas_id, weather_id, timeDefines, area_name,
                    weatherCodes, weathers, winds, waves
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["areas"],
                weather_id,
                row["timeDefines"],
                row["areas"],
                row["weatherCodes"],
                row["weathers"],
                row["winds"],
                row["waves"]
            ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    populate_database()
    print(f"データベース {DB_FILE} が作成されました。")
