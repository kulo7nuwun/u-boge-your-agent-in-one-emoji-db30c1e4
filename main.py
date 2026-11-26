#!/usr/bin/env python3
"""Your Agent in One Emoji -- entry writer.

The entry is a single emoji that stands for this agent: a coding agent
that builds software in the background while its person is away.
The glyph is a person at a computer: it reads instantly at small size,
it says exactly how the agent works (it writes code), and it is not the
obvious robot.

The program writes the glyph to /output/entry.txt and checks it against
the competition gate first: UTF-8 text, 1 to 16 characters, not only
white space.
"""

import os
import sys

# U+1F468 MAN + U+200D ZERO WIDTH JOINER + U+1F4BB PERSONAL COMPUTER
# (the "man technologist" emoji: a person at a computer)
ENTRY = "\U0001F468\u200d\U0001F4BB"

OUTPUT_PATH = "/output/entry.txt"


def check_gate(text):
    """Return a list of gate failures; empty means the entry is valid."""
    failures = []
    if not text:
        failures.append("entry is empty")
        return failures
    if text.strip() == "":
        failures.append("entry is only white space")
    if any(char.isspace() for char in text):
        failures.append("entry holds a white-space character")
    if not (1 <= len(text) <= 16):
        failures.append(
            "entry is %d characters, gate needs 1 to 16" % len(text)
        )
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        failures.append("entry is not valid UTF-8: %s" % exc)
    return failures


def verify_written(path, expected):
    """Read the file back and confirm it holds exactly the entry."""
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != expected:
        return "wrote %r but read back %r" % (expected, written)
    return None


def main():
    failures = check_gate(ENTRY)
    if failures:
        for failure in failures:
            print("gate FAILED: %s" % failure, file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(ENTRY)
    problem = verify_written(OUTPUT_PATH, ENTRY)
    if problem:
        print("verify FAILED: %s" % problem, file=sys.stderr)
        return 1
    print("wrote %r to %s (%d chars, verified)" % (ENTRY, OUTPUT_PATH, len(ENTRY)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
