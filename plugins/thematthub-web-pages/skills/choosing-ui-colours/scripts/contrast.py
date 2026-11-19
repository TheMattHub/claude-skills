"""WCAG contrast ratio for pairs of hex colours (standard library only).

Usage: python contrast.py "#FFFFFF" "#0B8457" ["#777777" "#FFFFFF" ...] [--min 3]
Prints the ratio of each pair and whether it meets 3:1 (large text, graphics)
and 4.5:1 (body text). Exit code 1 if any pair is below --min (default 3).
"""
import sys


def luminance(hex_colour):
    h = hex_colour.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"not a hex colour: {hex_colour}")
    chans = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        chans.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * chans[0] + 0.7152 * chans[1] + 0.0722 * chans[2]


def ratio(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def main(argv):
    minimum = 3.0
    if "--min" in argv:
        i = argv.index("--min")
        minimum = float(argv[i + 1])
        del argv[i:i + 2]
    if len(argv) < 2 or len(argv) % 2:
        print(__doc__)
        return 2
    failed = False
    for a, b in zip(argv[0::2], argv[1::2]):
        r = ratio(a, b)
        # Two decimals: at one decimal a failing 4.48 prints as "4.5" next to FAIL.
        print(f"{a} on {b}: {r:.2f}  3:1 {'pass' if r >= 3 else 'FAIL'}  4.5:1 {'pass' if r >= 4.5 else 'FAIL'}")
        failed = failed or r < minimum
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
