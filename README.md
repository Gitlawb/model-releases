# Model Release Journal

An open, community-curated journal tracking model releases across the AI landscape.

## Why?

Model releases happen constantly. Pricing changes, context windows expand, new capabilities drop. This journal exists to create a durable, diffable, community-editable record.

## Schema

Each entry tracks:

| Field | Description |
|-------|-------------|
| `model_id` | The exact model identifier (e.g., `claude-sonnet-4-6`, `gpt-4.5`) |
| `provider` | The serving provider (e.g., `Anthropic`, `OpenAI`, `xAI`) |
| `release_date` | ISO 8601 date (`YYYY-MM-DD`) |
| `context_window` | Context window in tokens (e.g., `200000`) |
| `modalities` | Comma-separated list (e.g., `text, image, audio`) |
| `x_post` | Link to the official X/Twitter announcement post |
| `notes` | What changed, why it matters |

## Contributing

1. Add an entry to `journal/YYYY-MM.md`
2. Keep entries in reverse chronological order (newest first)
3. Include the X post link when available — it is the primary source

## License

MIT
