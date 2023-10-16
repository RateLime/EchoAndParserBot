import random
import json
with open("dicts/dic.json", 'r', encoding='utf-8') as f:
    dice = json.load(f)

m="O"
def dict():

    return dice

def rand(message):

    keys = list(dice.keys())
    random_index = random.randint(0, len(keys) - 1)
    random_key = keys[random_index]
    random_value = dice[random_key]
    if "тебя" in message or "ты" in message:
        return random_value
    else:
        create(random_value, message)
        return random_value
def create(n,m):
    dice[n] = m
    with open("dicts/dic.json", 'w', encoding='utf-8') as f:
        json.dump(dice, f, ensure_ascii=False, indent=4)
