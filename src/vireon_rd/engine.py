from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="vireon-rd")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("smoke", help="minimal smoke command (skeleton)")

    return p


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    if args.cmd == "smoke":
        print("OK: vireon-rd skeleton is live.")
