from poem_mapper_v2 import *
from time import sleep
from pprint import pprint

model = loadGlove()

with open("examples.txt", "r") as f:
    for line in f.readlines():
        print(line)
        pprint(getQuoteForInput(line, model))