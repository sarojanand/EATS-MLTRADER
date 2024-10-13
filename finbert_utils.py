import torch
from typing import Tuple
from transformers import AutoTokenizer, AutoModelForSequenceClassification

device = "cuda:0" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(device)
labels = ["positive", "negative", "neutral"]

def estimate_sentiment(news: list) -> Tuple[float, str]:
    """
    Estimates the sentiment of a list of news articles.

    Args:
        news (List[str]): A list of news articles as strings.

    Returns:
        
        Tuple[float, str]: A tuple where the first element is the probability of the most likely sentiment,
                           and the second element is the predicted sentiment label.
    """
    if news:
        tokens = tokenizer(news, return_tensors="pt", padding=True).to(device)
        result = model(tokens["input_ids"], attention_mask=tokens["attention_mask"])["logits"]
        result = torch.nn.functional.softmax(torch.sum(result, 0), dim=-1)
        probability = result[torch.argmax(result)].item()
        sentiment = labels[torch.argmax(result)]
        return probability, sentiment
    else:
        return 0, labels[-1], "No sentiment found"

if __name__ == "__main__":
    tensor, sentiment = estimate_sentiment(['the market repsonded negatively to the news!', 'traders were displeased to the market!'])
    print(tensor, sentiment)
    cuda_available = None
    if torch.cuda.is_available():
        cuda_available = "is"
    elif not torch.cuda.is_available():
        cuda_available = "is not"
    print(f"CUDA {cuda_available} available")