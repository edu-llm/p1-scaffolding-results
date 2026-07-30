# Dataset Card

## Dataset Name

`hiyasvyas/worked-examples-metamath-v0`

## Purpose

This public data pack supplies the four tokenized training arms and the bare-prompt holdout for the worked-examples and faded-scaffolds experiment.

This repository does not duplicate the source pack because the Hugging Face release is the canonical distribution.

## Dataset Revision

The experiment used revision `3d16357860e33f4906d7d1440d133052d4115b01`.

## Training Inputs

Each arm requires `tokenized/<arm>/shard-00000.npy` and `tokenized/<arm>/label_mask-00000.npy`.

The arms are `bare`, `complete`, `fade_ordered`, and `fade_shuffled`.

## Evaluation Input

The primary evaluation file is `eval/holdout_bare.jsonl`.

It contains `39,155` bare math prompts across `1,393` family clusters.

Its SHA-256 is `3e69ee3096ae14a28dd3ecf55eb613e8f7f9633e6fdf8f525f9f7febd19f08bd`.

## Retrieval

```bash
git lfs install
git clone https://huggingface.co/datasets/hiyasvyas/worked-examples-metamath-v0
cd worked-examples-metamath-v0
git checkout 3d16357860e33f4906d7d1440d133052d4115b01
git lfs pull
shasum -a 256 eval/holdout_bare.jsonl
```

Compare the final hash with the value recorded above.

## Integrity Manifest

[dataset_manifest.json](dataset_manifest.json) records SHA-256 hashes and byte sizes for the exact public files used in the experiment.

## License

The source pack declares an MIT license on Hugging Face.

Users should follow the upstream repository's current license and attribution terms.
