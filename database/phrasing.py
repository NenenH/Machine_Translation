import re

# Read Txt file with Post Tagged Words
import subprocess
subprocess.call(['java', '-cp', 'stanford-postagger.jar', 'edu.stanford.nlp.tagger.maxent.MaxentTagger', '-model',
             'filipino-left5words-owlqn2-distsim-pref6-inf2.tagger', '-textFile', 'InputText.txt', '-outputFormat',
             'tsv', '-outputFile', 'Postagged_words.tag'])

#Read tag words
def postTagged():
    rule = []
    rules = []
    with open('Postagged_words.tag') as fp:
        line = fp.readline()
        while line:
            temp = re.findall(r"[\w']+|[-+|,.``\"?]", line)
            print(temp)
            if len(temp) > 2:
                if temp[0] == '`' or temp[1] == 'PMS':
                    temp = ["''", 'PMS']
                else:
                    temp = [temp[0] + temp[1] + temp[2], temp[3]]

            if temp != []:
                print(temp)
                rules.append(temp)

                if (temp[0] == '.' or temp[0] == '?'):
                    rule.append(rules)
                    rules = []
                    # fp.close()
                    # return rules
            line = fp.readline()

    fp.close()
    return rule

#Stemmer
def stem(toStem):
    # toStem = (postTagged())
    x = 0
    while x < len(toStem):
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

            print("Stem: ", toStem[x][0])


        x += 1

    return toStem

def rootWord(toRoot):
    verbUnlapi =['nakipag', 'nakikipag,' 'magpapa', 'magpa', 'mapagma', 'magkasing', 'mapang', 'kaka', 'kapapa','ka', 'nakapag', 'pinag', 'pina', 'mag', 'mai',  'makapag',  'mang',  'man',  'mapa'  'ma',   'nag',  'nang',  'nam', 'nai',  'na', 'pinag', 'ipinang', 'ni', 'i', 'tagapag','taga', 'tiga']
    adjUnlapi = ['kasing', 'magsing', 'sing', 'pinaka', 'mapang', 'mapam', 'ma', 'pang', 'pan', 'pala']
    nounUnlapi = ['tagapag', 'tigapag',  'taga',  'tiga',  'pakikipag',  'pag', 'man']
    print(toRoot)

    for toRoot in toRoot:
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
    return toRoot

#Return phrases
def phrase(sentence):
    phrase = []
    phraseList = []
    cc = ['samantala', 'ngunit', 'bagkus', 'kundi', 'imbes', 'kahit', 'maliban', 'bilang', 'bagamat', 'datapwat', 'samantala', 'habang', 'kasi', 'dahil', 'kung', 'sapagkat', 'dahilan', 'palibhasa', 'upang', 'gayundin', 'basta\'t']
    print(sentence)
    x = 0
    while x < len(sentence):
        print("Current: ", sentence[x])

        #phrase start with Conjunction
        if str(sentence[x][1]).__contains__("CC") and not (
                str(sentence[x][1]).__contains__("JJ") or str(sentence[x][1]).__contains__("PRSP")
                or str(sentence[x][1]).__contains__("NN")):
            print("Current Word [CC]: ", sentence[x])
            while not (str(sentence[x][1]).__contains__("VB") or str(sentence[x][1]).__contains__("PMP") or str(
                    sentence[x][1]).__contains__("PMQ") or str(sentence[x][1]).__contains__("JJ")):
                print("Current Word [CC]: ", sentence[x])
                phrase.append(sentence[x])
                x += 1
            phraseList.append(phrase)
            phrase = []
            print(phraseList)
            x -= 1

        # phrase start with Adverb
        elif str(sentence[x][1]).__contains__("RB"):
            print("Current Word [RB]: ", sentence[x])
            while not (str(sentence[x][1]).__contains__("VB") or str(sentence[x][1]).__contains__("PMP") or str(sentence[x][1]).__contains__("PMQ")):
                print("Current Word [RB]: ", sentence[x])
                phrase.append(sentence[x])
                x += 1
            phraseList.append(phrase)
            phrase = []
            print(phraseList)
            x -= 1

        # phrase start with Noun
        elif str(sentence[x][1]).__contains__("NN") and x == 0:
            print("Current Word [NN]: ", sentence[x])
            while not (str(sentence[x][1]).__contains__("VB") or str(sentence[x][1]).__contains__("PMP") or str(
                    sentence[x][1]).__contains__("PMQ")):
                print("Current Word [NN]: ", sentence[x])
                phrase.append(sentence[x])
                x += 1
            phraseList.append(phrase)
            phrase = []
            print(phraseList)
            x -= 1

        # phrase start with Pronoun
        elif str(sentence[x][1]).__contains__("PR") and x == 0:
            print("Current Word [PR]: ", sentence[x])
            phrase.append(sentence[x])
            phraseList.append(phrase)
            phrase = []

        # phrase start with RBW
        elif str(sentence[x][1]).__contains__("RBW"):
            print("Current Word [RBW]: ", sentence[x])
            phrase.append(sentence[x])
            phraseList.append(phrase)
            phrase = []

        # phrase start with LM
        elif str(sentence[x][1]).__contains__("LM") and not str(sentence[x+1][1]).__contains__("VB"):
            print("Current Word [LM]: ", sentence[x])
            phrase.append(sentence[x])
            phraseList.append(phrase)
            phrase = []

        # phrase start with Determiner
        elif str(sentence[x][1]).__contains__("DT"):
            while not (str(sentence[x][1]).__contains__("VB") or str(sentence[x][1]).__contains__("PMP") or str(sentence[x][1]).__contains__("PMQ")):
                print("Current Word [DT]: ", sentence[x])
                phrase.append(sentence[x])
                x += 1
            phraseList.append(phrase)
            phrase = []
            print(phraseList)
            x -= 1


        # phrase start with Adjective
        elif str(sentence[x][1]).__contains__("JJ"):
            while not (str(sentence[x][1]).__contains__("VB") or str(sentence[x][1]).__contains__("PMP") or str(sentence[x][1]).__contains__("PMQ")):
                print("Current Word [JJ]: ", sentence[x])
                phrase.append(sentence[x])
                x += 1
            phraseList.append(phrase)
            phrase = []
            print(phraseList)
            x -= 1

        # phrase start with Verb
        elif str(sentence[x][1]).__contains__("VB"):
            print(sentence[x])
            while not (str(sentence[x][1]).__contains__("PMP") or str(sentence[x][1]).__contains__("PMQ")):
                go = 0
                print("Current Word [VB]: ", sentence[x])
                if (str(sentence[x][1]).__contains__("CC") or str(sentence[x][1]).__contains__("RBW")) and str(sentence[x + 1][1]).__contains__("VB"):
                    print('Dito pumasok')
                    break

                #samantala, ngunit, bagkus, kundi, imbes, kahit, maliban, bilang, bagamat, datapwat, samantala, habang, kasi, dahil, kung, sapagkat, dahilan, palibhasa, upang, gayundin, basta't
                elif str(sentence[x][1]).__contains__("CC") or str(sentence[x][1]).__contains__("RBW"):
                    z = 0
                    while z < len(cc):
                        if str(cc[z]) == str(sentence[x][0]):
                            go = 1
                            break
                        z += 1
                    if go == 1:
                        break

                if str(sentence[x][1]).__contains__("JJ") and not (str(sentence[x-1][1]).__contains__("DT") or str(sentence[x-2][1]).__contains__("JJ") or str(sentence[x][1]).__contains__("JJN")
                                                                   or (str(sentence[x-1][0]).__contains__("ng") and str(sentence[x-1][1]).__contains__("CCB"))):
                    break


                phrase.append(sentence[x])

                x += 1
            phraseList.append(phrase)
            phrase = []
            print(phraseList)
            x -= 1

        x += 1
    phrase = []
    phrase.append(sentence[len(sentence) -1])
    phraseList.append(phrase)
    return phraseList

#Transfer the filipino structure to english structure
def structure(phrases):
    i = 0

    # phrases = phrase()

    print('\n\n')
    while i < len(phrases):
        length = len(phrases[i])
        j = 0

        #VERBAL PHRASE
        if str(phrases[i][0][1]).__contains__("VB"):
            print("VERBAL PHRASE")
            print(str(phrases[i][0][0])[0:2], ": ", str(phrases[i][0][0])[2:4])

           #ACTIVE VOICE
           #-um -, -umi -, *inuulit, mag -, ma -, mang -, nag -, pinag -
            if str(phrases[i][0][0]).__contains__("um") or str(phrases[i][0][0]).__contains__("umi") \
                    or str(phrases[i][0][0]).lower().__contains__("mag") or str(phrases[i][0][0]).lower().__contains__("ma") \
                    or str(phrases[i][0][0]).lower().__contains__("mang") or str(phrases[i][0][0]).lower().__contains__("nag") \
                    or str(phrases[i][0][0]).lower().__contains__("pinag") or str(phrases[i][0][0])[0:2].lower() == (phrases[i][0][0])[2:4].lower():
                print(phrases[i][0][0], " [:] ", phrases[i][0][1])
                print("ACTIVE VOICE")

                while j < length:

                    #PRS and PRP
                    if (str(phrases[i][j][1]).__contains__("PRS") or str(phrases[i][j][1]).__contains__("PRP")) and not str(phrases[i][j][1]).__contains__("PRSP"):
                        phrases[i].insert(0, phrases[i].pop(j))
                        print(phrases[i][j], "[PRS | PRP]", j)
                        break

                    #ang
                    elif str(phrases[i][j][0]).lower().__contains__("ang") and str(phrases[i][j][1]).__contains__("DTC"):
                        x = 0
                        print("  [ang]>", phrases[i][j][1], j)

                        while str(phrases[i][j][1]).__contains__("NN") or str(phrases[i][j][1]).__contains__("PMC") \
                                or str(phrases[i][j][0]).__contains__("at") or str(phrases[i][j][0]).__contains__("ang") \
                                or str(phrases[i][j][1]).__contains__("JJ") or str(phrases[i][j][0]).__contains__("mga") \
                                or str(phrases[i][j][0]).__contains__("na") or str(phrases[i][j][1]).__contains__("PRSP") \
                                or str(phrases[i][j][0]).__contains__("si") or str(phrases[i][j][1]).__contains__("sina"):
                            print(phrases[i][j], "[DTC | ang]", j)
                            phrases[i].insert(x, phrases[i].pop(j))

                            x += 1
                            j += 1

                            if j == length:
                                break
                        # print(phrases[i][j], "DONE", j)
                        break

                    #sina
                    elif str(phrases[i][j][0]).__contains__("sina") and  str(phrases[i][j][1]).__contains__("DTP"):
                        x = 0
                        print("  [sina]>", phrases[i][j][1], j)

                        while str(phrases[i][j][1]).__contains__("NN") or str(phrases[i][j][1]).__contains__("PMC") \
                                or str(phrases[i][j][0]).__contains__("at") or str(phrases[i][j][0]).__contains__("sina"):
                            print(phrases[i][j], "[DTP | sina]", j)
                            phrases[i].insert(x, phrases[i].pop(j))

                            x += 1
                            j +=1

                            if j == length:
                                break
                       # print(phrases[i][j], "DONE", j)
                        break

                    #si
                    elif str(phrases[i][j][1]).__contains__("DTP") and str(phrases[i][j][0]).__contains__("si"):

                        x = 0
                        print("  [si]>", phrases[i][j][1], j)

                        while str(phrases[i][j][1]).__contains__("NN") or str(phrases[i][j][1]).__contains__("PMC") \
                                or str(phrases[i][j][0]).__contains__("at") or str(phrases[i][j][0]).__contains__("si"):
                            print(phrases[i][j], "[DTP | si]", j)
                            phrases[i].insert(x, phrases[i].pop(j))
                            print(phrases[i][j], "NEXT: [DTP | si]", j)

                            x += 1
                            j += 1

                            if j == length:
                                break

                        # print(phrases[i][j], "DONE", j)
                        break

                    j += 1

            #PASSIVE VOICE
            #na -, - in, ni, i -, ma -, ka -, pag...an, ipinang, ipang -
            elif str(phrases[i][0][0]).lower().__contains__("na") or str(phrases[i][0][0]).__contains__("in") or str(phrases[i][0][0]).__contains__("ni")\
                    or str(phrases[i][0][0]).lower().__contains__("ka") or str(phrases[i][0][0]).lower().__contains__("pag") \
                    or str(phrases[i][0][0]).lower().__contains__("ipinang") or str(phrases[i][0][0]).lower().__contains__("ipang"):
                print(phrases[i][0][0], " [:] ", phrases[i][0][1])
                print("PASSIVE VOICE")

                print(phrases[i])

                while j < length:

                    #PRS and PRP
                    if (str(phrases[i][j][1]).__contains__("PRS") or str(phrases[i][j][1]).__contains__("PRP")) and not str(phrases[i][j][1]).__contains__("PRSP"):
                        phrases[i].insert(0, phrases[i].pop(j))
                        print(phrases[i][j], "[PRS | PRP]", j)
                        break

                    #ang
                    elif str(phrases[i][j][0]).__contains__("ang") and str(phrases[i][j][1]).__contains__("DTC") and str(phrases[i][0][0]).lower().__contains__("na"):
                        x = 0
                        print("  [ang]>", phrases[i][j][1], j)

                        while str(phrases[i][j][1]).__contains__("NN") or str(phrases[i][j][1]).__contains__("PMC") \
                                or str(phrases[i][j][0]).__contains__("at") or str(phrases[i][j][0]).__contains__("ang") \
                                or str(phrases[i][j][1]).__contains__("JJ") or str(phrases[i][j][0]).__contains__("mga") \
                                or str(phrases[i][j][0]).__contains__("na") or str(phrases[i][j][1]).__contains__("PRSP"):
                            print(phrases[i][j], "[DTC | ang]", j)
                            phrases[i].insert(x, phrases[i].pop(j))

                            x += 1
                            j += 1

                            if j == length:
                                break

                        # print(phrases[i][j], "DONE", j)
                        break

                    #ng
                    elif str(phrases[i][j][0]).__contains__("ng") and str(phrases[i][j][1]).__contains__("CCB"):
                        x = 0
                        print("  [ng]>", phrases[i][j][1], j)


                        while str(phrases[i][j][1]).__contains__("NN") or str(phrases[i][j][1]).__contains__("PMC") \
                                or str(phrases[i][j][0]).__contains__("at") or (str(phrases[i][j][0]).__contains__("ng") and not str(phrases[i][j][0]).__contains__("ang") )\
                                or str(phrases[i][j][1]).__contains__("JJ") or str(phrases[i][j][0]).__contains__("mga") \
                                or str(phrases[i][j][0]).__contains__("na") or str(phrases[i][j][1]).__contains__("PRSP"):
                            print(phrases[i][j], "[CCB | ng]", j)
                            phrases[i].insert(x, phrases[i].pop(j))

                            x += 1
                            j += 1

                            if j == length:
                                break

                        # print(phrases[i][j], "DONE", j)
                        break

                    #nina
                    elif str(phrases[i][j][0]).__contains__("nina") and str(phrases[i][j][1]).__contains__("DTP"):
                        x = 0
                        print("  [nina]>", phrases[i][j][1], j)

                        while str(phrases[i][j][1]).__contains__("NN") or str(phrases[i][j][1]).__contains__("PMC") \
                                or str(phrases[i][j][0]).__contains__("at")  or str(phrases[i][j][0]).__contains__("nina"):
                            print(phrases[i][j], "[DTP | nina]", j)
                            phrases[i].insert(x, phrases[i].pop(j))

                            x += 1
                            j +=1

                            if j == length:
                                break

                       # print(phrases[i][j], "DONE", j)
                        break

                    #ni
                    elif str(phrases[i][j][1]).__contains__("DTP") and str(phrases[i][j][0]).__contains__("ni"):
                        x = 0
                        print("  [ni]>", phrases[i][j][1], j)

                        while str(phrases[i][j][1]).__contains__("NN") or str(phrases[i][j][1]).__contains__("PMC") \
                                or str(phrases[i][j][0]).__contains__("at") or str(phrases[i][j][0]).__contains__("ni"):
                            print(phrases[i][j], "[DTP | ni]", j)
                            phrases[i].insert(x, phrases[i].pop(j))
                            print(phrases[i][j], "NEXT: [DTP | ni]", j)

                            x += 1
                            j += 1

                            if j == length:
                                break

                        # print(phrases[i][j], "DONE", j)
                        break

                    j += 1

        #ADJECTIVAL PHRASE
        elif str(phrases[i][0][1]).__contains__("JJ"):
            print("ADJECTIVAL PHRASE")
            while j < length:

                # PRS and PRP
                if (str(phrases[i][j][1]).__contains__("PRS") or str(phrases[i][j][1]).__contains__("PRP")) and not str(phrases[i][j][1]).__contains__("PRSP"):
                    phrases[i].insert(0, phrases[i].pop(j))
                    print(phrases[i][j], "[PRS | PRP]", j)
                    break

                # ang
                elif str(phrases[i][j][0]).__contains__("ang") and str(phrases[i][j][1]).__contains__("DTC"):
                    x = 0
                    print("  [ang]>", phrases[i][j][1], j)

                    while str(phrases[i][j][1]).__contains__("NN") or str(phrases[i][j][1]).__contains__("PMC") \
                            or str(phrases[i][j][0]).__contains__("at") or str(phrases[i][j][0]).__contains__("ang") \
                            or str(phrases[i][j][1]).__contains__("JJ") or str(phrases[i][j][0]).__contains__("mga") \
                            or str(phrases[i][j][0]).__contains__("na") or str(phrases[i][j][1]).__contains__("PRSP") \
                            or str(phrases[i][j][0]).__contains__("si"):
                        print(phrases[i][j], "[DTC | ang]", j)
                        phrases[i].insert(x, phrases[i].pop(j))

                        x += 1
                        j += 1

                        if j == length:
                            break

                    # print(phrases[i][j], "DONE", j)
                    break

                # sina
                elif str(phrases[i][j][0]).__contains__("sina") and str(phrases[i][j][1]).__contains__("DTP"):
                    x = 0
                    print("  [sina]>", phrases[i][j][1], j)

                    while str(phrases[i][j][1]).__contains__("NN") or str(phrases[i][j][1]).__contains__("PMC") \
                            or str(phrases[i][j][0]).__contains__("at") or str(phrases[i][j][0]).__contains__("sina"):
                        print(phrases[i][j], "[DTP | sina]", j)
                        phrases[i].insert(x, phrases[i].pop(j))

                        x += 1
                        j += 1

                        if j == length:
                            break

                    # print(phrases[i][j], "DONE", j)
                    break

                # si
                elif str(phrases[i][j][1]).__contains__("DTP") and str(phrases[i][j][0]).__contains__("si"):
                    x = 0
                    print("  [si]>", phrases[i][j][1], j)

                    while str(phrases[i][j][1]).__contains__("NN") or str(phrases[i][j][1]).__contains__("PMC") \
                            or str(phrases[i][j][0]).__contains__("at") or str(phrases[i][j][0]).__contains__("si"):
                        print(phrases[i][j], "[DTP | si]", j)
                        phrases[i].insert(x, phrases[i].pop(j))
                        print(phrases[i][j], "NEXT: [DTP | si]", j)

                        x += 1
                        j += 1

                        if j == length:
                            break

                    # print(phrases[i][j], "DONE", j)
                    break

                j += 1

        #NOMINAL PHRASE
        elif str(phrases[i][0][1]).__contains__("NN"):
            print("NOMINAL PHRASE")
            while j < length:

                #PRS and PRP
                if (str(phrases[i][j][1]).__contains__("PRS") or str(phrases[i][j][1]).__contains__("PRP")) and not str(phrases[i][j][1]).__contains__("PRSP"):
                    phrases[i].insert(0, phrases[i].pop(j))
                    print(phrases[i][j], "[PRS | PRP]", j)
                    break

                #ang
                elif str(phrases[i][j][0]).lower().__contains__("ang") and str(phrases[i][j][1]).__contains__("DTC"):
                    x = 0
                    print("  [ang]>", phrases[i][j][1], j)

                    while str(phrases[i][j][1]).__contains__("NN") or str(phrases[i][j][1]).__contains__("PMC") \
                            or str(phrases[i][j][0]).__contains__("at") or str(phrases[i][j][0]).__contains__("ang") \
                            or str(phrases[i][j][1]).__contains__("JJ") or str(phrases[i][j][0]).__contains__("mga") \
                            or str(phrases[i][j][0]).__contains__("na") or str(phrases[i][j][1]).__contains__("PRSP") \
                            or str(phrases[i][j][0]).__contains__("si"):
                        print(phrases[i][j], "[DTC | ang]", j)
                        phrases[i].insert(x, phrases[i].pop(j))


                        x += 1
                        j += 1


                        if j == length:
                            break

                    # print(phrases[i][j], "DONE", j)
                    break

                #sina
                elif str(phrases[i][j][0]).__contains__("sina") and  str(phrases[i][j][1]).__contains__("DTP"):
                    x = 0
                    print("  [sina]>", phrases[i][j][1], j)

                    while str(phrases[i][j][1]).__contains__("NN") or str(phrases[i][j][1]).__contains__("PMC") \
                            or str(phrases[i][j][0]).__contains__("at") or str(phrases[i][j][0]).__contains__("sina"):
                        print(phrases[i][j], "[DTP | sina]", j)
                        phrases[i].insert(x, phrases[i].pop(j))

                        x += 1
                        j +=1

                        if j == length:
                            break

                   # print(phrases[i][j], "DONE", j)
                    break

                #si
                elif str(phrases[i][j][1]).__contains__("DTP") and str(phrases[i][j][0]).__contains__("si"):
                    # phrases[i].insert(0, phrases[i].pop(j))
                    # phrases[i].insert(1, phrases[i].pop(j+1))
                    # print(phrases[i][j],"[DTP | si]", j)
                    x = 0
                    print("  [si]>", phrases[i][j][1], j)

                    while str(phrases[i][j][1]).__contains__("NN") or str(phrases[i][j][1]).__contains__("PMC") \
                            or str(phrases[i][j][0]).__contains__("at") or str(phrases[i][j][0]).__contains__("si"):
                        print(phrases[i][j], "[DTP | si]", j)
                        phrases[i].insert(x, phrases[i].pop(j))
                        print(phrases[i][j], "NEXT: [DTP | si]", j)

                        x += 1
                        j += 1

                        if j == length:
                            break

                    # print(phrases[i][j], "DONE", j)
                    break

                j += 1
        i += 1
    return phrases

#Translate
def translate(phrases1):
    # phrases1 = structure()
    fp1 = open('Translated.txt', 'a')
    print('\n\n')
    i = x = 0
    prevTag = ''
    nextTag = ''
    plural = 0

    print("START TRANSLATE")
    while i < len(phrases1):
        print('\n', phrases1[i])
        passed = 0
        jjc = 0

        while x < len(phrases1[i]):
            translated = ''
           # print(phrases1[i][x][0])
            word = phrases1[i][x][0]
            tag = phrases1[i][x][1]
            flag = 1

            if x < (len(phrases1[i]) - 1):
               nextTag = phrases1[i][x+1][1]


            #Checking 'ng'
            if str(tag).__contains__("CCB") and str(word).__contains__("ng"):
                if (str(phrases1[i][0][0]) == 'ng' or str(prevTag).__contains__('VB')) and len(phrases1[i]) != 1:
                    translated = 'the'
                elif str(phrases1[i][0][0]) == 'ng':
                    translated = 'when'
                else:
                    translated = 'of'
                flag = 0

            #Checking JJC
            elif str(tag).__contains__("JJCC"):
                jjc = 0
                with open('Eng_Fil_1.csv') as fp:
                    line = fp.readline()
                    while line:
                        temp = re.findall(r"[\w']+|[+|/ ]", line)
                        if str(temp[1]).lower() == str(phrases1[i][x+1][0]).lower() and temp[2] == 'JJR':
                            translated = ''
                            jjc = 1
                            break
                        elif not(str(temp[1]).lower() == str(phrases1[i][x+1][0]).lower() and temp[2] == 'JJR'):
                            translated = 'more'

                        line = fp.readline()
                fp.close()
                flag = 0

            # Checking 'na'
            elif str(tag).__contains__("CCP") and str(word).__contains__("na"):
                if str(prevTag).__contains__('VB') or str(prevTag).__contains__('JJ'):
                    translated = ''
                flag = 0

            #Checking Plural Form
            elif str(tag).__contains__("DTCP") or str(tag).__contains__("DTPP"):
                print('PLURAL')
                if str(word).__contains__("kina"):
                    translated = 'to'
                plural = 1
                flag = 0

            # Checking 'ang'
            elif str(tag).__contains__("DTP") or str(tag).__contains__("DTC"):
                if str(word).lower().__contains__("ang") and not str(nextTag).__contains__("PRSP"):
                    translated = 'the'

                elif str(word).__contains__("kay"):
                    translated = 'to'

                flag = 0


            #Checking LM
            elif str(tag).__contains__("LM"):
                if plural == 1:
                    translated = 'were'
                else:
                    translated = 'was'
                flag = 0

            #Checking Pronouns
            elif str(tag).__contains__("PRS") or str(tag).__contains__('PRP'):
                translated = ''
                # print('Next tag: ', nextTag)
                if str(phrases1[i][x][1]).__contains__('PRSP') and (str(nextTag).__contains__('NN') or str(nextTag).__contains__('DTCP') or str(nextTag).__contains__('JJ')):
                    tense = 'pos'
                elif (str(phrases1[i][x][1]).__contains__('PRS') or str(phrases1[i][x][1]).__contains__('PRP')) and str(prevTag).__contains__('NN'):
                    tense = 'pos'
                    translated = 'of '

                elif (str(phrases1[i][0][1]).__contains__('PRS') or str(phrases1[i][0][1]).__contains__('PRP')) and passed != 1:
                    tense = 'subj'
                    passed = 1
                else:
                    tense = 'obj'

                with open('Prounoun.csv') as fp:
                    line = fp.readline()
                    while line:
                        temp = re.findall(r"[\w']+|[+|/ ]", line)
                        if (str(temp[0]).lower() == str(word).lower()) and (tense == temp[2]):
                            translated += temp[1]
                            flag = 0
                            break
                        line = fp.readline()
                fp.close()

                flag = 0


            elif str(tag).__contains__("NNP"):
                translated = word
                flag = 0

            else:
                with open('Eng_Fil_1.csv') as fp:
                    line = fp.readline()
                    while line:
                        temp = re.findall(r"[\w']+|[+|/ ]", line)
                        if str(temp[1]).lower() == str(word).lower():

                            if str(tag).__contains__("NN") and plural == 1:

                                if temp[2] == 'NNS':
                                    translated = temp[0]
                                    plural = 0
                                    flag = 0
                                    break
                            elif str(tag).__contains__("NN"):
                                if temp[2] != 'NNS':
                                    translated = temp[0]
                                    flag = 0
                                    break

                            elif str(tag).__contains__("VB") and plural == 1:
                                if temp[2] != 'VBZ':
                                    translated = temp[0]
                                    plural = 0
                                    flag = 0
                                    break
                            elif str(tag).__contains__("VB"):
                                translated = temp[0]
                                flag = 0
                                break

                            elif str(tag).__contains__("JJ") and jjc == 1:
                                if temp[2] == 'JJR':
                                    jjc = 0
                                    translated = temp[0]
                                    flag = 0
                                    break
                            elif str(tag).__contains__("JJ"):
                                if str(temp[2]).__contains__("JJ"):
                                    translated = temp[0]
                                    flag = 0
                                    break

                            elif str(tag).__contains__("RBD"):
                                if temp[2] == 'RB':
                                    translated = temp[0]
                                    flag = 0
                                    break
                            else:
                                translated = temp[0]
                                flag = 0
                                break

                        line = fp.readline()
                fp.close()

            if flag:
                print(word, end=' ')
                fp1.write(word + ' ')

            x += 1
            print(translated, end=' ')
            fp1.write(translated + ' ')
            prevTag = phrases1[i][x - 1][1]
        i += 1
        x = 0
    fp1.close()

#Running
rules = postTagged()
fp1 = open('Translated.txt', 'w')
fp1.close()
for toStem in rules:
    sentence = stem(toStem)
    phrases = phrase(sentence)
    phrases1 = structure(phrases)
    translate(phrases1)
    print('\n')

print("\nDone")
print("GOGO")

