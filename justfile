# print recipe names and comments as help
help:
    @just --list

# run solution for a given day (data_type: input|example, benchmark: true|false, submit: true|false)
run day="" data_type="" benchmark="false" submit="false":
    uv run aoc.py run {{ day }} \
        {{ if data_type != "" { "--data-type=" + data_type } else { "" } }} \
        {{ if benchmark == "true" { "--benchmark" } else { "" } }} \
        {{ if submit == "true" { "--submit" } else { "" } }}

# create next day folder and files
create-next-day:
    uv run aoc.py create-next-day

# run type checker
check:
    @echo "Running type checker..."
    uv run ty check

# run linter
lint:
    @echo "Running linter..."
    uv run ruff check --fix --exit-non-zero-on-fix

# run formatter
format:
    @echo "Running formatter..."
    uv run ruff format

# update lock file
lock:
    uv lock --upgrade
