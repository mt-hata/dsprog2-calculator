import sqlite3
import csv
import json

# JSONファイルを読み込む
def load_area_data(json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)

# SQLiteデータベースを作成し、テーブルを定義する
def create_database(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # regionテーブル
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS region (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region_id TEXT UNIQUE,
            region_name TEXT,
            prefecture_id TEXT UNIQUE
        )
    """)

    # prefectureテーブル
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prefecture (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prefecture_id TEXT UNIQUE,
            prefecture_name TEXT,
            areas_id TEXT UNIQUE
        )
    """)

    # areasテーブル
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS areas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            areas_id TEXT UNIQUE,
            area_name TEXT,
            weather_id INTEGER UNIQUE
        )
    """)

    # weatherテーブル
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            weather_id INTEGER UNIQUE,
            time_defines TEXT,
            area_name TEXT,
            weather_codes TEXT,
            weathers TEXT,
            winds TEXT,
            waves TEXT
        )
    """)

    conn.commit()
    return conn, cursor

# CSVデータを挿入する
def insert_data(conn, cursor, area_json, csv_path):
    with open(csv_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        area_data = load_area_data(area_json)

        centers = area_data.get("centers", {})
        offices = area_data.get("offices", {})

        region_map = {center_id: center["name"] for center_id, center in centers.items()}
        prefecture_map = {office_id: office["name"] for office_id, office in offices.items()}

        weather_id = 1  # weatherテーブル用のID
        for row in reader:
            region_name = row["region"]
            prefecture_name = row["prefecture"]
            area_name = row["areas"]
            time_defines = row["timeDefines"]
            weather_codes = row["weatherCodes"]
            weathers = row["weathers"]
            winds = row["winds"]
            waves = row["waves"]

            # region_id取得
            region_id = next((key for key, name in region_map.items() if name == region_name), None)
            # prefecture_id取得
            prefecture_id = next((key for key, name in prefecture_map.items() if name == prefecture_name), None)

            # areas_id取得
            areas_id = next((key for key, area in area_data.get("class10s", {}).items()
                            if area["name"] == area_name and area["parent"] == prefecture_id), None)

            # regionデータ挿入
            if region_id and prefecture_id:
                cursor.execute("""
                    INSERT OR IGNORE INTO region (region_id, region_name, prefecture_id)
                    VALUES (?, ?, ?)
                """, (region_id, region_name, prefecture_id))

            # prefectureデータ挿入
            if prefecture_id and areas_id:
                cursor.execute("""
                    INSERT OR IGNORE INTO prefecture (prefecture_id, prefecture_name, areas_id)
                    VALUES (?, ?, ?)
                """, (prefecture_id, prefecture_name, areas_id))

            # areasデータ挿入
            if areas_id:
                cursor.execute("""
                    INSERT OR IGNORE INTO areas (areas_id, area_name, weather_id)
                    VALUES (?, ?, ?)
                """, (areas_id, area_name, weather_id))

            # weatherデータ挿入
            cursor.execute("""
                INSERT OR IGNORE INTO weather (weather_id, time_defines, area_name, weather_codes, weathers, winds, waves)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (weather_id, time_defines, area_name, weather_codes, weathers, winds, waves))

            weather_id += 1

    conn.commit()

if __name__ == "__main__":
    # ファイルパス
    db_file = "/Users/hatakeyamaitsuki/dsprog2/jma2/weather_database.db"  # データベースファイルのフルパス
    area_json_path = "/Users/hatakeyamaitsuki/dsprog2/jma2/area.json"  # JSONファイルのフルパス
    csv_path = "/Users/hatakeyamaitsuki/dsprog2/jma2/japan_weather_forecast.csv"  # CSVファイルのフルパス

    # データベースの作成とデータの挿入
    conn, cursor = create_database(db_file)
    insert_data(conn, cursor, area_json_path, csv_path)

    print(f"{db_file} にデータベースが作成されました。")
    conn.close()
