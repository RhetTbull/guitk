# Developer Notes

These are here to help me remember how to do things.

## Setup Dev Environment

- `python3 -m pip install poetry`
- `poetry install`

## Update version

### Uses bump2version

- `bump2version patch --verbose --dry-run`

## Build

Uses [pydoit](https://pydoit.org/) to run tasks. Running `doit` will run all default tasks.

- `doit`

## Docs

Will be built as part of `doit` but can be built separately with:

- `mkdocs build`

Can be served locally with:

- `mkdocs serve`

To add a new page to the docs, edit the `mkdocs.yml` file and add the page under the `nav` section.
Then add the markdown file to the `docs/` directory.

## Test

All tests are interactive and require user interaction.  There are currently no automated tests.

- `pytest` or `doit tests`

## Updating README.md

Do not directly edit README.md, instead edit README.mdpp and process with MarkdownPP using `doit` to update README.md.
