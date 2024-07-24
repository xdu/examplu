def extract_examples(data):
    examples = []
    if 'entry' in data and 'microStructures' in data['entry']:
        for micro_structure in data['entry']['microStructures']:
            if 'grammaticalUnits' in micro_structure:
                for grammatical_unit in micro_structure['grammaticalUnits']:
                    if 'meanings' in grammatical_unit:
                        for meaning in grammatical_unit['meanings']:
                            if 'examples' in meaning:
                                for example in meaning['examples']:
                                    text, mark, end = extract_example_text(example)
                                    audio_file = example.get('audioFiles', {}).get('ogg', None)
                                    examples.append((text, mark, end, audio_file))
    return examples

def extract_example_text(example):
    """
    Extracts example text from the given example dictionary.

    Args:
        example (dict): A dictionary containing example data.

    Returns:
        tuple: A tuple containing the extracted sentence, the starting position of the extracted word,
               and the ending position of the extracted word within the sentence.
    """
    sentence = ""
    mark = 0
    end = 0
    
    if 'parts' in example:
        for part in example['parts']:
            if 'parts' in part:
                for subpart in part['parts']:
                    if subpart.get('type') == 'inflectedHeadword' and 'content' in subpart:
                        mark = len(sentence)
                        sentence = sentence + " " + subpart['content']
                        end = len(sentence)
                    elif subpart.get('type') == 'word' and 'content' in subpart:
                        if subpart.get('joinWithPreviousWord', False) :
                            # Add the word without space if joinWithPreviousWord is True and there is content in sentence
                            sentence = sentence + subpart['content']
                        else:
                            # Otherwise, add the word with space
                            sentence = sentence + " " + subpart['content']
    
    return sentence, mark, end


