#!/usr/bin/env python3
"""Create calculator tables if migrate could not run (e.g. runserver holds SQLite lock)."""
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db.sqlite3"

SQL = """
CREATE TABLE IF NOT EXISTS "main_calculatorconfig" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "area_min" integer unsigned NOT NULL,
    "area_max" integer unsigned NOT NULL,
    "area_step" integer unsigned NOT NULL,
    "area_default" integer unsigned NOT NULL
);
CREATE TABLE IF NOT EXISTS "main_calculatormaterial" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "key" varchar(32) NOT NULL UNIQUE,
    "label" varchar(120) NOT NULL,
    "price_per_sqm" integer unsigned NOT NULL,
    "sort_order" integer NOT NULL,
    "is_active" bool NOT NULL
);
"""

SEED_CONFIG = (1, 20, 300, 5, 75)
SEED_MATERIALS = [
    ("srub", "Сруб (бревенчатый)", 1200, 0, 1),
    ("brus", "Дом из бруса", 1100, 1, 1),
    ("kleen", "Клееный брус", 1000, 2, 1),
    ("banya", "Баня/сауна", 1500, 3, 1),
]


def main():
    if not DB.exists():
        print(f"Database not found: {DB}")
        print("Run: python manage.py migrate")
        return 1

    conn = sqlite3.connect(DB, timeout=60)
    try:
        conn.executescript(SQL)
        conn.execute(
            "INSERT OR IGNORE INTO main_calculatorconfig "
            "(id, area_min, area_max, area_step, area_default) VALUES (?, ?, ?, ?, ?)",
            SEED_CONFIG,
        )
        for row in SEED_MATERIALS:
            conn.execute(
                "INSERT OR IGNORE INTO main_calculatormaterial "
                "(key, label, price_per_sqm, sort_order, is_active) VALUES (?, ?, ?, ?, ?)",
                row,
            )
        conn.execute(
            "INSERT OR IGNORE INTO django_migrations (app, name, applied) VALUES (?, ?, ?)",
            ("main", "0002_calculator", datetime.utcnow().isoformat(" ")),
        )
        conn.commit()
        print("Calculator tables ready:", DB)
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
