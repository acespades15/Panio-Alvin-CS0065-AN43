import re
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"


def load_words(filename):
    with (DATA / filename).open(encoding="utf-8") as file:
        return {
            line.strip().lower()
            for line in file
            if line.strip() and not line.startswith(";")
        }


HAPPY_WORDS = load_words("happy-words.txt")
SAD_WORDS = load_words("sad-words.txt")


def words(sentence):
    return re.findall(r"[a-z]+(?:[-'][a-z]+)*", sentence.lower())


def number_happy(sentence):
    return sum(word in HAPPY_WORDS for word in words(sentence))


def number_sad(sentence):
    return sum(word in SAD_WORDS for word in words(sentence))


if __name__ == "__main__":
    sentence = input("Enter a sentence: ")
    happy = number_happy(sentence)
    sad = number_sad(sentence)
    print(f"Happy words: {happy}")
    print(f"Sad words: {sad}")

    if happy > sad:
        print("Analysis: positive (happy)")
    elif sad > happy:
        print("Analysis: negative (sad)")
    else:
        print("Analysis: neutral")
