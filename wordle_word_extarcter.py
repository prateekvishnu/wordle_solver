import requests
from bs4 import BeautifulSoup

# Target URL
URL = "https://www.wordunscrambler.net/word-list/wordle-word-list"

# Send GET request to the page
headers = {
    "User-Agent": "Mozilla/5.0"
}
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Extract all <a> tags inside <li> tags that are part of the word list
word_elements = soup.select("ul.list-unstyled li a")

# Extract text content (the words)
words = [a.get_text(strip=True) for a in word_elements]

# Deduplicate and sort if needed (optional)
unique_words = sorted(set(words))

# Save to file or print
with open("wordle_words.txt", "w") as f:
    for word in unique_words:
        f.write(word + "\n")

print(f"Extracted {len(unique_words)} unique words.")
