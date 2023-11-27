import pandas as pd
from transformers import pipeline


def generate_summaries(df: pd.DataFrame) -> pd.DataFrame:
    summarizer = pipeline("summarization")
    df["summary"] = df["text"].apply(lambda x: summarizer(x[:1024])[0]["summary_text"])
    return df
