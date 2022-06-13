inp = '1,,473,6'
questions = [
    ['location', ['1','2']],
    ['special stuff', ['3','4']]
]

for q in questions:
    print(q[0])
    for i in q[1]:
        print(i, inp.count(i))

'''
f = {'x':7}
print(list(f.values()))'''