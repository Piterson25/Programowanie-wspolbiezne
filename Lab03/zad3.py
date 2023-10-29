import os
import re
import sys


def process_file(filename, word):
    with open(filename, 'r') as file:
        text = file.read()

    input_directives = re.findall(r'\\input\{([^}]*)}', text)

    total_word_count = text.count(word)

    for input_file in input_directives:
        pid = os.fork()

        # proces potomny
        if pid == 0:
            child_word_count = process_file(input_file, word)
            sys.exit(child_word_count)
        # proces macierzysty
        else:
            # czekanie za zakonczenie procesu potomnego
            _, child_status = os.waitpid(pid, 0)
            child_word_count = os.WEXITSTATUS(child_status)
            total_word_count += child_word_count

    return total_word_count


p = input("Podaj nazwę pliku z początkiem tekstu: ")
s = input("Podaj słowo do zliczenia: ")

word_count = process_file(p, s)
print(f"Ilość wystąpień słowa '{s}': {word_count}")
