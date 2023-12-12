from typing import List, Dict
import sys
import json

topics: List[str] = sys.argv[1].split(",")
PATH: str = './'
filename: str = PATH+topics[0]
with open(filename,'r') as fp:
    cards: List[Dict] = json.load(fp)


for card in cards:
    print()
    print(f'Q. {card["q"]}')
    print('X----------X----------X----------X')
    print('[A]how answer')
    print('Mark as [C]orrect :D')
    print('Mark as [I]ncorrect ;_;')
    print('Agai[N] >:)')
    print('[S]ave :)')
    print('[Q]uit x)')
    choice = input()
    if choice == 's':
        with open(filename,'w') as fp:
            json.dump(cards,fp)
    elif choice == 'q':
        with open(filename,'w') as fp:
            json.dump(cards,fp)
        break;
    elif choice == 'a':
        print(f'A. {card['a']}')
    elif choice == 'c':
        card['s'] += 5
        print(f'Score = {card["s"]}')
        continue
    elif choice == 'i':
        card['s'] -= 5
        print(f'Score = {card["s"]}')
        continue

print('Summary')
print('-------')
print(f'Topic: {topics[0]}')
score = sum(card['s'] for card in cards)/len(cards)
print(f'Score: {round(score,2)}%')
print('Bye Bye')
