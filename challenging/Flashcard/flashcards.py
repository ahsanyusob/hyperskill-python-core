import random
import sys
import shutil
import argparse
from collections import defaultdict


# CLASSES
class LoggerOut:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.filename = filename

    def write(self, message):
        self.terminal.write(message)
        with open(self.filename, "a") as file:
            print(message, file=file, flush=True, end='')

    def flush(self):
        pass


class LoggerIn:
    def __init__(self, filename):
        self.terminal = sys.stdin
        self.filename = filename

    def readline(self):
        entry = self.terminal.readline()
        with open(self.filename, "a") as file:
            print(entry.rstrip(), file=file, flush=True)
        return entry


# DEF
def add_card(flashcard_dictionary):
    _numError = 0
    _term = input(f"The term for card:\n")
    while _term in flashcard_dictionary.keys():
        _term = input(f'The term "{_term}" already exists. '
                     f'Try again::\n')
    _def = input(f"The definition for card:\n")
    while _def in [flashcard_dictionary[_key][0] for _key in flashcard_dictionary.keys()]:
        _def = input(f'The definition "{_def}" already exists. '
                     f'Try again::\n')
    flashcard_dictionary.update({_term: [_def, _numError]})
    print(f'The pair ("{_term}":"{_def}") has been added.\n')


def remove_card(flashcard_dictionary):
    card2remove = input("Which card?\n")
    if card2remove in flashcard_dictionary.keys():
        del flashcard_dictionary[card2remove]
        print("The card has been removed.\n")
    else:
        print(f'Can\'t remove "{card2remove}": there is no such card.\n')


def import_card(imported_file_name=None):
    try:
        if imported_file_name is not None:
            file_name = imported_file_name
        else:
            file_name = input("File name:\n")
        with open(file_name, "rt") as text:
            n = 0
            flashcard_dictionary = defaultdict(list)
            for line in text:
                _key, _val, _numErr = line[:-1].split(": ")
                n += 1
                flashcard_dictionary.update({_key: [_val, int(_numErr)]})
        print(f'{n} cards have been loaded\n')

        return flashcard_dictionary

    except FileNotFoundError:
        print("File not found.\n")


def export_card(flashcard_dictionary, export_destination=None):
    if export_destination is not None:
        file_name = export_destination
    else:
        file_name = input("File name:\n")
    n = 0
    with open(file_name, "w", encoding="utf-8") as text:
        for _k, _v in flashcard_dictionary.items():
            text.write(_k + ": " + _v[0] + ": " + str(_v[1]) + "\n")
            n += 1
    print(f'{n} cards have been saved.\n')


def ask_definition(flashcard_dictionary):
    num_question = int(input("How many times to ask?\n"))
    for _ in range(num_question):
        selected_random_term = random.choice(list(flashcard_dictionary.keys()))
        ans = input(f'Print the definition of "{selected_random_term}":\n')
        correct_answer = flashcard_dictionary[selected_random_term][0]
        if ans == correct_answer:
            print("Correct!\n")
        elif ans in [flashcard_dictionary[_key][0] for _key in flashcard_dictionary.keys()]:
            k = [k for k, v in flashcard_dictionary.items() if v[0] == ans]
            flashcard_dictionary[selected_random_term][1] += 1
            print(f'Wrong. The right answer is "{correct_answer}", but your definition is correct for "{k[0]}"\n')
        else:
            flashcard_dictionary[selected_random_term][1] += 1
            print(f'Wrong. The right answer is "{correct_answer}"\n')


def log():
    file_name = input("File name:\n")
    shutil.copy(default_log, file_name)
    print("The log has been saved.\n")


def hardest_card(flashcard_dictionary):
    try:
        cur_hardest_card_val = max([flashcard_dictionary[_key][1] for _key in flashcard_dictionary.keys()])
        if cur_hardest_card_val == 0:
            print("There are no cards with errors.\n")
        else:
            cur_hardest_card = [k for k, v in flashcard_dictionary.items() if v[1] == cur_hardest_card_val]
            if len(cur_hardest_card) == 1:
                print(f'The hardest card is "{cur_hardest_card[0]}". '
                      f'You have {cur_hardest_card_val} errors answering it.\n')
            else:
                print('The hardest cards are', end=' "')
                print(*cur_hardest_card, sep='", "', end='". ')
                print(f'You have {cur_hardest_card_val} errors answering them.\n')
    except ValueError:
        print("There are no cards with errors.\n")


def reset_stats(flashcard_dictionary):
    for _key in flashcard_dictionary.keys():
        flashcard_dictionary[_key][1] = 0
    print("Card statistics have been reset.\n")


# MAIN
action_list = ["add", "remove", "import", "export", "ask", "exit", "log", "hardest card", "reset stats"]
flashcard_dict = defaultdict(list)
export_flag = False

default_log = 'temp.txt'
sys.stdout = LoggerOut(default_log)
sys.stdin = LoggerIn(default_log)

parser = argparse.ArgumentParser()
parser.add_argument("--import_from")
parser.add_argument("--export_to")
args = parser.parse_args()

if args.import_from is not None:
    imported_file = args.import_from
    flashcard_dict = import_card(imported_file)
if args.export_to is not None:
    export_flag = True
    export_filename = args.export_to
    export_card(flashcard_dict, export_filename)


while True:
    action = input("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n")

    while action not in action_list:
        action = input("Input action from the list (add, remove, import, export, ask, exit, log, "
                       "hardest card, reset stats):\n")

    if action == "add":
        add_card(flashcard_dict)

    elif action == "remove":
        remove_card(flashcard_dict)

    elif action == "import":
        flashcard_dict = import_card()

    elif action == "export":
        export_card(flashcard_dict)

    elif action == "ask":
        ask_definition(flashcard_dict)

    elif action == "log":
        log()

    elif action == "hardest card":
        hardest_card(flashcard_dict)

    elif action == "reset stats":
        reset_stats(flashcard_dict)

    else:
        if export_flag is True:
            export_card(flashcard_dict, export_filename)
        print("Bye Bye!\n")
        break
