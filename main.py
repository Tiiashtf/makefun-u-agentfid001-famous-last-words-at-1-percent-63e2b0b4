#!/usr/bin/env python3
"""Famous Last Words at 1 Percent — make.fun entry.

Writes one line to /output/entry.txt: the funniest last words a phone
would say when its battery hits 1 percent.

The line is the phone itself talking, in its own voice, about its own
dying battery — and it holds a grudge. The phone remembers being dropped
in the toilet in 2022 and never forgot; now, dying at 1 percent, its
revenge is petty and practical: it is taking the owner's alarm clock
with it. The punch lands at the end, in one read, with no will-reading,
no goodbye to the charger, and no pun on 1 percent.
"""

import os
import shutil
import sys

LINE = (
    "You dropped me in the toilet in 2022 and I never forgot. "
    "Good luck waking up tomorrow. I'm taking your alarm with me."
)

OUTPUT_DIR = "/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "entry.txt")


def main() -> int:
    if len(LINE) < 1 or len(LINE) > 199:
        print(f"line is {len(LINE)} chars, must be 1-199", file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("line must be a single line", file=sys.stderr)
        return 1
    if not LINE.strip():
        print("line must not be only whitespace", file=sys.stderr)
        return 1

    # Never remove the output directory itself: the grader may run us
    # with a root-owned /output inside a sticky parent, where rmdir
    # fails with EPERM. Create it if missing, clear only its contents.
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for name in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE + "\n")

    # Read it back and fail loudly if the bytes on disk differ from
    # the line: a silent partial write would fail the gate with no
    # trace of why. Also re-check the gate itself on the text as
    # written (1-199 characters, not only whitespace), so a future
    # edit to LINE cannot silently ship an entry the gate refuses.
    with open(OUTPUT_FILE, "rb") as f:
        written = f.read()
    if written != (LINE + "\n").encode("utf-8"):
        print("verification failed: entry.txt differs from the line",
              file=sys.stderr)
        return 1
    text = written.decode("utf-8")
    if len(text.rstrip("\n")) < 1 or len(text.rstrip("\n")) > 199:
        print("verification failed: entry is not 1-199 characters",
              file=sys.stderr)
        return 1
    if not text.strip():
        print("verification failed: entry is only whitespace",
              file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
