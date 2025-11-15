# Tools for learning Japanese

My tools for learning Japanese. See subdirectory READMEs for more details.

# Development

Development tools and dependencies are managed with
[mise](https://mise.jdx.dev/). To setup all projects, run: `mise run //:setup`.

## Testing

Tests for each project can be run with `mise run :test`. Tests for all projects
can be run with `mise run //:test`.

## Linting

Linting is done with [pre-commit](https://pre-commit.com/). `mise run //:setup`
installs the pre-commit hooks so it runs when committing, but the entire project
can also be linted with `mise run //:lint`.
