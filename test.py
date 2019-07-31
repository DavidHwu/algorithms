from collections import defaultdict


test = set()
if test:
    print('exists')
else:
    print('not exists')

test = set()
print(type(test))
test.add('orange')
print(test)
test.remove('orange')
print(test)

s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
d = defaultdict(list)
for k, v in s:
    d[k].append(v)

print(d.items())
