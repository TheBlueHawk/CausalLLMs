# CausalLLMs
Collection of experiments and utilities for testing causal reasoning in LLMs.



## Perplexity calculator
Utility to quickly compute the perplexity score of a given sentence or list of sentences. Mean perplexity is printed in the terminal and all results are saved in a json file as a collection of `{sentence: "text", perplexity: score}`

### Usage
If there is only one sentence, it can be directly passed as an argument with `-t` or `--text`:
```bash
python perplexity_calculator.py -t "This is my sentence"
```
A list of sentences saved in a `.txt` file (one sentence per line) can be processed in parallel with the `-f` or `--file` argument:
```bash
python perplexity_calculator.py -f ./path/to/file.txt
```
Additonal parameters are:
- `--model_id`: must be a [causalLLM](https://huggingface.co/docs/transformers/main/en/model_doc/auto#transformers.AutoModelForCausalLM), default `gpt2`
- `--out-file`: desired location of the json file, default `./out/perplexities/TIMESTAMP.json`

### Examples
```bash
python perplexity_calculator.py -t "To be or not to be?"
>> Mean perplexity: 24.73
```

```bash
python perplexity_calculator.py -t "What is the square root of 343?"
>> Mean perplexity: 54.31
```

```bash
python perplexity_calculator.py -t "What is the 2nd root of 343?"
>> Mean perplexity: 135.41
```

```bash
python perplexity_calculator.py -t "lorem ipsum Wanna Bonjour cane?"
>> Mean perplexity: 438.12
```

## Pile Word Frequency Counting
Utility to count the occurences of a given list of strings in the Pile corpus.
This is a streaming script, so doesn't store the entire Pile corpus, nevertheless you will need at least 20GB of disk space.

### Usage
Save the sentences you want to look for in the file `input.txt` in the `data` directory and then run the following shell script:
```
./run_pile_counting.sh
```

This script calls `count_partial.py` on multiple JSON, outputting to `script_output/` and then merges the outputs in a single file by calling `merge_json_counts.py`
