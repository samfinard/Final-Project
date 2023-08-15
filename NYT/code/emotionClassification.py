import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from tqdm import tqdm
import os

def classify_emotion(inputfilepath, outputfilepath, threshold, batch_size=100, checkpoint_file="emotion_checkpoint.txt"):
    tokenizer = AutoTokenizer.from_pretrained("SamLowe/roberta-base-go_emotions")
    model = AutoModelForSequenceClassification.from_pretrained("SamLowe/roberta-base-go_emotions")
    df = pd.read_csv(inputfilepath)
    emotions_dict = {f"emotion_{label}": [None] * len(df) for label in model.config.id2label.values()}

    # Initialize the checkpoint
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            checkpoint = f.read()
            start_row = int(checkpoint or 0)
    else:
        start_row = 0

    # Process the rows in batches, starting from the last checkpoint
    for i in tqdm(range(start_row, len(df), batch_size), desc="Classifying emotions"):
        end_row = min(i + batch_size, len(df))
        for j in range(i, end_row):
            text = df.loc[j, 'abstract'] + ' ' + df.loc[j, 'headline']
            inputs = tokenizer(text, return_tensors="pt", padding=True)
            with torch.no_grad():
                outputs = model(**inputs)
            normalized_logits = torch.sigmoid(outputs.logits)
            labels_and_scores = {model.config.id2label[index]: score.item() for index, score in enumerate(normalized_logits[0])}
            for label, score in labels_and_scores.items():
                emotions_dict[f"emotion_{label}"][j] = score # if score > threshold else None

        # Update the DataFrame and save to output file
        for col_name, col_values in emotions_dict.items():
            df[col_name] = col_values
        df.to_csv(outputfilepath, index=False)

        # Update the checkpoint
        with open(checkpoint_file, 'w') as f:
            f.write(str(end_row))



def main():
    inputfilepath = "../data/NYT_articles_text.csv"
    outputfilepath = "NYT_articles_emotion.csv"
    threshold = 0.25
    classify_emotion(inputfilepath, outputfilepath, threshold)

if __name__ == "__main__":
    main()
