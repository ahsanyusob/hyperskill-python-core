import random
import logging


# DEF
def add_card(flashcard_dictionary):
    _key = input(f"The term for card:\n")
    while _key in flashcard_dictionary.keys():
        _key = input(f'The term "{_key}" already exists. '
                     f'Try again::\n')
    _val = input(f"The definition for card:\n")
    while _val in flashcard_dictionary.values():
        _val = input(f'The definition "{_val}" already exists. '
                     f'Try again::\n')
    flashcard_dictionary.update({_key: _val})
    print(f'The pair ("{_key}":"{_val}") has been added.')

    print()


def remove_card(flashcard_dictionary):
    card2remove = input("Which card?\n")
    if card2remove in flashcard_dictionary.keys():
        del flashcard_dictionary[card2remove]
        print("The card has been removed.")
    else:
        print(f'Can\'t remove "{card2remove}": there is no such card.')

    print()


def import_card():
    flashcard_dictionary = dict()
    file_name = input("File name:\n")
    try:
        n = 0
        with open(file_name, "rt") as text:
            for line in text:
                _key, _val = line.split(": ")
                n += 1
                flashcard_dictionary.update({_key: _val[:-1]})
        print(f'{n} cards have been loaded')
        print()
        return flashcard_dictionary

    except FileNotFoundError:
        print("File not found.")


def export_card(flashcard_dictionary):
    file_name = input("File name:\n")
    n = 0
    with open(file_name, "w", encoding="utf-8") as text:
        for _k, _v in flashcard_dictionary.items():
            text.write(_k + ": " + _v + "\n")
            n += 1
    print(f'{n} cards have been saved.')


def ask_definition(flashcard_dictionary):
    num_question = int(input("How many times to ask?\n"))
    for _ in range(num_question):
        selected_term = random.choice(list(flashcard_dictionary.keys()))
        ans = input(f'Print the definition of "{selected_term}":\n')
        correct_answer = flashcard_dictionary[selected_term]
        if ans == correct_answer:
            print("Correct!")
        elif ans in flashcard_dictionary.values():
            k = [k for k, v in flashcard_dictionary.items() if v == ans]
            print(f'Wrong. The right answer is "{correct_answer}", but your definition is correct for "{k[0]}"')
        else:
            print(f'Wrong. The right answer is "{correct_answer}"')

    print()


def log(flashcard_dictionary):
    pass


def hardest_card(flashcard_dictionary):
    pass


def reset_stats(flashcard_dictionary):
    pass


# MAIN
action_list = ["add", "remove", "import", "export", "ask", "exit", "log", "hardest card", "reset stats"]
flashcard_dict = dict()

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
        log(flashcard_dict)
    
    elif action == "hardest card":
        hardest_card(flashcard_dict)
    
    elif action == "reset stats":
        reset_stats(flashcard_dict)

    else:
        print("Bye Bye!")
        break
