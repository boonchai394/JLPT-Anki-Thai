#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JLPT Kanji Anki Generator - Thai Edition

วิธีใช้:
1) ติดตั้ง Python 3
2) ถ้าอยากได้ไฟล์ .apkg ให้ติดตั้ง:
   pip install genanki
3) รัน:
   python build_decks.py

ผลลัพธ์:
- export_csv/*.csv  นำเข้า Anki ได้ทันที
- export_apkg/*.apkg ถ้ามี genanki
"""

import csv
from pathlib import Path

try:
    import genanki
except Exception:
    genanki = None

ROOT = Path(__file__).parent
CSV_DIR = ROOT / "export_csv"
APKG_DIR = ROOT / "export_apkg"
CSV_DIR.mkdir(exist_ok=True)
APKG_DIR.mkdir(exist_ok=True)

DATA = [
    {
        "kanji": "一", "level": "N5", "strokes": 1,
        "onyomi": "イチ・イツ", "kunyomi": "ひと・ひとつ",
        "meaning_th": "หนึ่ง",
        "vocab": [
            ("一つ", "ひとつ", "หนึ่งอัน"),
            ("一日", "いちにち", "หนึ่งวัน"),
            ("一人", "ひとり", "หนึ่งคน"),
            ("一番", "いちばん", "อันดับหนึ่ง / ที่สุด"),
            ("一月", "いちがつ", "มกราคม"),
        ],
        "examples": [
            ("一日に一時間、日本語を勉強します。", "いちにちに いちじかん、にほんごを べんきょうします。", "เรียนภาษาญี่ปุ่นวันละ 1 ชั่วโมง"),
            ("これは一番大切です。", "これは いちばん たいせつです。", "อันนี้สำคัญที่สุด"),
        ],
        "mnemonic": "一 = เส้นเดียว จำง่ายว่า 'หนึ่ง'",
    },
    {
        "kanji": "二", "level": "N5", "strokes": 2,
        "onyomi": "ニ", "kunyomi": "ふた・ふたつ",
        "meaning_th": "สอง",
        "vocab": [
            ("二つ", "ふたつ", "สองอัน"),
            ("二人", "ふたり", "สองคน"),
            ("二月", "にがつ", "กุมภาพันธ์"),
            ("二日", "ふつか", "วันที่ 2 / 2 วัน"),
            ("二枚", "にまい", "สองแผ่น"),
        ],
        "examples": [
            ("二枚分作ってください。", "にまいぶん つくってください。", "กรุณาทำสำหรับ 2 ผืน"),
            ("二人で行きます。", "ふたりで いきます。", "ไปกันสองคน"),
        ],
        "mnemonic": "二 = เส้นสองเส้น = สอง",
    },
    {
        "kanji": "三", "level": "N5", "strokes": 3,
        "onyomi": "サン", "kunyomi": "み・みっつ",
        "meaning_th": "สาม",
        "vocab": [
            ("三つ", "みっつ", "สามอัน"),
            ("三人", "さんにん", "สามคน"),
            ("三月", "さんがつ", "มีนาคม"),
            ("三日", "みっか", "วันที่ 3 / 3 วัน"),
            ("三回", "さんかい", "สามครั้ง"),
        ],
        "examples": [
            ("三回確認しました。", "さんかい かくにんしました。", "ตรวจสอบสามครั้งแล้ว"),
            ("三人で働いています。", "さんにんで はたらいています。", "ทำงานกันสามคน"),
        ],
        "mnemonic": "三 = เส้นสามเส้น = สาม",
    },
    {
        "kanji": "人", "level": "N5", "strokes": 2,
        "onyomi": "ジン・ニン", "kunyomi": "ひと",
        "meaning_th": "คน",
        "vocab": [
            ("人", "ひと", "คน"),
            ("日本人", "にほんじん", "คนญี่ปุ่น"),
            ("外国人", "がいこくじん", "ชาวต่างชาติ"),
            ("一人", "ひとり", "หนึ่งคน"),
            ("人気", "にんき", "ความนิยม"),
        ],
        "examples": [
            ("日本人の友達がいます。", "にほんじんの ともだちが います。", "มีเพื่อนคนญี่ปุ่น"),
            ("あそこに人がいます。", "あそこに ひとが います。", "ตรงนั้นมีคนอยู่"),
        ],
        "mnemonic": "人 = เหมือนคนยืนกางขา",
    },
    {
        "kanji": "日", "level": "N5", "strokes": 4,
        "onyomi": "ニチ・ジツ", "kunyomi": "ひ・か",
        "meaning_th": "วัน / พระอาทิตย์",
        "vocab": [
            ("日", "ひ", "วัน / พระอาทิตย์"),
            ("日本", "にほん", "ญี่ปุ่น"),
            ("毎日", "まいにち", "ทุกวัน"),
            ("日曜日", "にちようび", "วันอาทิตย์"),
            ("一日", "いちにち", "หนึ่งวัน"),
        ],
        "examples": [
            ("毎日、日本語を勉強します。", "まいにち、にほんごを べんきょうします。", "เรียนภาษาญี่ปุ่นทุกวัน"),
            ("今日は日差しが強いです。", "きょうは ひざしが つよいです。", "วันนี้แดดแรง"),
        ],
        "mnemonic": "日 = รูปพระอาทิตย์แบบสี่เหลี่ยม",
    },
]

LEVEL_ORDER = ["N5", "N4", "N3", "N2", "N1"]

def front_html(item):
    color = {"N5":"#2e7d32","N4":"#1565c0","N3":"#ef6c00","N2":"#c62828","N1":"#6a1b9a"}.get(item["level"], "#333")
    return f"""<div style="text-align:center;">
<div style="font-size:112px;font-weight:bold;line-height:1.0;">{item["kanji"]}</div>
<div style="font-size:22px;margin-top:8px;">{item["strokes"]}画</div>
<div style="font-size:18px;color:{color};font-weight:bold;margin-top:6px;">JLPT {item["level"]}</div>
</div>"""

def back_html(item):
    vocab_html = "<br>".join([f"{w}（{r}）<br>= {m}" for w, r, m in item["vocab"]])
    examples_html = "<br><br>".join([f"{s}<br>（{r}）<br>= {m}" for s, r, m in item["examples"]])
    return f"""<div style="text-align:center;font-size:72px;font-weight:bold;">{item["kanji"]}</div>
<div style="text-align:center;font-size:18px;">JLPT {item["level"]}・{item["strokes"]}画</div>
<hr>
<b>音読み</b><br>{item["onyomi"]}<br><br>
<b>訓読み</b><br>{item["kunyomi"]}<br><br>
<b>ความหมาย</b><br>{item["meaning_th"]}<br><br>
<b>คำศัพท์</b><br>{vocab_html}<br><br>
<b>例文</b><br>{examples_html}<br><br>
<b>Mnemonic</b><br>{item["mnemonic"]}"""

def export_csv():
    by_level = {lv: [] for lv in LEVEL_ORDER}
    for item in DATA:
        by_level[item["level"]].append(item)

    for lv, items in by_level.items():
        if not items:
            continue
        path = CSV_DIR / f"JLPT_{lv}_Kanji_Thai.csv"
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Front", "Back", "Tags"])
            for item in items:
                writer.writerow([front_html(item), back_html(item), f"JLPT::{lv} Kanji Stroke"])
        print("CSV:", path)

    all_path = CSV_DIR / "JLPT_N5-N1_Kanji_Thai_ALL.csv"
    with open(all_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Front", "Back", "Tags"])
        for item in DATA:
            writer.writerow([front_html(item), back_html(item), f"JLPT::{item['level']} Kanji Stroke"])
    print("CSV:", all_path)

def export_apkg():
    if genanki is None:
        print("genanki not installed. CSV files were created only.")
        return

    model = genanki.Model(
        2026070801,
        "JLPT Kanji Thai Model",
        fields=[
            {"name": "Front"},
            {"name": "Back"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Front}}",
                "afmt": "{{FrontSide}}<hr id='answer'>{{Back}}",
            },
        ],
    )

    by_level = {lv: [] for lv in LEVEL_ORDER}
    for item in DATA:
        by_level[item["level"]].append(item)

    for idx, lv in enumerate(LEVEL_ORDER, start=1):
        items = by_level[lv]
        if not items:
            continue
        deck = genanki.Deck(2026070800 + idx, f"JLPT {lv} Kanji Thai")
        for item in items:
            note = genanki.Note(
                model=model,
                fields=[front_html(item), back_html(item)],
                tags=[f"JLPT_{lv}", "Kanji", "Thai"],
            )
            deck.add_note(note)
        out = APKG_DIR / f"JLPT_{lv}_Kanji_Thai.apkg"
        genanki.Package(deck).write_to_file(out)
        print("APKG:", out)

if __name__ == "__main__":
    export_csv()
    export_apkg()
    print("Done.")
