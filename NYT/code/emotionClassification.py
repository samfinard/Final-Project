import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from tqdm import tqdm

def classify_emotion(inputfilepath, outputfilepath, threshold):
    tokenizer = AutoTokenizer.from_pretrained("SamLowe/roberta-base-go_emotions")
    model = AutoModelForSequenceClassification.from_pretrained("SamLowe/roberta-base-go_emotions")

    # Read the CSV file from the input path
    df = pd.read_csv(inputfilepath)

    # Initialize an empty list to store emotions
    emotions_list = []

    # Loop through the DataFrame with tqdm progress bar
    for i, row in tqdm(df.iterrows(), total=df.shape[0], desc="Classifying emotions"):
        text = row['abstract'] + ' ' + row['headline']
        inputs = tokenizer(text, return_tensors="pt", padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        normalized_logits = torch.sigmoid(outputs.logits)
        labels_and_scores = {model.config.id2label[index]: score.item() for index, score in enumerate(normalized_logits[0])}
        filtered_labels = {label: score for label, score in labels_and_scores.items() if score > threshold}
        emotions_list.append(str(filtered_labels))

    # Add the emotions list as a new column
    df['emotion'] = emotions_list

    # Write the result to the output path
    df.to_csv(outputfilepath, index=False)

def main():
    inputfilepath = "../data/NYT_articles_text.csv"
    outputfilepath = "NYT_articles_emotion.csv"
    threshold = 0.25
    classify_emotion(inputfilepath, outputfilepath, threshold)

if __name__ == "__main__":
    main()
