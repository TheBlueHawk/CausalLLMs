#!/bin/bash
# Downloading from the pile.
# wget 'the-eye.eu/public/AI/pile/train/##.jsonl.zst'
## varies from 00, 01, ..., 29.

set -e

data_dir=data/tmp/script_data
output_dir=out/pile_counts
full_sentences="${1:-true}"

for idx in $(seq -w 00 29); do
  filename_zip="${idx}.jsonl.zst"
  url="the-eye.eu/public/AI/pile/train/${filename_zip}"
  #filename_zip="test.jsonl.zst"
  #url="the-eye.eu/public/AI/pile/test.jsonl.zst"
  filename="${idx}.jsonl"

  # Remove old data.
  rm -rf $data_dir

  # Download new data.
  mkdir -p $data_dir
  pushd $data_dir
  wget "$url"

  # The first and last lines are corrupted in most files,
  # since we are only doing a partial extraction. So we drop the first and last lines.
  echo "Extracting $filename_zip"
  zstdcat $filename_zip  > $filename
  popd

  data_path=$data_dir/$filename
  python count_partial_pile.py ${data_path} --output_dir $output_dir --full_sentences $full_sentences
done

python merge_json_counts.py out/pile_counts/* > merged_counts.json
