# Model Release Journal

An open, community-curated record of AI model releases.

- **Structured data**: one YAML file per model under [`models/`](models/).
- **Validated**: every entry is checked against [`schema/model.schema.json`](schema/model.schema.json) in CI.
- **Generated views**: [`INDEX.md`](INDEX.md) (all models, sortable by date or provider) and [`journal/`](journal/) (grouped by month) are rebuilt from the YAML — do not edit them by hand.

See [`INDEX.md`](INDEX.md) for the current list.

## Why

Model releases happen constantly. Pricing shifts, context windows expand, naming conventions drift. Storing this as structured data — not prose — makes it diffable, queryable, and durable.

## Schema

Each `models/<model_id>.yaml` entry has these fields (see [`schema/model.schema.json`](schema/model.schema.json) for the authoritative definition):

| Field | Required | Description |
|-------|----------|-------------|
| `model_id` | yes | Canonical slug, lowercase. Must match the filename stem. |
| `display_name` | no | Human-readable name. |
| `provider` | yes | Organization that serves the model. |
| `release_date` | yes | ISO 8601 date of public availability. |
| `context_window` | no | Input tokens (integer) or null. |
| `output_tokens_max` | no | Max output tokens per response. |
| `modalities` | no | Subset of `text, code, image, audio, video, pdf, embedding`. |
| `status` | no | `preview`, `stable` (default), `deprecated`, `retired`. |
| `supersedes` | no | `model_id` of the predecessor, if tracked here. |
| `pricing` | no | `{ input_per_mtok, output_per_mtok, cached_input_per_mtok }`. |
| `sources` | no | URLs of primary sources. |
| `tags` | no | Free-form labels. |
| `notes` | no | Short prose on what changed. |

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Short version:

```sh
cp models/TEMPLATE.yaml models/<model_id>.yaml
# edit fields
python -m venv .venv && .venv/bin/pip install pyyaml jsonschema
.venv/bin/python scripts/validate.py
.venv/bin/python scripts/build.py
git add models/ journal/ INDEX.md
```

## Repository layout

```
schema/model.schema.json   # JSON Schema for entries
models/<model_id>.yaml     # one file per model (source of truth)
models/TEMPLATE.yaml       # copy this to start a new entry
scripts/validate.py        # schema + sanity checks (CI enforces)
scripts/build.py           # regenerates journal/ and INDEX.md
journal/YYYY-MM.md         # generated monthly view
INDEX.md                   # generated global index
.github/workflows/         # CI
```

## License

MIT
