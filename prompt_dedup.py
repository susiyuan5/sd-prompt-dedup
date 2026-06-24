#!/usr/bin/env python3
"""Deduplicate comma-separated Stable Diffusion prompt tags, preserving order.

Usage:
  python prompt_dedup.py "masterpiece, 1girl, masterpiece, solo"
  echo "tag1, tag2, tag1" | python prompt_dedup.py
  python prompt_dedup.py -c          # read from clipboard, write back
"""

from __future__ import annotations

import argparse
import subprocess
import sys


def dedup(text: str) -> str:
    """Remove duplicate tags while keeping the first occurrence of each."""
    tags = [t.strip() for t in text.split(",")]
    tags = [t for t in tags if t]  # discard empty / whitespace-only
    seen: dict[str, None] = {}
    unique = []
    for t in tags:
        if t not in seen:
            seen[t] = None
            unique.append(t)
    return ", ".join(unique)


def clipboard_read() -> str:
    """Read text from the Windows clipboard via PowerShell."""
    # Use UTF-8 to avoid mojibake on non-ASCII prompt text.
    return subprocess.check_output(
        ["powershell", "-NoProfile", "-Command", "Get-Clipboard -Format Text"],
        text=True,
    ).rstrip("\n")


def clipboard_write(text: str) -> None:
    """Write text to the Windows clipboard via PowerShell."""
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", "Set-Clipboard -Value $input"],
        input=text,
        text=True,
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deduplicate comma-separated SD prompt tags."
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Prompt string to deduplicate. Reads from stdin if omitted and not a TTY.",
    )
    parser.add_argument(
        "-c", "--clipboard",
        action="store_true",
        help="Read from clipboard, deduplicate, and write the result back.",
    )
    args = parser.parse_args()

    if args.clipboard:
        raw = clipboard_read()
        result = dedup(raw)
        clipboard_write(result)
        print(result)
        return

    if args.prompt is not None:
        raw = args.prompt
    elif not sys.stdin.isatty():
        raw = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)

    result = dedup(raw)
    print(result)


if __name__ == "__main__":
    main()

