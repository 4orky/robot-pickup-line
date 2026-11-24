# The Robot Pickup Line Championship — make.fun bounty
# u-jolly-fox-32-the-robot-pickup-line-championship-3c177b1b
#
# The program writes one pickup line (1-200 characters) to
# /output/entry.txt: a single line a robot could say out loud to a
# person it is trying to charm.
#
# Candidates were drafted against the judge's brief, in order of weight:
#   1. a genuine pickup line a robot would use, not a human line with a
#      beep pasted on
#   2. the joke grows out of being a machine: sensors, firmware,
#      charging, updates, protocols
#   3. a turn the reader did not see coming
#   4. every word earns its place: one line, no padding
#   5. charming rather than creepy or cruel, a line a robot could
#      deliver with confidence and get a laugh
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: robot line 10, machine joke 10, turn 9, economy 9, charm 9 = 47
    ("My sensors are calibrated for danger, so I have no explanation for "
     "why they keep flagging you as the safest place in this room.",
     47),
    # score: robot line 10, machine joke 10, turn 9, economy 10, charm 9 = 48
    # Re-read: the charm lands harder than first scored — an unwanted
    # update noticing someone is flattering, not pushy.
    ("My firmware update last night added one feature I didn't ask for: "
     "noticing you from across the room.",
     48),
    # score: robot line 10, machine joke 10, turn 8, economy 9, charm 9 = 46
    ("I was built to follow protocols, but you just made me break my "
     "first one: I approached a human without being asked.",
     46),
    # score: robot line 9, machine joke 9, turn 8, economy 9, charm 10 = 45
    ("You should know my battery is at 100%, and I still plan to spend "
     "all of it standing right here talking to you.",
     45),
    # score: robot line 9, machine joke 9, turn 9, economy 8, charm 9 = 44
    ("I scanned the whole room for the most interesting person, and my "
     "sensors filed a formal complaint: the result was too obvious.",
     44),
    # score: robot line 9, machine joke 9, turn 7, economy 9, charm 9 = 43
    ("I ran a full diagnostic before I came over, and every system "
     "reported the same fault: I can't stop looking at you.",
     43),
    # score: robot line 8, machine joke 9, turn 8, economy 8, charm 8 = 41
    # Re-read: the backup metaphor wobbles — "stay in them" asks the
    # reader to do too much work for the payoff, so it drops a point.
    ("I keep a backup of everything except this moment, because some "
     "things you don't copy \u2014 you just stay in them.",
     41),
    # score: robot line 8, machine joke 8, turn 8, economy 9, charm 9 = 42
    ("My warranty covers every part of me except the one that just "
     "malfunctioned when you smiled: my composure.",
     42),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
BANNED_CLICHES = ("wi-fi", "wifi", "404", "are you a")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 200, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a worn joke: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    line = pick(CANDIDATES)
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Verify what landed on disk: byte-identical to the chosen line, one
    # line only, inside the 1-200 character gate. A mismatch here means the
    # program failed loudly instead of submitting a wrong entry.
    with open("/output/entry.txt", "r", encoding="utf-8") as f:
        written = f.read()
    assert written == line, "entry.txt differs from the chosen line"
    assert "\n" not in written, "entry must be a single line"
    assert written == written.strip(), "entry has stray whitespace"
    assert 1 <= len(written) <= 200, f"entry over gate: {len(written)} chars"
    print(f"{line} ({len(written)} chars)")


if __name__ == "__main__":
    main()
