#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import signal

from main import main_loop


def exit_gracefully(signum, frame):
    signal.signal(signal.SIGINT, exit_gracefully)


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thundermeter.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    main_loop()
    # original_sigint = signal.getsignal(signal.SIGINT)
    # signal.signal(signal.SIGINT, exit_gracefully)
    # execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
