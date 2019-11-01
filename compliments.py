"""
Generate compliments for MagicMirror
"""
import os
import json

import rhyming

MM_HOME = os.environ.get("MAGICMIRROR_HOME")

def write_compliments_file(count):
    rhymes = [rhyming.find_rhyme(3, "bar") for _ in range(count)]

    messages = ["♫ Break me off a piece of that %s ♫" % rhyme for rhyme in rhymes]
    compliments_json = {"anytime": messages}

    file_path = os.path.join(MM_HOME, "modules", "default", "compliments", "compliments.json")
    with open(file_path, "w", encoding="utf-8") as compliments_file:
        json.dump(compliments_json, compliments_file, ensure_ascii=False)

if __name__ == "__main__":
    write_compliments_file(5)
