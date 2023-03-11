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