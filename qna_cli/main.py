import sys
import os
from typing import List, Dict
from operator import add, sub
import json

"""
Screens

Options on Screens
Naviate to other Screens

Global State Management: topic
"""


TOPIC = ''

PATH: str = os.path.dirname(os.path.abspath(__file__)) + '/'
UPDATE_SCORE: int = 5
MAX_SCORE: int = 100
MIN_SCORE: int = 0

def padding(func):
    """
    Decorator to add an empty line at the beginning and end of functions
    """
    def wrapper(*args, **kwargs):
        print()
        res = func(*args, **kwargs)
        print()
        return res
    return wrapper

@padding
def welcome() -> None:
    """
    Disaply Welcome Message
    """
    print("QnA")
    print("===")
    print("Welcome to QnA")

@padding
def main_menu() -> None:
    """
    Display options of the Main Menu
    """
    print('* Add Topic    (at)')
    print('* Add Card     (ac)')
    print('* List Topic   (lt)')
    print('* List Card    (lc)')
    print('* Revise       (r)')
    print('* Quit         (q)')
    # print('* Modify Topic  (mt)')
    # print('* Modify Card   (mc)')


def create_topic() -> None:
    new_topic = input()
    filename = new_topic.strip(' ').lower()
    os.mkdir(PATH + filename)

def force_select_topic():
    if not TOPIC:
        select_topic(list_topics())

def nav() -> None:
    choice = input().lower()
    if choice == 'at':
        add_topic()
    elif choice == 'lt':
        list_topics()
    elif choice == 'lc':
        force_select_topic()
        list_cards()
    elif choice == 'ac':
        force_select_topic()
        add_question()
    elif choice == 'r':
        force_select_topic()
        revise()
    elif choice == 'q':
        quit()
    print("X - - - * - - - X - - - * - - - X")
    main_menu()
    nav()

def quit():
    sys.exit()

@padding
def list_topics() -> List[str]:
    topics = []
    for _, _, filenames in os.walk(PATH):
        topics = [filename.replace('.json','').lower() for filename in filenames if filename != '__init__.py' and filename != 'main.py']
    for topic in topics:
        print(f'* {topic.upper()}')
    return topics

@padding
def select_topic(topics: List[str]) -> str | None:
    global TOPIC
    print('Choose a topic:', end = ' ')
    selection = input().lower()
    if selection in topics:
        TOPIC = selection
        return
    return select_topic(topics)

@padding
def ask_question(question: str) -> None:
    """
    Print Question
    """
    print(f'Q. {question}')

@padding
def show_answer(answer: str) -> None:
    """
    Show answer to the cheater
    """
    print(f'A. {answer}')

def update_score(card: dict, correct=True) -> None:
    """Increase or decrease score by 5
    """
    if (card['s'] == MIN_SCORE and not correct) or (card['s'] == MAX_SCORE and correct):
        return
    operator = add if correct else sub
    card['s'] = operator(card['s'], UPDATE_SCORE)

def save(cards: List[Dict]) -> None:
    """
    Save the currect set of card scores
    """
    filename = PATH + TOPIC + '.json'
    with open(filename,'w') as fp:
        json.dump(cards,fp, indent=2)

def display_card(card):
    print('---')
    ask_question(card['q'])
    print('.')
    show_answer(card['a'])
    print('---')

def list_cards():
    cards = load();
    for card in cards:
        display_card(card)

def load() -> List[Dict]:
    """
    Load cards of a particular topic
    """
    filename = PATH + TOPIC + '.json'
    with open(filename,'r') as fp:
        cards = json.load(fp)
    return cards

@padding
def revision_options() -> None:
    """
    Display Options While Revising Questions"
    """
    print('* Show [A]nswer        :O')
    print('* Mark as [C]orrect    :D')
    print('* Mark as [I]ncorrect  ;_;')
    print('* Agai[N]             >:)')
    print('* [S]ave               :)')
    print('* [E]nd                x)')

def test(card) -> str | int | None:
    """
    Ask question on a particular card
    """
    ask_question(card['q'])
    revision_options()
    response = input()
    if response == 'c':
        return 1
    if response == 'i':
        return -1
    if response == 'n':
        return 0 
    if response == 'e':
        return 'e'
    if response == 's':
        return 's'
    if response == 'a':
        show_answer(card['a'])
        test(card)

def revise() -> None:
    cards = load()
    for card in cards:
        response = test(card)
        if response == 1:
            update_score(card)
        elif response == -1:
            update_score(card, False)
        if response == 'e':
            break;
        if response == 's':
            break;
    save(cards)
    del cards

@padding
def summarize(topic: str, cards: List[Dict]) -> None:
    print('Summary')
    print('+++++++')
    print()
    print(f'Topic: {topic}', end=' ')
    score = sum(card['s'] for card in cards)/len(cards)
    print(f'Score: {round(score,2)}%')
    print()
    print('Bye Bye')


@padding
def add_topic():
    print('Topic Name:', end=' ')
    name = input()
    filename = PATH + name.lower() + '.json' 
    if os.path.isfile(filename):
        print()
        print('Topic already exists')
        print()
        return
    with open(filename,'w') as fp:
        fp.write('[]')
    print('Topic Created Successfully')


@padding
def add_question():
    print('Q.', end=' ')
    q = input()
    print('A.', end=' ')
    a = input()
    cards = load()
    cards.append({'q':q, 'a':a, 's':0})
    save(cards=cards)


def main():
    welcome()
    main_menu()
    nav()

if __name__ == '__main__':
    main()

