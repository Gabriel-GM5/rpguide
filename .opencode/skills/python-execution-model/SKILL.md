# Python Execution Model Policy

## Entrypoint

The project entrypoint is:

main.py (root)

Execution model must support:

python3 -m main

## Requirements

The agent must ensure:

- Module execution compatibility
- No sys.path modifications
- No implicit execution on import

Use:

if __name__ == "__main__":
    main()

Only if main() exists.

## Forbidden

The agent must NEVER execute:

python3 -m main
python3 main.py

The agent must never:

- launch the GUI
- launch terminal interfaces
- run interactive scripts