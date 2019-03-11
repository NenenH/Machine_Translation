import re


class Stack:

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)

    def show(self):
        return self.items


def parseSentence(n):
    rules = []
    i = 1
    with open('Postagged_words.txt') as fp:
        if n > i:
            while True:
                line = fp.readline()
                temp = re.findall(r"[\w']+|[+|,.]", line)
                if temp[0] == '.':
                    break
            i += 1
        line = fp.readline()
        while line:
            temp = re.findall(r"[\w']+|[+|,.]", line)
            rules.append(temp)
            if temp[0] == '.':
                fp.close()
                return rules
            line = fp.readline()

    fp.close()
    return rules

def countSentence():
    i = 0
    with open('Postagged_words.txt') as fp:
        line = fp.readline()
        while line:
            temp = re.findall(r"[\w']+|[+|,.]", line)
            if temp[0] == '.':
                i += 1
            line = fp.readline()

    fp.close()
    return i

def translate(word, prev, next, current):
    translated = ''

    if current != 'D':
        with open('db.csv') as fp:
            line = fp.readline()
            while line:
                temp = re.findall(r"[\w']+|[+|/ ]", line)
                if temp[1] == word:
                    translated = temp[0]
                    return translated
                line = fp.readline()
        if str(word).lower() == 'ko' and prev == 'N':
            translated = 'my'
        elif str(word).lower() == 'ko' and prev == 'V':
            translated = 'I'
        elif prev == 'Q':
            translated = translated + 's'
        elif str(word).lower() == 'ay' and next == 'V':
            translated = ''
        elif translated == '':
            translated = word

    elif current == 'D':
        if str(word).lower() == 'ang':
            if next == 'A' or next == 'N':
                translated = 'the'
            elif next == 'V':
                translated = 'the one who'
            elif next == 'P':
                translated = 'the one who is'

        elif str(word).lower() == 'ay':
            if next == 'A' or next == 'N' or next == 'P' or next == 'D':
                translated = 'is'

        elif str(word).lower() == 'sina':
            if next == 'N':
                translated = 'both'

        elif str(word).lower() == 'sa':
            if next == 'A' or next == 'N':
                translated = 'to the'

        elif str(word).lower() == 'ni' or str(word).lower() == 'kina':
            if prev == 'V':
                translated = 'by'
            elif next == 'N':
                translated = 'of'

        elif str(word).lower() == 'nang':
            if next == 'V':
                translated = 'when'

        elif str(word).lower() == 'ng':
            if next == 'ADV':
                translated = 'to'

    return translated


def parse(r):
    prev = ''
    next = ''
    output = ''
    node = ''
    translation = ''
    phrase = ''
    check = ''
    under = ''
    subconj = ''

    subjects = []
    # objects = []
    pandesal = []

    n = 0
    index = 0
    parenthesis = 0
    loop = 0

    m = False

    tree = Stack()

    sentence = parseSentence(r)

    tree.push('S')

    while not tree.isEmpty():
        if not tree.isEmpty():
            node = tree.pop()

        if next == 'PERIOD':
            current = 'PERIOD'
        if index > 0:
            prev = sentence[index-1][1]
        if len(sentence) > index:
            current = sentence[index][1]
        if current != 'PERIOD':
            next = sentence[index + 1][1]

        if current == 'C' and str(sentence[index][0]).lower() != 'o' and str(sentence[index][0]).lower() != 'at' and index == 0:
            subconj = translate(sentence[index][0], prev, next, current)


        if node == 'S':
            if current == 'V' or current == 'ADV':
                tree.push('PERIOD')
                tree.push("S'")
                tree.push('VP')
            elif current == 'D' or current == 'Q':
                tree.push('PERIOD')
                tree.push("S'")
                tree.push('DP')
                check = 'DP'
            elif current == 'P' or current == 'ADV':
                tree.push('PERIOD')
                tree.push("S'")
                tree.push('PP')
            elif current == 'A' or current == 'ADV':
                tree.push('PERIOD')
                tree.push("S'")
                tree.push('AP')
            elif current == 'N' or current == 'A':
                tree.push('PERIOD')
                tree.push("S'")
                tree.push('NP')
                check = 'NP'
            elif current == 'C':
                tree.push('PERIOD')
                tree.push("S'")
            parenthesis += 1

        elif node == "S'":
            if current == 'C':
                tree.push("S'")
                tree.push('translate')
                tree.push('C')
            elif current == 'V' or current == 'ADV':
                tree.push("S'")
                tree.push('VP')
            elif current == 'D' or current == 'Q':
                tree.push("S'")
                tree.push('DP')
            elif current == 'P' or current == 'ADV':
                tree.push("S'")
                tree.push('PP')
            elif current == 'A' or current == 'ADV':
                tree.push("S'")
                tree.push('AP')
            elif current == 'N' or current == 'A':
                tree.push("S'")
                tree.push('NP')
            elif current == 'COMMA':
                tree.push("S'")
                tree.push('COMMA')
            if current is not '.':
                output = output + node + "("
                parenthesis += 1
            under = "S'"

        elif node == 'VP':
            if current == 'V':
                tree.push('translate')
                tree.push('ADV')
                tree.push("V'")
            else:
                tree.push('translate')
                tree.push("V'")
                tree.push('ADV')
            output = output + node + "("
            parenthesis += 1

        elif node == 'DP':
            if sentence[index][0] == 'si' or sentence[index][0] == 'sina' or sentence[index][0] == 'kina' or (sentence[index][0] == 'ang' and (under != "S'" and under != 'VP')):
                check = 'DP'
                m = False
            elif ((sentence[index][0] == 'ang' and under != '') or sentence[index][0] == 'ng') or (sentence[index][0] == 'ay' and (next == 'N' or next == 'A')) or sentence[index][0] == 'ni':
                check = 'DP'
                m = True

            if current == 'D':
                tree.push('translate')
                tree.push('Q')
                tree.push("D'")
            else:
                tree.push('translate')
                tree.push("D'")
                tree.push('Q')
            output = output + node + "("
            parenthesis += 1

        elif node == 'PP':
            if current == 'P':
                tree.push('translate')
                tree.push('ADV')
                tree.push("P'")
            else:
                tree.push('translate')
                tree.push("P'")
                tree.push('ADV')
            output = output + node + "("
            parenthesis += 1

        elif node == 'AP':
            if current == 'A':
                tree.push('translate')
                tree.push('ADV')
                tree.push("A'")
            else:
                tree.push('translate')
                tree.push("A'")
                tree.push('ADV')
            output = output + node + "("
            parenthesis += 1

        elif node == 'NP':
            if current == 'N' and next == 'A':
                tree.push('translate')
                tree.push('AP')
                tree.push("N'")
            elif current == 'A':
                tree.push('translate')
                tree.push("N'")
                tree.push('AP')
            else:
                tree.push('translate')
                tree.push("N'")
            output = output + node + "("
            parenthesis += 1

        elif node == "V'":
            under = 'VP'
            if current == 'V' and (next == 'D' or next == 'Q'):
                tree.push('DP')
                tree.push('V')
            elif next == 'V' and (current == 'D' or current == 'Q'):
                tree.push('V')
                tree.push('DP')
            elif current == 'V' and not (next == 'D' or next == 'Q'):
                tree.push('V')
            output = output + node + "("
            parenthesis += 1

        elif node == "D'":
            if current == 'D' and (next == 'N' or next == 'A'):
                tree.push('NP')
                tree.push('D')
            elif next == 'D' and (current == 'N' or current == 'A'):
                tree.push('D')
                tree.push('DP')
            elif current == 'D' and not (next == 'N' or next == 'A'):
                tree.push('D')
            output = output + node + "("
            parenthesis += 1

        elif node == "P'":
            if current == 'P' and (next == 'D' or next == 'Q'):
                tree.push('DP')
                tree.push('P')
            elif next == 'P' and (current == 'D' or current == 'Q'):
                tree.push('P')
                tree.push('DP')
            elif current == 'P' and not (next == 'D' or next == 'Q'):
                tree.push('P')
            output = output + node + "("
            parenthesis += 1

        elif node == "A'":
            if current == 'A' and (next == 'D' or next == 'Q'):
                tree.push('DP')
                tree.push('A')
            elif next == 'A' and (current == 'D' or current == 'Q'):
                tree.push('A')
                tree.push('DP')
            elif current == 'A' and not (next == 'D' or next == 'Q'):
                tree.push('A')
            output = output + node + "("
            parenthesis += 1

        elif node == "N'":
            if current == 'N' and (next == 'D' or next == 'ADV'):
                tree.push('DP')
                tree.push('N')
            elif next == 'N' and (current == 'D' or current == 'ADV'):
                tree.push('N')
                tree.push('DP')
            elif current == 'N' and not (next == 'D' or next == 'ADV'):
                tree.push('N')
            output = output + node + "("
            parenthesis += 1

        elif node == 'translate':
            if check is not 'DP':
                check = ''
                if phrase is not '':
                    if not m:
                        subjects.append(phrase.strip())
                    #else:
                     #   objects.append(phrase.strip())
                    phrase = ''
            else:
                check = 'NP'

        elif node == current:
            output = output + node + "(" + sentence[index][0] + ")"

            if next != '.' and loop <= 0:
                if current == 'N' and sentence[index + 1][0] == 'na' and sentence[index + 2][1] == 'A':
                    translation = translation.strip() + ' ' + translate(sentence[index + 2][0], prev, next, current) + ' ' + translate(sentence[index][0], prev, next, current)
                    loop = 2
                elif current == 'A' and sentence[index + 1][0] == 'na' and sentence[index + 2][1] == 'V':
                    translation = translation.strip() + ' ' + translate(sentence[index + 2][0], prev, next, current) + ' ' + translate(sentence[index][0], prev, next, current)
                    loop = 2
                elif current == 'N' and sentence[index + 1][0] == 'ng' and sentence[index + 2][1] == 'N':
                    translation = translation.strip() + ' ' + translate(sentence[index][0], prev, next, current) + ' ' + 'of' + ' ' + translate(sentence[index + 2][0], prev, next, current)
                    loop = 3
                elif current == 'A' and sentence[index + 1][0] == 'ng' and sentence[index + 2][1] == 'N':
                    translation = translation.strip() + ' ' + translate(sentence[index][0], prev, next, current) + ' ' + 'of' + ' ' + 'the'
                    loop = 2
                elif current == 'N' and sentence[index + 1][0] == 'ni' and sentence[index + 2][1] == 'N':
                    translation = translation.strip() + ' ' + translate(sentence[index][0], prev, next, current) + ' ' + 'of' + ' ' + translate(sentence[index + 2][0], prev, next, current)
                    loop = 2
                elif current == 'N' and sentence[index + 1][0] == 'ay' and (sentence[index + 2][1] == 'A' or sentence[index + 2][1] == 'P'):
                    if sentence[index][0] == 'kami' or sentence[index][0] == 'sila' or sentence[index][0] == 'tayo':
                        translation = translation.strip() + ' ' + translate(sentence[index][0], prev, next, current) + ' ' + 'are' + ' ' + translate(sentence[index + 2][0], prev, next, current)
                        loop = 2
                elif current == 'N' and sentence[index + 1][0] == 'ay' and sentence[index + 2][1] == 'V':
                    if sentence[index + 3] == 'ni' or sentence[index + 3] == 'nina' or sentence[index + 3] == 'kay':
                        translation = translation.strip() + ' ' + translate(sentence[index][0], prev, next, current) + ' ' + 'is' + ' ' + translate(sentence[index + 2][0], prev, next, current)
                    else:
                        translation = translation.strip() + ' ' + translate(sentence[index][0], prev, next, current) + ' ' + translate(sentence[index + 2][0], prev, next, current)
                    loop = 2
                elif current == 'V' and sentence[index + 1][0] == 'ng' and (sentence[index + 2][1] == 'ADV' or sentence[index + 2][1] == 'A'):
                    translation = translation.strip() + ' ' + translate(sentence[index][0], prev, next, current) + ' ' + translate(sentence[index + 2][0], prev, next, current)
                    loop = 2
                elif current == 'P' and sentence[index + 1][0] == 'kay' and sentence[index + 2][1] == 'N':
                    translation = translation.strip() + ' ' + translate(sentence[index][0], prev, next, current) + ' ' + translate(sentence[index + 2][0], prev, next, current)
                    loop = 2
                elif current == 'V' and sentence[index + 1][0] == 'kay' and sentence[index + 2][1] == 'N':
                    translation = translation.strip() + ' ' + translate(sentence[index][0], prev, next, current) + ' ' + 'to' + ' ' + translate(sentence[index + 2][0], prev, next, current)
                    loop = 2
                elif current == 'Q' and sentence[index + 1][1] == 'N' and sentence[index + 2][0] == 'ay' and sentence[index + 3][1] == 'A':
                    translation = translation.strip() + ' ' + translate(sentence[index][0], prev, next, current) + ' ' + translate(sentence[index + 1][0], prev, next, current) + ' ' + 'are' + ' ' + translate(sentence[index + 3][0], prev, next, current)
                    loop = 3
                elif current != 'D':
                    translation = translation.strip() + ' ' + translate(sentence[index][0], prev, next, current)
                else:
                    translation = translation.strip() + ' ' + translate(sentence[index][0], prev, next, current)
            elif current != 'D' and loop < 0:
                translation = translation.strip() + ' ' + translate(sentence[index][0], prev, next, current)

            if node == 'V':
                pandesal.append(translate(sentence[index][0], prev, next, current))

            if not m:
                if check is not '':
                    phrase = phrase + translate(sentence[index][0], prev, next, current)

                if current == 'V' and next == 'N':
                    if sentence[index + 1][0] == 'kita':
                        subjects.append('I ' + translate(sentence[index][0], prev, next, current) + ' you')
                    else:
                        prev = 'V'
                        subjects.append(translate(sentence[index + 1][0], prev, next, current))

            else:
                if check is not '':
                    phrase = phrase + translate(sentence[index][0], prev, next, current) + ' '

            index += 1
            n += 1
            loop -= 1

        if not tree.isEmpty():
            if tree.peek() == "S'":
                while parenthesis > 1:
                    output = output + ")"
                    parenthesis -= 1

    while parenthesis > 0:
        output = output + ")"
        parenthesis -= 1

    #print(subconj)
    #print('====================REGEX=====================')
    #print(output)
    #print('============WORD-BY-WORD TRANSALATION=========')
    #print(translation)
    #print('===================SUBJECTS===================')
    #print(subjects)
    #print('===================OBJECTS====================')
    #print(objects)
    #print('===================PANDESAL===================')
    #print(pandesal)


    for i in subjects:
        i = str(i).split()
        for n in i:
            translation = translation.replace(n, '').strip()

    for i in pandesal:
        i = str(i).split()
        for n in i:
            translation = translation.replace(n, '').strip()
    '''
    for i in objects:
        i = str(i).split()
        for n in i:
            translation = translation.replace(n, '').strip()
    '''

    translation = translation.strip()

    #print('============MISC. WORDS(STRIPED)==============')
    #print(translation)

    if subjects == []:
        subjects.append('')
    if pandesal == []:
        pandesal.append('')
    #if objects == []:
    #    objects.append('')

    translation = translation.replace(subconj,'')

    #print('===========TRANSALATION(OUTPUT)===============')

    outputfile = open('output.txt', 'a')
    outputfile.write(subconj)
    print(subconj, end = '')
    if subconj is not '':
        outputfile.write(' ')
        print(' ', end = '')
    outputfile.write((str(subjects[0]).strip() + " " + str(pandesal[0]).strip() + " " + str(translation).strip()).strip() + ' ')
    print((str(subjects[0]).strip() + " " + str(pandesal[0]).strip() + " " + str(translation).strip()).strip() + ' ', end = '')
    outputfile.close()

count = countSentence()

currsen = 1

while count >= currsen:
    parse(currsen)
    currsen += 1
