import json
from extractor import extract_examples

# Load the test JSON data from a file
with open('test_data.json', 'r') as file:
    test_data = json.load(file)

# Extract the examples
examples = extract_examples(test_data)

# Print the extracted examples as concatenated sentences
print("Extracted Examples:")
for example in examples:
    # Concatenate the words into a sentence
    print(f"Sentence: {example['text']}")
    print(f"Mark Index: {example['mark']}")
    print(f"Audio File: {example['audioFile']}")
    print()  # Add a newline for separation
