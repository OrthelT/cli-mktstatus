# cli-mktstatus

A command-line tool for querying market statistics from EVE Online market databases. This tool provides quick access to market data including prices, stock levels, and market activity for items in your EVE Online market databases.

## Features

- 🔍 **Flexible Filtering** - Query by item type ID/name or group ID/name with partial matching
- 📊 **Clean Output** - Formatted tables with thousand separators and readable timestamps
- 🚀 **Fast Queries** - Direct SQLite database access for instant results
- 🎯 **Multiple Databases** - Support for multiple market database instances
- 💼 **Case-Insensitive** - Database arguments accept uppercase or lowercase

## Installation

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cli-mktstatus.git
   cd cli-mktstatus
   ```

2. **Install dependencies**

   Using uv (recommended):
   ```bash
   uv sync
   ```

   Using pip:
   ```bash
   pip install -e .
   ```

3. **Set up your database files**

   Place your EVE Online market database files in the project root directory. The tool expects SQLite database files named according to the database map (see Configuration below).

   Your database files should contain a `marketstats` table with the schema described below.

4. **Configure database mappings** (optional)

   Edit `main.py` to customize the database mappings in the `DB_MAP` dictionary:
   ```python
   DB_MAP = {
       "4H": "wcmktprod.db",      # Your production market database
       "B9": "wcmktnorth2.db",     # Your regional market database
   }
   ```

   Add or modify entries to match your database files and preferred shorthand names.

## Usage

### Basic Syntax

```bash
mktstatus <DB> [--type_id ID] [--type_name NAME] [--group_id ID] [--group_name NAME]
```

### Database Arguments

The database argument uses the shorthand codes defined in `DB_MAP`:

- `4H` (or `4h`) - wcmktprod.db (production market)
- `B9` (or `b9`) - wcmktnorth2.db (north region market)

Arguments are case-insensitive, so `4H`, `4h`, `B9`, and `b9` all work.

### Query Filters

You must specify exactly one filter option:

| Option | Type | Description |
|--------|------|-------------|
| `--type_id` | Integer | Filter by exact item type ID |
| `--type_name` | String | Filter by item type name (case-insensitive partial match) |
| `--group_id` | Integer | Filter by exact item group ID |
| `--group_name` | String | Filter by item group name (case-insensitive partial match) |

### Examples

**Query a specific item group by ID:**
```bash
mktstatus B9 --group_id 831
```

**Search for items by name (partial match):**
```bash
mktstatus 4H --type_name "Tritanium"
mktstatus 4h --type_name trit        # Case-insensitive, partial match
```

**Find all items in a group by name:**
```bash
mktstatus B9 --group_name "Interceptor"
mktstatus b9 --group_name inter      # Partial match works
```

**Query a specific item by type ID:**
```bash
mktstatus 4H --type_id 34
```

### Sample Output

```
Type                    Group           Stock      Price  Last Update
----------------------  ------------  -------  ---------  ---------------
Republic Fleet Firetail  Assault Ship   12,450  45,000,000  2025-12-31 14:30
Imperial Navy Slicer    Assault Ship    8,320  48,500,000  2025-12-31 14:30
```

## Database Schema

Your SQLite database must contain a `marketstats` table with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `type_id` | INTEGER | Unique item type identifier (Primary Key) |
| `type_name` | VARCHAR | Item name |
| `group_id` | INTEGER | Item group identifier |
| `group_name` | VARCHAR | Item group name |
| `category_id` | INTEGER | Item category identifier |
| `category_name` | VARCHAR | Item category name |
| `total_volume_remain` | INTEGER | Total stock available across all orders |
| `price` | FLOAT | Current market price |
| `min_price` | FLOAT | Minimum price in market |
| `avg_price` | FLOAT | Average price |
| `avg_volume` | FLOAT | Average trading volume |
| `days_remaining` | FLOAT | Estimated days of stock remaining |
| `last_update` | DATETIME | Last data refresh timestamp |

The tool queries and displays: `type_name`, `group_name`, `total_volume_remain`, `price` (rounded), and `last_update` (rounded to nearest minute).

## Development

### Running from source

```bash
# Using uv
uv run mktstatus --help

# Or activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
mktstatus --help
```

### Project Structure

```
cli-mktstatus/
├── main.py              # Main application code
├── pyproject.toml       # Project configuration and dependencies
├── CLAUDE.md           # Development documentation
├── README.md           # This file
├── *.db                # Your market database files (gitignored)
└── .venv/              # Virtual environment (gitignored)
```

### Dependencies

- **tabulate** (≥0.9.0) - For formatted table output

### Making Changes

1. The entry point is defined in `pyproject.toml` under `[project.scripts]`
2. Database mappings are in the `DB_MAP` dictionary in `main.py`
3. Query logic is in the `query_market()` function
4. Output formatting happens in the `main()` function

## Customization for Your Workflow

### Adding New Databases

1. Add your database file to the project root
2. Update the `DB_MAP` in `main.py`:
   ```python
   DB_MAP = {
       "4H": "wcmktprod.db",
       "B9": "wcmktnorth2.db",
       "XY": "your_custom_db.db",  # Add your database
   }
   ```
3. Use your new shorthand code: `mktstatus XY --type_name "Tritanium"`

### Modifying Output Columns

Edit the query in `query_market()` function (line 52-57 in main.py) to select different columns, and update the formatting in `main()` (line 122-133).

### Changing Output Format

The tool uses the `tabulate` library. You can change the table format by modifying the `tablefmt` parameter in main.py:133:

```python
print(tabulate(formatted, headers=headers, tablefmt="grid"))  # or "pipe", "github", etc.
```

## Troubleshooting

**Database not found error:**
- Ensure your database files are in the project root directory
- Check that filenames in `DB_MAP` match your actual files
- Database files are gitignored, so they won't be in version control

**No results found:**
- Try using partial name matches instead of exact matches
- Check your filter values are correct
- Verify the database contains data for your query

**Import errors:**
- Run `uv sync` to ensure dependencies are installed
- Make sure you're using Python 3.13 or higher

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
