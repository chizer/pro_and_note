import re

s = "psychoanalytic   [ psychoanalysis: ] psychoanalytic"
patten=r'(\w+)\s+(.+)'

a = re.findall(patten,s)
print(a)