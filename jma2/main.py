import sqlite3
import flet as ft
from datetime import datetime

DB_FILE = "/Users/hatakeyamaitsuki/dsprog2/jma2/weather_data.db"

# データベースから地域データを取得
def get_regions():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT region_id, region_name FROM region")
    regions = cursor.fetchall()
    conn.close()
    return regions

def get_prefectures(region_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT prefecture_id, prefecture_name FROM prefecture WHERE region_id = ?", (region_id,))
    prefectures = cursor.fetchall()
    conn.close()
    return prefectures

def get_areas(prefecture_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT areas_id, area_name FROM areas WHERE prefecture_id = ?", (prefecture_id,))
    areas = cursor.fetchall()
    conn.close()
    return areas

def get_weather(areas_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timeDefines, weatherCodes, weathers, winds, waves
        FROM weather WHERE areas_id = ?
    """, (areas_id,))
    weather_data = cursor.fetchall()
    conn.close()
    return weather_data

# 日付フォーマット関数
def format_date(date_str):
    try:
        date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return date_obj.strftime("%Y年%m月%d日")
    except Exception as e:
        return date_str

# アプリのメインロジック
def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.scroll = "auto"

    # スタックで画面の履歴を管理
    navigation_stack = []

    def navigate_to(view_func, *args):
        """指定の画面に遷移"""
        navigation_stack.append((view_func, args))
        view_func(*args)

    def go_back():
        """前の画面に戻る"""
        if len(navigation_stack) > 1:
            navigation_stack.pop()  # 現在の画面を削除
            prev_view_func, args = navigation_stack[-1]
            prev_view_func(*args)

    def show_regions():
        """地方選択画面"""
        page.controls.clear()
        regions = get_regions()
        page.controls.append(ft.Text("地方を選択してください", style="headlineMedium"))
        for region_id, region_name in regions:
            page.controls.append(
                ft.ElevatedButton(
                    region_name, on_click=lambda _, r_id=region_id: navigate_to(show_prefectures, r_id)
                )
            )
        page.update()

    def show_prefectures(region_id):
        """県選択画面"""
        page.controls.clear()
        prefectures = get_prefectures(region_id)
        page.controls.append(ft.ElevatedButton("戻る", on_click=lambda _: go_back()))
        page.controls.append(ft.Text("県を選択してください", style="headlineMedium"))
        for prefecture_id, prefecture_name in prefectures:
            page.controls.append(
                ft.ElevatedButton(
                    prefecture_name, on_click=lambda _, p_id=prefecture_id: navigate_to(show_areas, p_id)
                )
            )
        page.update()

    def show_areas(prefecture_id):
        """市町村選択画面"""
        page.controls.clear()
        areas = get_areas(prefecture_id)
        page.controls.append(ft.ElevatedButton("戻る", on_click=lambda _: go_back()))
        page.controls.append(ft.Text("市町村を選択してください", style="headlineMedium"))
        for areas_id, area_name in areas:
            page.controls.append(
                ft.ElevatedButton(
                    area_name, on_click=lambda _, a_id=areas_id: navigate_to(show_weather, a_id)
                )
            )
        page.update()

    def show_weather(areas_id):
        """天気予報画面"""
        page.controls.clear()
        weather_data = get_weather(areas_id)
        page.controls.append(ft.ElevatedButton("戻る", on_click=lambda _: go_back()))
        page.controls.append(ft.Text("天気予報", style="headlineMedium"))
        if weather_data:
            for record in weather_data:
                date, weather_code, weather, wind, wave = record
                page.controls.append(
                    ft.Card(
                        content=ft.Column(
                            [
                                ft.Text(f"日付: {format_date(date)}"),
                                ft.Text(f"天気: {weather}"),
                                ft.Text(f"風: {wind}"),
                                ft.Text(f"波: {wave}"),
                            ]
                        )
                    )
                )
        else:
            page.controls.append(ft.Text("天気データが見つかりませんでした。"))
        page.update()

    # 初期画面を表示
    navigate_to(show_regions)

ft.app(target=main)
