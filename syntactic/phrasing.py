import re

# Read Txt file with Post Tagged Words
import subprocess
subprocess.call(['java', '-cp', 'stanford-postagger.jar', 'edu.stanford.nlp.tagger.maxent.MaxentTagger', '-model',
             'filipino-left5words-owlqn2-distsim-pref6-inf2.tagger', '-textFile', 'InputText.txt', '-outputFormat',
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
            rules.append(temp)
            if temp[0] == '.' or temp[0] == '?':
                fp.close()
                return rules
            line = fp.readline()

    fp.close()
    return rules

#Stemmer
def stem():
    toStem = (postTagged(1))
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

#Return phrases
def phrase():
    sentence = stem()
    phrase = []
    phraseList = []
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
        elif str(sentence[x][1]).__contains__("RB") and x ==0:
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
        elif str(sentence[x][1]).__contains__("DT") and x == 0:
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
                print("Current Word [VB]: ", sentence[x])
                if (str(sentence[x][1]).__contains__("CC") or str(sentence[x][1]).__contains__("RBW")) and str(sentence[x + 1][1]).__contains__("VB"):
                    break

                if str(sentence[x][1]).__contains__("JJ") and not (str(sentence[x-1][1]).__contains__("DT")
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
def structure():
    i = 0

    phrases = phrase()

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
                        # phrases[i].insert(0, ['was', 'VBTS'])
                        # length += 1
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
                        # phrases[i].insert(0, phrases[i].pop(j))
                        # phrases[i].insert(1, phrases[i].pop(j+1))
                        # print(phrases[i][j],"[DTP | si]", j)
                        # break
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
                            or str(phrases[i][j][0]).__contains__("na") or str(phrases[i][j][1]).__contains__("PRSP"):
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
                    # phrases[i].insert(0, phrases[i].pop(j))
                    # phrases[i].insert(1, phrases[i].pop(j + 1))
                    #
                    # print(phrases[i][j], "[DTP | si]", j)
                    # break
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
                            or str(phrases[i][j][0]).__contains__("na") or str(phrases[i][j][1]).__contains__("PRSP"):
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
def translate():
    phrases1 = structure()
    print('\n\n')
    i = x = 0
    prevTag = ''
    nextTag = ''
    plural = 0

    print("START TRANSLATE")
    while i < len(phrases1):
       # print('\n', phrases1[i])
        passed = 0

        while x < len(phrases1[i]):
            translated = ''
           # print(phrases1[i][x][0])
            word = phrases1[i][x][0]
            tag = phrases1[i][x][1]
            flag = 1

            if x < (len(phrases1[i]) - 1):
               nextTag = phrases1[i][x+1][1]

            #Checking 'ang'
            if str(tag).__contains__("DTP"):
                if str(word).__contains__("ang"):
                    translated = 'the'
                flag = 0

            #Checking 'ng'
            elif str(tag).__contains__("CCB") and str(word).__contains__("ng"):
                if (str(phrases1[i][0][0]) == 'ng' or str(prevTag).__contains__('VB')) and len(phrases1[i]) != 1:
                    translated = 'the'
                elif str(phrases1[i][0][0]) == 'ng':
                    translated = 'when'
                else:
                    translated = 'of'
                flag = 0

            # Checking 'na'
            elif str(tag).__contains__("CCP") and str(word).__contains__("na"):
                if str(prevTag).__contains__('VB') or str(prevTag).__contains__('JJ') :
                    translated = ''
                flag = 0

            #Checking Plural Form
            elif str(tag).__contains__("DTCP"):
               plural = 1
               flag = 0

            #Checking Pronouns
            elif str(tag).__contains__("PRS") or str(tag).__contains__('PRP'):
                if str(phrases1[i][x][1]).__contains__('PRSP') and (str(nextTag).__contains__('NN') or str(nextTag).__contains__('DTCP')):
                    tense = 'pos'
                elif (str(phrases1[i][x][1]).__contains__('PRS') or str(phrases1[i][x][1]).__contains__('PRP')) and str(prevTag).__contains__('NN'):
                    tense = 'pos'
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
                            translated = temp[1]
                            flag = 0
                            break
                        line = fp.readline()
                fp.close()
                flag = 0

            elif str(tag).__contains__("NNP"):
                translated = word
                flag = 0

            else:
                #if Plural Form
                if str(tag).__contains__("NN") and plural == 1:
                    with open('Plural.csv') as fp:
                        line = fp.readline()
                        while line:
                            temp = re.findall(r"[\w']+|[+|/ ]", line)
                            if str(temp[1]).lower() == str(word).lower():
                                translated = temp[0]
                                flag = 0
                                break
                            line = fp.readline()
                    fp.close()
                    plural = 0

                else:
                    with open('Eng_Fil_1.csv') as fp:
                        line = fp.readline()
                        while line:
                            temp = re.findall(r"[\w']+|[+|/ ]", line)
                            if str(temp[1]).lower() == str(word).lower():
                                translated = temp[0]
                                flag = 0
                                break
                            line = fp.readline()
                    fp.close()

            if flag:
                print(word , end=' ')
            x += 1
            print(translated, end=' ')
            prevTag = phrases1[i][x - 1][1]
        i += 1
        x= 0

#Running
translate()
print("\nDone")

