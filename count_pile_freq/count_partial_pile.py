"""
Outputs words frequencies from partial Pile data.
"""
import argparse
import json
import pathlib
import sys
from collections import Counter

import jsonlines
import lm_dataformat as lmd
import tqdm


def get_length(reader):
    count = 0
    for _ in catch_json_error(reader.stream_data()):
        count += 1
    return count


def get_words_set():
    with open("input.txt", "r") as file:
        words = set(file.read().split())
    return words


def get_lines_set():
    lines = set()
    with open("input.txt", "r") as file:
        for line in file:
            line = line.strip().lower()
            lines.add(line)
    return lines


WORDS_SET = get_words_set()
LINES_SET = get_lines_set()


def catch_json_error(generator):
    try:
        yield from generator
    except jsonlines.jsonlines.InvalidLineError:
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=pathlib.Path)
    parser.add_argument("--output_dir", type=pathlib.Path)
    parser.add_argument("--full_senteces", type=bool)
    args = parser.parse_args()

    reader = lmd.Reader(str(args.input_file))
    length = get_length(reader)

    cnt = Counter()
    if args.full_senteces:
        for text in tqdm.tqdm(catch_json_error(reader.stream_data()), total=length):
            text = text.lower()
            for sentence in LINES_SET:
                count = (text).count(sentence)
                cnt[sentence] += count

    else:
        for text in tqdm.tqdm(catch_json_error(reader.stream_data()), total=length):
            for word in text.split():
                word: str
                if len(word) <= 1:
                    continue
                if not word[0].isupper():
                    continue
                if not word.isascii():
                    continue
                if word.lower() not in WORDS_SET:
                    continue

                chars = set(word)
                banned_chars = set("<>")
                if len(chars.intersection(banned_chars)) > 0:
                    continue

                drop_suffixes = ".,!?"
                if word[-1] in drop_suffixes:
                    word = word[:-1]
                cnt[word.lower()] += 1

    if args.output_dir is not None:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        filename = str(args.input_file).replace("/", "__") + "_words.json"
        output_path = args.output_dir / filename
        with open(output_path, "w") as f:
            json.dump(dict(cnt), f)
        print(
            f"Wrote counts of {len(cnt)} unique words to {output_path}", file=sys.stderr
        )
    else:
        print(json.dumps(dict(cnt)))


if __name__ == "__main__":
    main()
