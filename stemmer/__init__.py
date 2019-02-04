import re
import subprocess
subprocess.call(['java', '-cp', 'stanford-postagger.jar', 'edu.stanford.nlp.tagger.maxent.MaxentTagger', '-model',
             'filipino-left5words-owlqn2-distsim-pref6-inf2.tagger', '-textFile', 'inputText.txt', '-outputFormat',
             'tsv', '-outputFile', 'Postagged_words.tag'])

#Read tag words
def postTagged(n):
    rules = []
    i = 1
    with open('Postagged_words.tag') as fp:
        if n > i:
            while True:
                line = fp.readline()
                temp = re.findall(r"[\w']+|[+|,.?]", line)
                if temp[0] == '.' or temp[0] == '?':
                    break
            i += 1
        line = fp.readline()
        while line:
            temp = re.findall(r"[\w']+|[-+|,.?]", line)
            if len(temp) > 2:
                temp = [temp[0] + temp[1] + temp[2], temp[3] ]

            rules.append(temp)
            if temp[0] == '.' or temp[0] == '?':
                fp.close()
                return rules
            line = fp.readline()

    fp.close()
    return rules


def stem():
    toStem = (postTagged(1))
    x = 0
    while x < len(toStem):
        print(toStem[x][1])
        if str(toStem[x][1]).__contains__("_CCP"):
            print(toStem[x][1])
            word = str(toStem[x][0])
            tag = str(toStem[x][1])
            leng1 = len(word)
            leng2 = len(tag)
            word = word[0:leng1 - 1]
            toStem[x][1] = tag[0:leng2 - 4]
            flag = 1

            with open('Eng_Fil_1.csv') as fp:
                line = fp.readline()
                while line:
                    temp = re.findall(r"[\w']+|[+|/ ]", line)
                    if str(temp[1]).lower() == str(word).lower():
                        toStem[x][0] = word
                        print(toStem[x][0])
                        flag = 0
                        break
                    line = fp.readline()
            fp.close()

            if flag == 1:
                toStem[x][0] = word[0:leng1 - 2]

            # print("Stem: ", toStem[x][0])


        x += 1

    return toStem

def rootWord():
    toRoot = stem()
    verbUnlapi =['nakipag', 'nakikipag,' 'magpapa', 'magpa', 'mapagma', 'magkasing', 'mapang', 'kaka', 'kapapa','ka', 'nakapag', 'pinag', 'pina', 'mag', 'mai',  'makapag',  'mang',  'man',  'mapa'  'ma',   'nag',  'nang',  'nam', 'nai',  'na', 'pinag', 'ipinang', 'ni', 'i', 'tagapag','taga', 'tiga']
    adjUnlapi = ['kasing', 'magsing', 'sing', 'pinaka', 'mapang', 'mapam', 'ma', 'pang', 'pan', 'pala']
    nounUnlapi = ['tagapag', 'tigapag',  'taga',  'tiga',  'pakikipag',  'pag', 'man']

    for toRoot in toRoot:
        #print(toRoot[0])
        if str(toRoot[1]).__contains__("VB"):
            #unlapi
            for vp in verbUnlapi:
                if vp == str(toRoot[0])[0:len(vp)].lower():
                    print("->", vp)
                    toRoot[0] = (toRoot[0])[len(vp): len(toRoot[0])]
                    break
            #inuulit
            if str(toRoot[0])[0:2].lower() == (toRoot[0])[2:4].lower():
                toRoot[0] = (toRoot[0])[2: len(toRoot[0])]


            #gitlapi
            if str(toRoot[0]).lower().__contains__("umi"):
                toRoot[0] = (toRoot[0])[4: len(toRoot[0])]

            elif str(toRoot[0]).lower().__contains__("um"):
                toRoot[0] = (toRoot[0])[0] + (toRoot[0])[3: len(toRoot[0])]

            elif str(toRoot[0]).lower().__contains__("in") and str(toRoot[0]).lower()[0] == 'i':
                toRoot[0] = (toRoot[0])[1] + (toRoot[0])[4: len(toRoot[0])]

            elif str(toRoot[0]).lower().__contains__("in"):
                toRoot[0] = (toRoot[0])[0] + (toRoot[0])[3: len(toRoot[0])]

            #hulapi
            if str(toRoot[0]).lower().__contains__("han"):
                toRoot[0] = (toRoot[0])[0: len(toRoot[0]) - 3]
            elif str(toRoot[0]).lower().__contains__("hin"):
                toRoot[0] = (toRoot[0])[0: len(toRoot[0]) - 3]
            elif (toRoot[0])[len(toRoot)-2: len(toRoot)] == 'an':
                toRoot[0] = (toRoot[0])[0: len(toRoot[0]) - 2]

            print(toRoot[0])

        elif str(toRoot[1]).__contains__("JJ") or str(toRoot[1]).__contains__("RBD"):
            for adj in adjUnlapi:
                if adj == str(toRoot[0])[0:len(adj)].lower():
                    print("->", adj)
                    toRoot[0] = (toRoot[0])[len(adj): len(toRoot[0])]
                    print(toRoot[0])
                    break

        elif str(toRoot[1]).__contains__("NNC"):
            for nn in nounUnlapi:
                if nn == str(toRoot[0])[0:len(nn)].lower():
                    print("->", nn)
                    toRoot[0] = (toRoot[0])[len(nn): len(toRoot[0])]
                    print(toRoot[0])
                    break

rootWord()
print('Done')