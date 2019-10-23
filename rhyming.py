""" asdf"""
import random
import requests

SYLLABLE_TARGET = 3
API_BASE = "https://api.datamuse.com/words"

CACHED_RHYMES = {}

def pos_filter(word, part_of_speech):
    """ Filter by part of speech """
    return part_of_speech in word.get("tags", {})

def syl_filter(word, min_syllables, max_syllables):
    """ Filter by syllable count (between min and max) """
    return min_syllables <= word["numSyllables"] <= max_syllables

def fetch_rhymes(word):
    """ Queries API for list of words that rhyme """
    if word in CACHED_RHYMES:
        return CACHED_RHYMES[word]

    params = {"rel_rhy": word, "md": "ps", "max": 1000}
    response = requests.get(API_BASE, params=params)
    rhyming_words = response.json()

    CACHED_RHYMES[word] = rhyming_words

    return rhyming_words

def fetch_adjs(word):
    """ Queries for adjatives that commonly precede the given word """
    params = {"rel_jjb": word, "md": "ps", "max": 1000}
    response = requests.get(API_BASE, params=params)
    return response.json()

def find_rhyme(syllables, base, attempts=10):
    """
    Find a string with (adjative)? (noun)
      which has a total of SYLLABLE_TARGET syllables and rhymes with "kit kat bar
    """
    if not attempts:
        raise Exception("Failed to find a suitable rhyme")

    base_words = fetch_rhymes(base)

    for word in base_words:
        if not pos_filter(word, "n") or not syl_filter(word, 1, syllables):
            base_words.remove(word)

    chosen_base_word = random.choice(base_words)
    print(chosen_base_word)

    # Figure out remaining syllables. If none, we're done.
    syl_left = syllables - chosen_base_word["numSyllables"]
    if not syl_left:
        return chosen_base_word["word"]

    adj_list = fetch_adjs(chosen_base_word["word"])
    adj_list = [word for word in adj_list if syl_filter(word, syl_left, syl_left)]

    if not adj_list:
        print(f"No matching adjatives for {chosen_base_word['word']}. Retrying ({attempts} more)")
        return find_rhyme(syllables, base, attempts - 1)

    chosen_adj = adj_list[0]

    return chosen_adj["word"] + " " + chosen_base_word["word"]

rhyme = find_rhyme(3, "bar")
jingle = f"🎶 Break me off a piece of that {rhyme} 🎶"
print(jingle)
