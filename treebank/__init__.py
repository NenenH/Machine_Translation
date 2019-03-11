import re

def postTagged(n):
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

def phrase():
    sentence = (postTagged(1))
    phrase = []
    phraseList = []
    print(sentence)
    x = 0
    while x < len(sentence):
        print(x)
        if str(sentence[x][1]).__contains__("JJ"):
            # print(sentence[x])
            print("yes")
            while not str(sentence[x][1]).__contains__("VB"):
                phrase.append(sentence[x])
                x += 1
            phraseList.append(phrase)
            phrase = []
            print(phraseList)
            x -= 1

        elif str(sentence[x][1]).__contains__("VB"):
            print(sentence[x])
            while not str(sentence[x][1]).__contains__("JJ"):
                phrase.append(sentence[x])
                x+=1
            phraseList.append(phrase)
            phrase = []
            print(phraseList)
            x -= 1

        x+=1
    return phraseList
#
# def phraseB():
#
#     sentence = (postTagged(1))
#     phrase = []
#     phraseList = []
#     print(sentence)



print(phrase())





