#!/usr/bin/env python3
import argparse
import os
import sys

from lightning_sdk import Machine, Studio


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"missing required environment variable: {name}")
    return value


def machine_from_name(name: str):
    try:
        return getattr(Machine, name)
    except AttributeError as exc:
        choices = sorted(k for k in dir(Machine) if k.isupper() and not k.startswith("_"))
        raise SystemExit(f"unknown Lightning machine {name!r}; available enum names include: {', '.join(choices)}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Start or stop the Lightning Studio used as an Expert-centricity Actions runner.")
    parser.add_argument("operation", choices=("start", "stop"))
    parser.add_argument("--machine", default="T4", help="lightning_sdk.Machine enum name (default: T4)")
    args = parser.parse_args()

    # lightning-sdk reads LIGHTNING_USER_ID and LIGHTNING_API_KEY directly.
    require_env("LIGHTNING_USER_ID")
    require_env("LIGHTNING_API_KEY")
    studio_name = require_env("LIGHTNING_STUDIO_NAME")

    studio = Studio(studio_name)
    if args.operation == "start":
        machine = machine_from_name(args.machine)
        print(f"starting Lightning Studio {studio_name!r} on Machine.{args.machine}")
        studio.start(machine)
        print("start request accepted")
    else:
        print(f"stopping Lightning Studio {studio_name!r}")
        studio.stop()
        print("stop request accepted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
