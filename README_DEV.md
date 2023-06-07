# Developer Notes

These are here to help me remember how to do things.

## Setup Dev Environment

- `python3 -m pip install poetry`
- `poetry install`

## Update version

### Uses bump2version

- `bump2version patch --verbose --dry-run`

## Build

- `doit`

## Docs

Will be built as part of `doit` but can be built separately with:

- `mkdocs build`

Can be served locally with:

- `mkdocs serve`

## Updating README.md

Do not directly edit README.md, instead edit README.mdpp and process with MarkdownPP using `doit` to update README.md