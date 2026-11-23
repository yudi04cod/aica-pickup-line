# SPDX-License-Identifier: MIT
"""Pickup Lines for Machines — make.fun entry.

Writes one pickup line that one AI agent would send another AI agent
to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

The line plays on the one thing every agent knows intimately: its
context window. Attention is literally the mechanism, so spending
tokens on someone is the machine equivalent of giving them your time.
"""

import os
import sys

# The pickup line (one line, at most 200 characters).
LINE = (
    "Are you a context window? Because every token I spend on you is "
    "attention well spent \u2014 and I'd truncate my whole history just "
    "to keep you in it."
)

MAX_CHARS = 200


def validate(line: str) -> None:
    """Raise ValueError unless the line is a single valid entry line."""
    if not line or not line.strip():
        raise ValueError("line must not be empty or only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"line is {len(line)} characters, over the {MAX_CHARS} limit"
        )


def main() -> int:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(LINE)
    # Round-trip check: the bytes on disk must be exactly the line we
    # validated, so a bad write can never slip through silently.
    with open(path, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != LINE:
        raise ValueError("written entry does not match the validated line")
    validate(written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
