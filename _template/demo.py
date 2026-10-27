"""
demo.py

One-paragraph description of what this demo shows.

Run:
    python3 demo.py
"""
import argparse


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seed", type=int, default=1, help="random seed")
    args = parser.parse_args()
    print(f"Running demo with seed {args.seed}")


if __name__ == "__main__":
    main()
