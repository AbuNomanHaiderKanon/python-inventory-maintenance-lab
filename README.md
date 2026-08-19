# Inventory Maintenance Lab

A small but realistic Python inventory and order-management application for software-maintenance experiments.

## Features

- SQLite persistence
- Product creation and stock updates
- Low-stock reporting
- Order creation with stock validation
- Summary reporting
- Unit tests
- Optional logging and profiling experiments for CSE 4802 Lab 3

## Quick start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m inventory seed
python -m inventory list-products
python -m inventory report
```

Use `python -m inventory --help` for all commands.

## Example

```powershell
python -m inventory add-product P-100 "Wireless Mouse" 25 15.50
python -m inventory restock P-100 10
python -m inventory order P-100 2
python -m inventory report
```

The default database is `inventory.db`. Set `INVENTORY_DB` to use another path.

Run the tests with the Python standard library:

```powershell
python -m unittest discover -s tests -v
```

For optional packaging, run `python -m pip install -e .` in an environment with internet access.

## Lab experiments

The application has clear service functions suitable for Loguru, PySnooper, VizTracer, and cProfile/SnakeViz. Keep experimental instrumentation in a separate branch or copy so the baseline remains easy to run.

## License

MIT
