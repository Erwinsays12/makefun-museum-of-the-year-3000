"""Museum of the Year 3000 — the curator's label writer.

A tiny deterministic program. It drafts five museum labels — each the
label a museum in the year 3000 puts beside an ordinary object from
today — scores them against the judge's published brief, and writes
the best one to /output/entry.txt, the single text the competition's
judge reads.

No input is read, no clock or network is consulted, and the output is
the same on every run: the candidates are fixed strings, the scoring
is a pure function of them, and the label is checked against the
competition's gate (UTF-8 text, 1 to 200 characters, not only white
space) before it is written.
"""

import os

# Candidate labels, drafted and weighed against the judge's brief:
# on-subject museum label first, the joke landing on a first read,
# the humour in the year 3000 misreading the object, a deadpan
# museum-label voice, and a fresh object and angle. Each candidate
# names its object and year the way a real label does.
CANDIDATES = [
    (
        "Smoke alarm, c. 2022. A small god on the ceiling that screamed "
        "whenever toast was offered to it.",
        "smoke alarm mistaken for a ceiling god receiving toast offerings",
    ),
    (
        "USB cable, c. 2020. Ritual cord. Its priest flipped it three "
        "times before the gods allowed it to connect.",
        "cable mistaken for a ritual cord needing three flips",
    ),
    (
        "Rubber duck, c. 2024. Bath-time deity. Citizens confessed their "
        "troubles to it daily, and it never once interrupted.",
        "bath toy mistaken for a confessional deity",
    ),
    (
        "Stapler, c. 2019. A device that married two sheets of paper. "
        "Divorce was not an option.",
        "stapler mistaken for a marriage device",
    ),
    (
        "Traffic cone, c. 2025. Sacred orange pyramid. Worshippers placed "
        "it around holes in the ground to warn travellers that the earth "
        "was broken.",
        "cone mistaken for a sacred warning pyramid",
    ),
]

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def score_label(text: str) -> int:
    """Score a candidate the way the judge's brief weighs labels.

    Higher is better: a museum date marker, a short deadpan line, a
    misreading verb and a label that lands in a single sentence after
    its date all count; a line outside the gate's length loses outright.
    """
    if not (1 <= len(text) <= MAX_CHARS):
        return -1
    score = 0
    if ", c. 20" in text:
        score += 3  # reads like a real museum label
    if len(text) <= 120:
        score += 2  # short and straight faced
    for verb in ("screamed", "worship", "mistook", "confessed", "married"):
        if verb in text:
            score += 2
    if text.count(".") >= 2:
        score += 1  # label plus deadpan explanation, no throat clearing
    # The first two periods belong to the label's date ("c. 2022."):
    # what follows them is the label proper, and the joke landing in
    # a single sentence there counts extra.
    tail = text.split(".", 2)[2] if text.count(".") >= 2 else ""
    if tail.count(".") == 1:
        score += 1  # the joke lands in one sentence, not two
    return score


def choose_label(candidates) -> str:
    """Pick the highest-scoring candidate; ties go to the earliest."""
    best_text, best_score = None, -1
    for text, _angle in candidates:
        score = score_label(text)
        if score > best_score:
            best_text, best_score = text, score
    if best_text is None:
        raise ValueError("no candidate label passes the gate")
    return best_text


# The label the program writes: the highest-scoring candidate.
LABEL = choose_label(CANDIDATES)


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
