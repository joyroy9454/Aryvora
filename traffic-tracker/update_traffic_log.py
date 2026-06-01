#!/usr/bin/env python3
"""
Aryvora Traffic Tracker
========================
Fill in weekly metrics manually from GoatCounter + Buttondown.
Run this script to generate summary stats and charts.

Usage:
  python3 update_traffic_log.py                    # Add a new week manually
  python3 update_traffic_log.py --auto             # Auto-fill from GoatCounter API (if configured)
  python3 update_traffic_log.py --summary          # Print summary stats
  python3 update_traffic_log.py --chart            # Generate a simple text chart
"""

import csv
import os
import sys
from datetime import datetime, timedelta

CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "traffic-log.csv")

# Column headers
HEADERS = [
    "week_start",          # Monday date (YYYY-MM-DD)
    "week_end",            # Sunday date (YYYY-MM-DD)
    "total_page_views",    # From GoatCounter
    "total_visitors",      # From GoatCounter
    "top_post_1",          # Title of most-viewed post
    "top_post_1_views",    # Its view count
    "top_post_2",          # Title of 2nd most-viewed post
    "top_post_2_views",
    "top_post_3",          # Title of 3rd most-viewed post
    "top_post_3_views",
    "newsletter_subs",     # Total Buttondown subscribers at end of week
    "new_subs_this_week",  # New subscribers gained
    "deals_page_clicks",   # From GoatCounter goal tracking
    "prompt_library_dl",   # Content upgrade conversions
    "notes",               # Any notes about the week
]


def init_csv():
    """Create the CSV file with headers if it does not exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)
        print(f"Created: {CSV_FILE}")
    else:
        print(f"Found: {CSV_FILE}")


def get_last_week_start():
    """Get the Monday of last week."""
    today = datetime.now().date()
    days_since_monday = today.weekday()
    last_monday = today - timedelta(days=days_since_monday + 7)
    return last_monday.strftime("%Y-%m-%d")


def add_week():
    """Interactively add a week of data."""
    init_csv()

    week_start = input(f"Week starting (YYYY-MM-DD) [{get_last_week_start()}]: ").strip()
    if not week_start:
        week_start = get_last_week_start()

    # Calculate Sunday
    monday = datetime.strptime(week_start, "%Y-%m-%d").date()
    sunday = monday + timedelta(days=6)
    week_end = sunday.strftime("%Y-%m-%d")

    print(f"\n--- Week: {week_start} to {week_end} ---\n")
    print("Enter metrics (press Enter to skip any field):\n")

    row = {"week_start": week_start, "week_end": week_end}

    for field in HEADERS[2:]:  # Skip week_start and week_end
        if field == "notes":
            val = input(f"  {field}: ").strip()
        else:
            val = input(f"  {field}: ").strip()
        row[field] = val

    # Write to CSV (append)
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writerow(row)

    print(f"\n✓ Saved week {week_start} to {CSV_FILE}")


def summary():
    """Print summary statistics from the CSV log."""
    init_csv()

    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("No data yet. Add your first week!")
        return

    weeks = len(rows)
    last = rows[-1]
    first = rows[0]

    # Calculate totals
    total_views = sum(int(r["total_page_views"] or 0) for r in rows)
    total_new_subs = sum(int(r["new_subs_this_week"] or 0) for r in rows)

    # Week-over-week for last two entries
    if len(rows) >= 2:
        prev = rows[-2]
        views_change = int(last["total_page_views"] or 0) - int(prev["total_page_views"] or 0)
        subs_change = int(last["new_subs_this_week"] or 0) - int(prev["new_subs_this_week"] or 0)
    else:
        views_change = 0
        subs_change = 0

    print("\n" + "=" * 60)
    print("  ARYVORA TRAFFIC SUMMARY")
    print("=" * 60)
    print(f"\n  Period:       {first['week_start']} to {last['week_end']}")
    print(f"  Weeks tracked: {weeks}")
    print()
    print(f"  Total page views:     {total_views:,}")
    print(f"  Total new subs:       {total_new_subs}")
    print(f"  Current subs:         {last['newsletter_subs']}")
    print()
    print(f"  Last week views:      {last['total_page_views']} ({views_change:+,} WoW)")
    print(f"  Last week new subs:   {last['new_subs_this_week']} ({subs_change:+,} WoW)")
    print(f"  Last week visitors:   {last['total_visitors']}")
    print()
    print(f"  Top post this week:   {last['top_post_1']} ({last['top_post_1_views']} views)")
    if last.get("notes"):
        print(f"  Notes: {last['notes']}")
    print("\n" + "=" * 60)

    # Weekly trend (last 8 weeks)
    if len(rows) > 1:
        recent = rows[-8:]
        max_views = max(int(r["total_page_views"] or 0) for r in recent)

        print("\n  Weekly Views (last {} weeks):".format(len(recent)))
        for r in recent:
            views = int(r["total_page_views"] or 0)
            bar_len = int(views / max(max_views, 1) * 30)
            bar = "█" * bar_len
            print(f"  {r['week_start']}  {bar} {views:,}")

        print()


def chart():
    """Generate a simple text-based chart of top posts."""
    init_csv()

    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("No data yet.")
        return

    print("\n" + "=" * 50)
    print("  TOP POSTS - LAST 4 WEEKS")
    print("=" * 50)

    recent = rows[-4:]
    all_posts = {}

    for r in recent:
        for i in range(1, 4):
            title = r.get(f"top_post_{i}", "")
            views = int(r.get(f"top_post_{i}_views", 0) or 0)
            if title and views > 0:
                if title not in all_posts:
                    all_posts[title] = []
                all_posts[title].append(views)

    # Sort by total views
    sorted_posts = sorted(all_posts.items(), key=lambda x: sum(x[1]), reverse=True)

    for title, views_list in sorted_posts[:10]:
        total = sum(views_list)
        avg = total // len(views_list)
        short_title = title[:40] + "..." if len(title) > 40 else title
        bar = "█" * min(int(avg / 50), 30)
        print(f"  {short_title}")
        print(f"  {bar} avg {avg:,}/week ({len(views_list)} weeks)")

    print()


if __name__ == "__main__":
    init_csv()

    if "--summary" in sys.argv:
        summary()
    elif "--chart" in sys.argv:
        chart()
    elif "--auto" in sys.argv:
        print("Auto-fill from GoatCounter API not yet configured.")
        print("Set GOATCOUNTER_API_KEY env var to enable.")
        add_week()
    else:
        add_week()
