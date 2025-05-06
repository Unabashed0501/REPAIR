import pandas as pd

# Login using e.g. `huggingface-cli login` to access this dataset
splits = {'dev': 'data/dev-00000-of-00001.parquet', 'test': 'data/test-00000-of-00001.parquet'}
df_dev = pd.read_parquet("hf://datasets/princeton-nlp/SWE-bench_Lite/" + splits["dev"])
df_test = pd.read_parquet("hf://datasets/princeton-nlp/SWE-bench_Lite/" + splits["test"])

df_dev.to_csv("SWE-Bench-Lite/swe_bench_lite_dev.csv", index=True)
df_test.to_csv("SWE-Bench-Lite/swe_bench_lite_test.csv", index=True)