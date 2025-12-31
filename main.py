#!/usr/bin/env python3
"""CLI tool for querying EVE Online market statistics."""

import argparse
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

from tabulate import tabulate

DB_MAP = {
    "4H": "wcmktprod.db",
    "B9": "wcmktnorth2.db",
}


def format_number(value: int | float) -> str:
    """Format number with thousand separators."""
    if isinstance(value, float):
        return f"{value:,.0f}"
    return f"{value:,}"


def format_timestamp(ts_str: str) -> str:
    """Round timestamp to nearest minute."""
    try:
        dt = datetime.fromisoformat(ts_str)
        # Round seconds to nearest minute
        if dt.second >= 30:
            dt = dt.replace(second=0, microsecond=0)
            dt = dt.replace(minute=dt.minute + 1)
        else:
            dt = dt.replace(second=0, microsecond=0)
        return dt.strftime("%Y-%m-%d %H:%M")
    except (ValueError, TypeError):
        return ts_str


def query_market(db_path: Path, filter_type: str, filter_value: str | int) -> list[tuple]:
    """Query marketstats table with the given filter."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if filter_type in ("type_id", "group_id"):
        where_clause = f"{filter_type} = ?"
        params = (int(filter_value),)
    else:
        where_clause = f"{filter_type} LIKE ?"
        params = (f"%{filter_value}%",)

    query = f"""
        SELECT type_name, group_name, total_volume_remain, ROUND(price, 0), last_update
        FROM marketstats
        WHERE {where_clause}
        ORDER BY group_name, type_name
    """

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Query market statistics from EVE Online market databases.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mktstatus B9 --group_id 831
  mktstatus 4H --type_name Tritanium
  mktstatus B9 --group_name Interceptor
        """,
    )

    parser.add_argument(
        "db",
        type=str.upper,
        metavar="DB",
        help="Database to query (4H=wcmktprod.db, B9=wcmktnorth2.db)",
    )

    filter_group = parser.add_mutually_exclusive_group(required=True)
    filter_group.add_argument("--type_id", type=int, help="Filter by type ID")
    filter_group.add_argument("--type_name", type=str, help="Filter by type name (partial match)")
    filter_group.add_argument("--group_id", type=int, help="Filter by group ID")
    filter_group.add_argument("--group_name", type=str, help="Filter by group name (partial match)")

    args = parser.parse_args()

    if args.db not in DB_MAP:
        parser.error(f"invalid db: {args.db} (choose from 4H, B9)")

    # Determine database path
    script_dir = Path(__file__).parent
    db_file = DB_MAP[args.db]
    db_path = script_dir / db_file

    if not db_path.exists():
        print(f"Error: Database not found: {db_path}", file=sys.stderr)
        sys.exit(1)

    # Determine filter
    if args.type_id is not None:
        filter_type, filter_value = "type_id", args.type_id
    elif args.type_name is not None:
        filter_type, filter_value = "type_name", args.type_name
    elif args.group_id is not None:
        filter_type, filter_value = "group_id", args.group_id
    else:
        filter_type, filter_value = "group_name", args.group_name

    # Query database
    results = query_market(db_path, filter_type, filter_value)

    if not results:
        print("No results found.")
        sys.exit(0)

    # Format results
    formatted = []
    for type_name, group_name, stock, price, last_update in results:
        formatted.append([
            type_name,
            group_name,
            format_number(stock),
            format_number(price),
            format_timestamp(last_update),
        ])

    headers = ["Type", "Group", "Stock", "Price", "Last Update"]
    print(tabulate(formatted, headers=headers, tablefmt="simple"))


if __name__ == "__main__":
    main()
