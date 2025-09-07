"""
Entry point for running grants_monitor as a module.

This allows the package to be executed with: python -m grants_monitor
"""

from .main import cli

if __name__ == "__main__":
    cli()
