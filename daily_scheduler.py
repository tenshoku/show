import datetime
import json
import os
from time import sleep

"""追加モジュール"""
import gspread
import schedule
from oauth2client.service_account import ServiceAccountCredentials

STATS_KEY = "STATS_KEY" # スプレッドシートのID
module_dir = os.path.dirname(__file__)

bot_list = [
    "bot1",
    "bot2",
    "bot3",
    "bot4",
    "bot5"
]
'''
サンプル
{
    "No.1": {"today_view": 0},
    "No.2": {"today_view": 0},
    "No.3": {"today_view": 0},
    "No.4": {"today_view": 0},
    "No.5": {"today_view": 0},
    "No.6": {"today_view": 0},
    "No.7": {"today_view": 0},
    "No.8": {"today_view": 0},
    "No.9": {"today_view": 0}
'''
def daily_scheduler():
    for bot in bot_list:

# 閲覧データが格納されているjsonをdictに
        json_open = open(module_dir + f"/{bot}.json", 'r', encoding="utf-8_sig")
        view_data = json.load(json_open)

#操作するスプレッドシートのアレコレ
        scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
        ca = ServiceAccountCredentials.from_json_keyfile_name(module_dir + "/analytics.json", scope)
        gs = gspread.authorize(ca)
        analytics_sheet = gs.open_by_key(STATS_KEY)
        stats_sheet = analytics_sheet.worksheet(bot)

# リストの先頭に日付の追加
        today = datetime.datetime.now()
        today = today.strftime("%Y/%m/%d")
        stats_list = ["(定期)"+today]
        num = 0
# viewer_{bot_list}.jsonからlist化
        for v in view_data.values():
            num += 1
            stats_list.append(v["today_view"])
            # 閲覧データの初期化
            view_data.update({f"No.{num}":{"today_view":0}})
            with open(module_dir + f"/{bot}.json", 'w', encoding='utf-8') as f:
                json.dump(view_data, f, indent=4, ensure_ascii=False)
# リストをコンソールに出力
        print(stats_list)
# 一括で指定シートに書き込み
        stats_sheet.append_row(stats_list)


# daily_scheduler()
# 毎日0時に定期実行
schedule.every().days.at("00:00").do(daily_scheduler)

while True:
    schedule.run_pending()
    sleep(1)
