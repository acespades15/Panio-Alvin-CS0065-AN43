from textblob import TextBlob

positive = 0
neutral = 0
negative = 0

for count in range(1, 11):
    sentence = input(f"Sentence {count}/10: ")
    s = TextBlob(sentence)
    p = s.sentiment.polarity

    if p > 0:
        tone = "positive"
        positive += 1
    elif p < 0:
        tone = "negative"
        negative += 1
    else:
        tone = "neutral"
        neutral += 1

    print(f"Polarity: {p:.2f} | Sentiment: {tone}")

print("\nSummary of 10 sentences")
print(f"Positive: {positive}")
print(f"Neutral: {neutral}")
print(f"Negative: {negative}")
