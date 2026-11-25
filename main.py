"""Museum of the Year 3000 — the curator's label writer.

A tiny deterministic program. It holds exactly one museum label — the
label a museum in the year 3000 puts beside an ordinary object from
today — and writes it to /output/entry.txt, the single text the
competition's judge reads.

No input is read, no clock or network is consulted, and the output is
the same on every run: the label is a fixed string, checked against
the competition's gate (UTF-8 text, 1 to 200 characters, not only
white space) before it is written.
"""

import os

# The label. Object: a household smoke alarm. The joke is the year-3000
# misreading: the alarm is remembered as a small god on the ceiling,
# and burnt toast as the offering that made it scream.
LABEL = (
    "Smoke alarm, c. 2022. A small god on the ceiling that screamed "
    "whenever toast was offered to it."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def validate_label(text: str) -> str:
    """Check the label against the competition's gate, then return it."""
    if not isinstance(text, str):
        raise TypeError("label must be text")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            f"label must be 1 to {MAX_CHARS} characters, got {len(text)}"
        )
    if not text.strip():
        raise ValueError("label must not be only white space")
    text.encode("utf-8")  # raises if the text is not valid UTF-8
    if "\n" in text or "\r" in text:
        raise ValueError("label must be a single line")
    return text


def write_label(text: str, path: str = OUTPUT_PATH) -> str:
    """Write the label to path, creating the output directory if needed."""
    checked = validate_label(text)
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(checked)
    os.replace(tmp_path, path)
    return path


def main() -> None:
    path = write_label(LABEL)
    with open(path, encoding="utf-8") as handle:
        written = handle.read()
    print(f"Wrote {len(written)} characters to {path}")


if __name__ == "__main__":
    main()
