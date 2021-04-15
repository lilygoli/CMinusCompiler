


def get_dictionary(file_name):
    # first_sets, follow_sets, predicate_sets
    name = "parserdata/" + file_name + ".txt"
    file = open(name, 'r')

    Lines = file.readlines()
    count = 0
    tokens = []
    info = {}
    for line in Lines:
        count += 1
        s = line.strip()
        if count == 1:
            tokens = s.split("\t")
        else:
            a = s.split("\t")
            rule_id = a[0]
            l = []
            for i in range(1, len(a)):
                if a[i] == "+":
                    l.append(tokens[i - 1])
            info[rule_id] = l
    return info

first = get_dictionary("first_sets")
follow = get_dictionary("follow_sets")

lili_command = ["B", "H", "Statement", "Statementlist"]

for i in lili_command:
    print(i, "__________")
    print("first set is")
    print(first[i])
    print("follow set is")
    print(follow[i])