# cli-mktstatus

Command line tool for querying market statistics from EVE Online market databases.

## Usage

```bash
mktstatus <db> [--type_id ID] [--type_name NAME] [--group_id ID] [--group_name NAME]
```

### Database Arguments
- `4H` - wcmktprod.db (production market)
- `B9` - wcmktnorth2.db (north region market)

### Query Filters (use one)
- `--type_id` - Filter by item type ID
- `--type_name` - Filter by item type name (partial match)
- `--group_id` - Filter by item group ID
- `--group_name` - Filter by item group name (partial match)

### Examples
```bash
mktstatus B9 --group_id 831
mktstatus 4H --type_name "Tritanium"
mktstatus B9 --group_name "Interceptor"
```

## Database Schema

The `marketstats` table contains:
- `type_id`, `type_name` - Item identifier and name
- `group_id`, `group_name` - Item group identifier and name
- `category_id`, `category_name` - Item category identifier and name
- `total_volume_remain` - Stock available
- `price`, `min_price`, `avg_price` - Pricing data
- `avg_volume` - Average trading volume
- `days_remaining` - Estimated days of stock remaining
- `last_update` - Last data refresh timestamp

## Development

```bash
uv sync
uv run mktstatus --help
```
