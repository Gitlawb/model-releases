# Contributing

Thanks for helping keep the journal accurate.

## Adding a new model

1. Copy `models/TEMPLATE.yaml` to `models/<model_id>.yaml`. The filename
   stem must equal the `model_id` field (the validator enforces this).
2. Fill in as much as you know. Fields you're unsure about can stay `null`
   — a sparse entry is fine, a wrong entry is not.
3. Add at least one URL in `sources` pointing to a primary source (the
   official announcement post, the provider's model card, or the API docs).
4. Run the toolchain locally:
   ```sh
   python -m venv .venv
   .venv/bin/pip install pyyaml jsonschema
   .venv/bin/python scripts/validate.py
   .venv/bin/python scripts/build.py
   ```
5. Commit the new YAML **and** the regenerated `journal/*.md` and
   `INDEX.md`. CI will reject PRs where generated files drift from the
   YAML.
6. Open a PR. The template has a checklist.

## Correcting an existing model

Edit the YAML under `models/`. Don't edit `journal/*.md` or `INDEX.md` by
hand — they're regenerated from the YAML.

## Schema changes

Changes to `schema/model.schema.json` are welcome but require:
- Migration of every existing `models/*.yaml` in the same PR.
- A note in the PR description explaining why the change is necessary.

## What belongs here

- New model releases from any provider.
- Material updates to existing entries (pricing change, new modality,
  context-window bump, deprecation).
- Corrections.

## What doesn't

- Benchmarks and subjective reviews — this is a release record, not a
  leaderboard.
- Rumors or leaks without a primary source.
