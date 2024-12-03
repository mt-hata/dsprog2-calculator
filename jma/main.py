import json
import requests
import flet as ft
from datetime import datetime

# APIエンドポイント
AREA_JSON_URL = "http://www.jma.go.jp/bosai/common/const/area.json"
FORECAST_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast"

# 地域データの取得
def fetch_area_data():
    try:
        response = requests.get(AREA_JSON_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching area data: {e}")
        return {}

# 天気予報データの取得
def fetch_forecast_data(area_code):
    url = f"{FORECAST_URL}/{area_code}.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching forecast data: {e}")
        return None

# 日付を「2024年12月3日」の形式に変換
def format_date(date_str):
    try:
        date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return date_obj.strftime("%Y年%m月%d日")
    except Exception as e:
        print(f"Error formatting date: {e}")
        return date_str

# 天気アイコンを取得
def get_weather_icon(weather):
    icons = {
        "晴れ": "🌞",
        "曇り": "☁️",
        "雨": "🌧️",
        "雪": "❄️",
        "雷": "⚡",
        "風": "💨",
        "その他": "🌈"
    }
    return icons.get(weather, "🌈")  # デフォルトは虹のアイコン

# アプリのメインロジック
def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.scroll = "auto"  # 自動スクロールを有効にする
    page.spacing = 20  # コンテンツの間隔を広げる

    # サイドバー
    sidebar = ft.Column(
        [
            ft.ElevatedButton("メインメニュー", on_click=lambda _: show_main_menu()),
            ft.Divider(),
            ft.ElevatedButton("設定", on_click=lambda _: show_settings()),
        ],
        width=200,
        alignment=ft.MainAxisAlignment.START,
        scroll="auto",
    )

    # 地域データをロード
    area_data = fetch_area_data()
    if not area_data:
        page.controls.append(ft.Text("地域データの取得に失敗しました。"))
        page.update()
        return

    # 地方データ（親エリアコード）と県データ（子エリアコード）を取得
    centers = area_data.get("centers", {})
    offices = area_data.get("offices", {})

    def show_regions(center_id):
        """選択された地方の県リストを表示"""
        center_info = centers[center_id]
        child_codes = center_info.get("children", [])

        # 地方選択時の県リスト表示
        page.controls.clear()
        page.controls.append(sidebar)
        page.controls.append(ft.Text(f"{center_info['name']} の県リスト", style="headlineMedium"))

        for child_code in child_codes:
            if child_code in offices:
                office_info = offices[child_code]
                page.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(office_info["name"], style="headlineSmall"),
                                    ft.Text(office_info["officeName"], style="bodyMedium"),
                                    ft.ElevatedButton(
                                        "詳細を見る",
                                        on_click=lambda _, code=child_code: handle_office_click(code),
                                    ),
                                ],
                                spacing=10,
                                alignment="center",
                            ),
                            padding=10,
                        ),
                        elevation=2,
                    )
                )
        page.update()

    def handle_office_click(office_code):
        """県のボタンが押された際に天気予報を取得"""
        forecast_data = fetch_forecast_data(office_code)
        page.controls.clear()
        page.controls.append(sidebar)
        page.controls.append(ft.ElevatedButton("戻る", on_click=lambda _: show_regions(offices[office_code]["parent"])))

        if forecast_data:
            page.controls.append(ft.Text(f"{offices[office_code]['name']} の天気予報", style="headlineMedium"))

            # 日付ごとの天気データを取得
            time_series = forecast_data[0].get("timeSeries", [])
            time_defines = time_series[0].get("timeDefines", []) if time_series else []
            areas = time_series[0].get("areas", []) if time_series else []

            # 日付ごとの天気をカードで表示
            for idx, date in enumerate(time_defines):
                formatted_date = format_date(date)  # 日付をフォーマット
                page.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(f"日付: {formatted_date}", style="headlineSmall"),
                                    ft.Divider(),
                                    *[
                                        ft.Text(
                                            f"地域: {area['area']['name']}, 天気: {area.get('weathers', ['情報なし'])[idx]} {get_weather_icon(area.get('weathers', ['情報なし'])[idx])}"
                                        )
                                        for area in areas
                                    ],
                                ],
                                spacing=10,
                            ),
                            padding=10,
                        ),
                        elevation=3,
                    )
                )
        else:
            page.controls.append(ft.Text("天気予報データの取得に失敗しました。", style="headlineSmall"))

        page.update()

    def show_main_menu():
        """メインメニュー（地方リスト）を表示"""
        page.controls.clear()
        page.controls.append(sidebar)
        page.controls.append(ft.Text("地方を選択してください", style="headlineMedium"))

        for center_id, center_info in centers.items():
            page.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(center_info["name"], style="headlineSmall"),
                                ft.Text(center_info["officeName"], style="bodyMedium"),
                                ft.ElevatedButton(
                                    "地域を見る",
                                    on_click=lambda _, center_id=center_id: show_regions(center_id),
                                ),
                            ],
                            spacing=10,
                            alignment="center",
                        ),
                        padding=10,
                    ),
                    elevation=2,
                )
            )
        page.update()

    def show_settings():
        """設定画面（例: 言語選択など）"""
        page.controls.clear()
        page.controls.append(sidebar)
        page.controls.append(ft.Text("設定", style="headlineMedium"))
        page.controls.append(ft.Text("言語設定", style="bodyMedium"))
        page.controls.append(ft.ElevatedButton("英語", on_click=lambda _: change_language("en")))
        page.controls.append(ft.ElevatedButton("日本語", on_click=lambda _: change_language("jp")))
        page.update()

    def change_language(language):
        """言語変更（仮の処理）"""
        if language == "en":
            page.controls.append(ft.Text("Language changed to English.", style="headlineMedium"))
        else:
            page.controls.append(ft.Text("言語が日本語に変更されました。", style="headlineMedium"))
        page.update()

    # 初期画面を表示
    show_main_menu()

ft.app(target=main)
