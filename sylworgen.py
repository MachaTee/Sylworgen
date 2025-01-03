from dataclasses import dataclass
from random import choices
from typing import List

@dataclass(frozen=False, order=False)
class Syllable:
    """
        Syllable dataclass
        Constructor params:
            Syllable: String datatype, and repr of class, name of syllable
            Position: Integer datatype, where the syllable occurs
            Frequency: Integer datatype, how many times the syllable occurs
    """
    syllable: str = '?undef'
    position: int = 0
    frequency: int = 0

def generate_words(generation_amount: int = 10, file_path: str = "syllables_en.txt",
                *, as_syllables: bool = False, with_rules: bool = False) -> List[str]:
    syllable_dict = {}
    syl_file_list = []
    longest_syllable = 0

    # Read from syllables file
    with open(file_path, 'r') as syl_file:
        while True:
            syl_read_line = syl_file.readline().strip()
            if len(syl_read_line.split(";")) > longest_syllable:
                longest_syllable = len(syl_read_line.split(";"))
            if not syl_read_line:
                break
            syl_file_list.append(syl_read_line)

    # Append syllables to dict
    for word in syl_file_list:
        for syllable_pos, syllable_raw in enumerate(word.split(';')):
            syllable_compound = f'{syllable_pos}{syllable_raw}'
            if syllable_dict.get(syllable_compound):
                syllable_dict[syllable_compound].frequency += 1
            else:
                syllable_dict[syllable_compound] = Syllable(syllable_raw, syllable_pos, 1)

    weights = {k:[] for k in range(longest_syllable)}
    syllabs = {k:[] for k in range(longest_syllable)}

    for x in range(longest_syllable):
        for y in syllable_dict.values():
            if y.position == x:
                weights[x].append(y.frequency)
                syllabs[x].append(y.syllable)


    word_weights = []
    for x in range(longest_syllable):
        word_weights.append(len(syllabs[x]))

    words = []

    # Generate 10 words
    for y in range(generation_amount):
        word_len = choices(population=[l for l in range(2,longest_syllable+1)], weights=word_weights[1::])
        word = []
        for x in range(word_len[0]):
            word.append(choices(population=syllabs[x], weights=weights[x])[0])
        words.append(("" if not as_syllables else ";").join(word))

    return words


if __name__ == "__main__":
    word_output = generate_words(100, as_syllables=False, file_path="syllables_de.txt")
    print(word_output)
