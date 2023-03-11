# Code inspired from public example on HuggingFace:
# https://huggingface.co/spaces/evaluate-measurement/perplexity

from ast import arg
from datetime import datetime
from time import time
import evaluate
from lightning_fabric import Fabric
from tqdm import tqdm
from datasets import load_dataset
import argparse
import csv
import dataclasses
from typing import Optional, Type
import datasets
import torch
from zmq import device
import json


def text_to_perplexity(input_texts: list[str], model_id="gpt2") -> list[float]:
    perplexity = evaluate.load("perplexity", module_type="measurement")
    results = perplexity.compute(
        model_id=model_id, add_start_token=False, data=input_texts
    )
    return results


def sentence_perplexity_to_json(
    input_texts: list[str], perplexities: list[float], out_file_name: str
):
    data = [{"sentence": s, "perplexity": f} for s, f in zip(input_texts, perplexities)]
    with open(out_file_name, "w") as outfile:
        outfile.write(json.dumps({"data": data}, indent=1))


def run():
    # Parse arguments
    args = parse_args()

    # Load input texts
    if args.text is not None:
        input_texts = [args.text]
    elif args.file is not None:
        with open(args.file, "r") as file:
            lines = file.readlines()
            input_texts = [line.strip() for line in lines]

    # Compute perplexities
    perplexities = text_to_perplexity(input_texts, args.model_id)

    # Save results to json file
    sentence_perplexity_to_json(
        input_texts, perplexities["perplexities"], args.out_file
    )
    print("Mean perplexity: ", round(perplexities["mean_perplexity"], 2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--text", type=str, default=None)
    parser.add_argument("-f", "--file", type=str, default=None)
    parser.add_argument("-m", "--model_id", type=str, default="gpt2")
    parser.add_argument(
        "-o",
        "--out-file",
        type=str,
        default="./out/perplexities/{}.json".format(
            datetime.now().strftime("%Y%m%d_%H%M%S")
        ),
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    run()
