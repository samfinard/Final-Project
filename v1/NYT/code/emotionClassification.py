import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from tqdm import tqdm
import os

def classify_emotion(inputfilepath, outputfilepath, threshold, batch_size=20, checkpoint_file="emotion_checkpoint.txt"):
    tokenizer = AutoTokenizer.from_pretrained("SamLowe/roberta-base-go_emotions")
    model = AutoModelForSequenceClassification.from_pretrained("SamLowe/roberta-base-go_emotions")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    df = pd.read_csv(inputfilepath)
    emotions_dict = {f"emotion_{label}": [None] * len(df) for label in model.config.id2label.values()}

    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            checkpoint = f.read()
            start_row = int(checkpoint or 0)
    else:
        start_row = 0

    for i in tqdm(range(start_row, len(df), batch_size), desc="Classifying emotions"):
        end_row = min(i + batch_size, len(df))
        texts = [df.loc[j, 'abstract'] + ' ' + df.loc[j, 'headline'] for j in range(i, end_row)]
        inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
        inputs = {key: value.to(device) for key, value in inputs.items()}
        
        with torch.no_grad():
            outputs = model(**inputs)
        normalized_logits = torch.sigmoid(outputs.logits)
        
        for j in range(end_row - i):
            labels_and_scores = {model.config.id2label[index]: score.item() for index, score in enumerate(normalized_logits[j])}
            for label, score in labels_and_scores.items():
                emotions_dict[f"emotion_{label}"][i + j] = score

        for col_name, col_values in emotions_dict.items():
            df[col_name] = col_values
        df.to_csv(outputfilepath, index=False)

        with open(checkpoint_file, 'w') as f:
            f.write(str(end_row))

def main():
    inputfilepath = "../data/NYT_articles_text.csv"
    outputfilepath = "NYT_articles_emotion.csv"
    threshold = 0.25
    classify_emotion(inputfilepath, outputfilepath, threshold)

if __name__ == "__main__":
    main()
