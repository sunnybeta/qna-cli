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


PATH: str = os.path.dirname(os.path.abspath(__file__))
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
    print('* Create Topic (ct)')
    print('* Add Card     (ac)')
    print('* Modify Topic (mt)')
    print('* Modify Card  (mc)')
    print('* Revise       (r)')
    print('* Quit         (q)')
    print('* Repeat       (0)')


def create_topic() -> None:
    new_topic = input()
    filename = new_topic.strip(' ').lower()
    os.mkdir(PATH + filename)

def main_menu_nav() -> None:
    choice = input()
    if choice == '0':
        main_menu()
        main_menu_nav()
    if choice == 'ct':
        list_topics()


@padding
def list_topics() -> List[str]:
    topics = []
    for _, _, filenames in os.walk(PATH):
        topics = [filename for filename in filenames if filename != '__init__.py' and filename != 'main.py']
    for topic in topics:
        print(f'* {topic.replace('.json','').upper()}')
    return topics

@padding
def select_topic(topics: List[str]) -> str:
    print('Choose a topic:')
    selection = input()
    if selection.lower() in topics:
        return selection.lower()
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

def save(cards: List[Dict], topic: str) -> None:
    """
    Save the currect set of card scores
    """
    filename = PATH + topic
    with open(filename,'w') as fp:
        json.dump(cards,fp)

def load(topic: str) -> List[Dict]:
    """
    Load cards of a particular topic
    """
    filename = PATH + topic
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

def test(card) -> None | str:
    """
    Ask question on a particular card
    """
    ask_question(card['q'])
    revision_options()
    response = input()
    if response == 'e':
        return response
    if response == 's':
        pass
    # handle a c i n s e options
    return 

def revise(topic: str) -> None:
    cards = load(topic)
    for card in cards:
        response = test(card)
        if response == 1:
            update_score(card)
        elif response == -1:
            update_score(card, False)
        else:
            update_score(card)
        if response == 'e':
            break;
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


def add_question(topic):
    q,a = get_qna()
    cards = load(topic=topic)
    cards.append({'q':q, 'a':a, 's':[0]})
    save(cards=cards, topic=topic)


def get_qna():
    print('Q.', end=' ')
    q = input()
    print('Q.', end=' ')
    a = input()
    return q,a

def main():
    welcome()
    while True:
        main_menu()
        break;


if __name__ == '__main__':
    main()

