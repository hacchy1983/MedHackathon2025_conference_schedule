import pandas as pd
from ics import Calendar, Event
from datetime import datetime
import pytz
import re

# タイムゾーンの設定
bkk_tz = pytz.timezone('Asia/Bangkok')

# CSVファイルの読み込み
df = pd.read_csv("Conference_Schedule.csv")

# カレンダーオブジェクトの作成
cal = Calendar()

# 序数を削除する関数 (3rd → 3)
def remove_ordinal_suffix(date_str):
    return re.sub(r'(\d{1,2})(st|nd|rd|th)', r'\1', date_str)

for index, row in df.iterrows():
    event = Event()
    event.name = row['Event']

    # 日付の序数を削除
    clean_date = remove_ordinal_suffix(row['Date'])

    # 時刻の形式を統一（1桁を2桁に変換）
    start_time = row['Start Time'].zfill(5)
    start_datetime_str = f"{clean_date} {start_time}"
    start_datetime = datetime.strptime(start_datetime_str, "%A, %d %B %Y %H:%M")
    start_datetime = bkk_tz.localize(start_datetime)  # タイムゾーンを設定
    event.begin = start_datetime

    if pd.notna(row['End Time']):
        end_time = row['End Time'].zfill(5)
        end_datetime_str = f"{clean_date} {end_time}"
        end_datetime = datetime.strptime(end_datetime_str, "%A, %d %B %Y %H:%M")
        end_datetime = bkk_tz.localize(end_datetime)  # タイムゾーンを設定
        event.end = end_datetime

    cal.events.add(event)

# カレンダーのタイムゾーン情報を設定
cal.events.add(event)

# カレンダーをICS形式で出力（タイムゾーン情報を手動で追加）
ics_content = cal.serialize()
ics_content = ics_content.replace("BEGIN:VCALENDAR", "BEGIN:VCALENDAR\nX-WR-TIMEZONE:Asia/Bangkok")

# ICSファイルの保存
with open("Conference_Schedule.ics", "w") as f:
    f.write(ics_content)
