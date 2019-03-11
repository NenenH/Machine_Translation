import re
from nltk import Nonterminal, nonterminals, Production, CFG
from nltk.parse.generate import generate, demo_grammar
from nltk.parse import RecursiveDescentParser
from nltk.parse import ShiftReduceParser
import nltk

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
            #debugprint(temp)
            if len(temp) > 2:
                if temp[0] == '`' or temp[1] == 'PMS':
                    temp = ["''", 'PMS']
                else:
                    temp = [temp[0] + temp[1] + temp[2], temp[3]]

            if temp != []:
                #debugprint(temp)
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
            #debugprint(toStem[x][1])
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
                        #debugprint(toStem[x][0])
                        flag = 0
                        break
                    line = fp.readline()
            fp.close()

            if flag == 1:
                toStem[x][0] = word[0:leng1 - 2]

            #debugprint("Stem: ", toStem[x][0])


        x += 1

    return toStem

def rootWord(toRoot):
    verbUnlapi =['nakipag', 'nakikipag,' 'magpapa', 'magpa', 'mapagma', 'magkasing', 'mapang', 'kaka', 'kapapa','ka', 'nakapag', 'pinag', 'pina', 'mag', 'mai',  'makapag',  'mang',  'man',  'mapa'  'ma',   'nag',  'nang',  'nam', 'nai',  'na', 'pinag', 'ipinang', 'ni', 'i', 'tagapag','taga', 'tiga']
    adjUnlapi = ['kasing', 'magsing', 'sing', 'pinaka', 'mapang', 'mapam', 'ma', 'pang', 'pan', 'pala']
    nounUnlapi = ['tagapag', 'tigapag',  'taga',  'tiga',  'pakikipag',  'pag', 'man']
    #debugprint(toRoot)

    for toRoot in toRoot:
        if str(toRoot[1]).__contains__("VB"):
            #unlapi
            for vp in verbUnlapi:
                if vp == str(toRoot[0])[0:len(vp)].lower():
                    #debugprint("->", vp)
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

            #debugprint(toRoot[0])

        elif str(toRoot[1]).__contains__("JJ") or str(toRoot[1]).__contains__("RBD"):
            for adj in adjUnlapi:
                if adj == str(toRoot[0])[0:len(adj)].lower():
                    #debugprint("->", adj)
                    toRoot[0] = (toRoot[0])[len(adj): len(toRoot[0])]
                    #debugprint(toRoot[0])
                    break

        elif str(toRoot[1]).__contains__("NNC"):
            for nn in nounUnlapi:
                if nn == str(toRoot[0])[0:len(nn)].lower():
                    #debugprint("->", nn)
                    toRoot[0] = (toRoot[0])[len(nn): len(toRoot[0])]
                    #debugprint(toRoot[0])
                    break
    return toRoot

#Return phrases
def phrase(sentence):
    phrase = []
    phraseList = []
    cc = ['samantala', 'ngunit', 'bagkus', 'kundi', 'imbes', 'kahit', 'maliban', 'bilang', 'bagamat', 'datapwat', 'samantala', 'habang', 'kasi', 'dahil', 'kung', 'sapagkat', 'dahilan', 'palibhasa', 'upang', 'gayundin', 'basta\'t']
    #debugprint(sentence)
    x = 0
    while x < len(sentence):
        #debugprint("Current: ", sentence[x])

        #phrase start with Conjunction
        if str(sentence[x][1]).__contains__("CC") and not (
                str(sentence[x][1]).__contains__("JJ") or str(sentence[x][1]).__contains__("PRSP")
                or str(sentence[x][1]).__contains__("NN")):
            #debugprint("Current Word [CC]: ", sentence[x])
            while not (str(sentence[x][1]).__contains__("VB") or str(sentence[x][1]).__contains__("PMP") or str(
                    sentence[x][1]).__contains__("PMQ") or str(sentence[x][1]).__contains__("JJ")):
                #debugprint("Current Word [CC]: ", sentence[x])
                phrase.append(sentence[x])
                x += 1
            phraseList.append(phrase)
            phrase = []
            #debugprint(phraseList)
            x -= 1

        # phrase start with Adverb
        elif str(sentence[x][1]).__contains__("RB"):
            #debugprint("Current Word [RB]: ", sentence[x])
            while not (str(sentence[x][1]).__contains__("VB") or str(sentence[x][1]).__contains__("PMP") or str(sentence[x][1]).__contains__("PMQ")):
                #debugprint("Current Word [RB]: ", sentence[x])
                phrase.append(sentence[x])
                x += 1
            phraseList.append(phrase)
            phrase = []
            #debugprint(phraseList)
            x -= 1

        # phrase start with Noun
        elif str(sentence[x][1]).__contains__("NN") and x == 0:
            #debugprint("Current Word [NN]: ", sentence[x])
            while not (str(sentence[x][1]).__contains__("VB") or str(sentence[x][1]).__contains__("PMP") or str(
                    sentence[x][1]).__contains__("PMQ")):
                #debugprint("Current Word [NN]: ", sentence[x])
                phrase.append(sentence[x])
                x += 1
            phraseList.append(phrase)
            phrase = []
            #debugprint(phraseList)
            x -= 1

        # phrase start with Pronoun
        elif str(sentence[x][1]).__contains__("PR") and x == 0:
            #debugprint("Current Word [PR]: ", sentence[x])
            phrase.append(sentence[x])
            phraseList.append(phrase)
            phrase = []

        # phrase start with RBW
        elif str(sentence[x][1]).__contains__("RBW"):
            #debugprint("Current Word [RBW]: ", sentence[x])
            phrase.append(sentence[x])
            phraseList.append(phrase)
            phrase = []

        # phrase start with LM
        elif str(sentence[x][1]).__contains__("LM") and not str(sentence[x+1][1]).__contains__("VB"):
            #debugprint("Current Word [LM]: ", sentence[x])
            phrase.append(sentence[x])
            phraseList.append(phrase)
            phrase = []

        # phrase start with Determiner
        elif str(sentence[x][1]).__contains__("DT"):
            while not (str(sentence[x][1]).__contains__("VB") or str(sentence[x][1]).__contains__("PMP") or str(sentence[x][1]).__contains__("PMQ")):
                #debugprint("Current Word [DT]: ", sentence[x])
                phrase.append(sentence[x])
                x += 1
            phraseList.append(phrase)
            phrase = []
            #debugprint(phraseList)
            x -= 1


        # phrase start with Adjective
        elif str(sentence[x][1]).__contains__("JJ"):
            while not (str(sentence[x][1]).__contains__("VB") or str(sentence[x][1]).__contains__("PMP") or str(sentence[x][1]).__contains__("PMQ")):
                #debugprint("Current Word [JJ]: ", sentence[x])
                phrase.append(sentence[x])
                x += 1
            phraseList.append(phrase)
            phrase = []
            #debugprint(phraseList)
            x -= 1

        # phrase start with Verb
        elif str(sentence[x][1]).__contains__("VB"):
            #debugprint(sentence[x])
            while not (str(sentence[x][1]).__contains__("PMP") or str(sentence[x][1]).__contains__("PMQ")):
                go = 0
                #debugprint("Current Word [VB]: ", sentence[x])
                if (str(sentence[x][1]).__contains__("CC") or str(sentence[x][1]).__contains__("RBW")) and str(sentence[x + 1][1]).__contains__("VB"):
                    #debugprint('Dito pumasok')
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
            #debugprint(phraseList)
            x -= 1

        x += 1
    phrase = []
    phrase.append(sentence[len(sentence) -1])
    phraseList.append(phrase)
    return phraseList

def parse_word_tag(word, tag, sentence):
    rule_perphrase_c = """S ->  DP | PP | AP | VP | CP | ADVP
            DP -> Dprime | Dprime QP | Dprime AP  | Dprime CP 
            Dprime -> D | NP | D NP  | D CP 
            NP -> Nprime | Nprime DP | Nprime PP | Nprime AP | Nprime VP | Nprime CP | Nprime ADVP 
            Nprime -> N | N PP | PP N | N QP
            PP -> Pprime | Pprime ADVP | Pprime VP
            Pprime -> P | P DP
            AP -> Aprime | Aprime ADVP | Aprime AP | Aprime CP
            Aprime -> A | A DP 
            VP -> Vprime | Vprime ADVP | Vprime DP | Vprime CP 
            Vprime -> V | V DP | V PRN 
            CP -> Cprime | Cprime VP | Cprime DP | Cprime NP | Cprime AP | Cprime QP | Cprime ADVP
            Cprime -> C | C Cprime
            QP ->  Qprime | Qprime CP
            Qprime -> Q | Q NP
            ADVP -> ADVprime | ADVprime QP | ADVprime DP  | ADVprime AP | ADVprime CP | ADVprime VP
            ADVprime -> ADV | ADV ADVP""" + '\n'

    rule_perphrase_b = """S ->  DP | PP | AP | VP | CP | ADV
            DP -> Dprime | Dprime QP | Dprime AP  | Dprime CP 
            Dprime -> D | D NP | NP | D CP
            NP -> Nprime | Nprime DP | Nprime PP | Nprime AP | Nprime VP | Nprime CP 
            Nprime -> N | N PP | PP N 
            PP -> Pprime | Pprime ADV | Pprime VP
            Pprime -> P | P DP
            AP -> Aprime | Aprime ADV | Aprime AP | Aprime CP
            Aprime -> A | A DP 
            VP -> Vprime | Vprime ADV| Vprime DP | Vprime CP 
            Vprime -> V | V DP | V PRN 
            CP -> Cprime | Cprime VP | Cprime DP | Cprime NP | Cprime QP | Cprime ADV
            Cprime -> C 
            QP ->  Qprime | Qprime CP
            Qprime -> Q""" + '\n'

    rule_perphrase_a = """S ->  DP | PP | AP | VP | CP | ADV
        DP -> Dprime | Dprime QP | Dprime AP  | Dprime CP 
        Dprime -> D NP | NP | D CP
        NP -> Nprime | Nprime DP | Nprime PP | Nprime AP | Nprime VP | Nprime CP 
        Nprime -> N | N PP | PP N 
        PP -> Pprime | Pprime ADV | Pprime VP
        Pprime -> P | P DP
        AP -> Aprime | Aprime ADV
        Aprime -> A | A DP
        VP -> Vprime | Vprime ADV | Vprime DP 
        Vprime -> V | V DP | V PRN | Vprime CP 
        CP -> Cprime | Cprime VP | Cprime DP | Cprime NP | Cprime QP
        Cprime -> C """ + '\n'

    rule_test_c = """S ->  DP Period | VP Period
    DP -> Dprime | Dprime QP | Dprime AP  | Dprime CP 
    Dprime -> D NP | NP | D CP
    NP -> Nprime | Nprime DP | Nprime PP | Nprime AP | Nprime VP | Nprime CP
    Nprime -> N | N PP | PP N 
    PP -> Pprime | Pprime ADV | Pprime VP
    Pprime -> P | P DP
    AP -> Aprime | Aprime ADV
    Aprime -> A | A DP
    VP -> Vprime | Vprime ADV | Vprime DP
    Vprime -> V | V DP | V PRN | Vprime CP 
    CP -> Cprime | Cprime VP | Cprime DP | Cprime NP
    Cprime -> C """ + '\n'


    rule_test = """S ->  DP Period | VP Period
    DP -> Dprime | Dprime QP | Dprime AP 
    Dprime -> D NP | NP
    NP -> Nprime | Nprime DP | Nprime PP | Nprime AP | Nprime VP 
    Nprime -> N | N PP | PP N | N CP PP | PP CP N 
    PP -> Pprime | Pprime ADV | Pprime VP
    Pprime -> P | P DP
    AP -> Aprime | Aprime ADV
    Aprime -> A | A DP
    VP -> Vprime | Vprime ADV | Vprime DP
    Vprime -> V | V DP | V PRN | Vprime CP 
    CP -> Cprime | Cprime VP
    Cprime -> C | C VP | C NP """ + '\n'

    rule_test_b = """S -> DP VP 
    DP ->  Dprime QP | Dprime AP   
    Dprime -> D NP
    PP ->   Pprime ADV | Pprime VP 
    Pprime -> P DP
    AP -> Aprime ADV
    Aprime -> A DP
    VP ->  Vprime ADV | Vprime DP 
    Vprime -> V DP | V PRN | V CP 
    NP ->  Nprime DP | Nprime PP | Nprime AP | Nprime VP 
    Nprime -> N PP | PP N 
    CP -> Cprime VP 
    Cprime -> C VP | C NP """ + '\n'

    rule_abc = """S ->  DP Period 
    DP -> Dprime QP | Dprime AP 
    Dprime -> D NP
    NP -> Nprime DP | Nprime PP | Nprime AP | Nprime VP 
    Nprime -> N PP | PP N | N CP PP | PP CP N 
    PP -> Pprime ADV | Pprime VP
    Pprime -> P DP
    AP -> Aprime ADV
    Aprime -> A DP
    VP -> Vprime ADV | Vprime DP
    Vprime -> V DP | V PRN | Vprime CP 
    CP -> Cprime VP
    Cprime -> C VP | C NP """ + '\n'

    rule_test_b = """S -> DP VP 
    DP ->  Dprime QP | Dprime AP   
    Dprime -> D NP
    PP ->   Pprime ADV | Pprime VP 
    Pprime -> P DP
    AP -> Aprime ADV
    Aprime -> A DP
    VP ->  Vprime ADV | Vprime DP 
    Vprime -> V DP | V PRN | V CP 
    NP ->  Nprime DP | Nprime PP | Nprime AP | Nprime VP 
    Nprime -> N PP | PP N 
    CP -> Cprime VP 
    Cprime -> C VP | C NP """ + '\n'



    rule = """S ->  NP VP Sym | VP NP Sym |  VP Comma NP | NP Comma VP
    DP -> Dprime QP | Dprime AP 
    Dprime -> D NP
    PP -> Pprime ADV | Pprime TP
    Pprime -> P DP
    AP -> Aprime ADV
    Aprime -> A DP
    VP -> Vprime ADV | Vprime DP
    Vprime -> V DP | V PRN | Vprime CP | V comma DP | V comma PRN | comma Vprime CP
    NP -> Nprime DP | Nprime PP | Nprime AP | Nprime VP 
    Nprime -> N PP | PP N | N Comma PP | PP Comma N | N CP PP | PP CP N 
    TP -> Tprime DP | Tprime Q
    Tprime -> Tum VP | Tin VP
    Tprime -> Tma AP
    Tprime -> Tna- PP
    Tprime -> Tmay VP
    Tprime -> Ttaga VP
    CP -> Cprime TP
    Cprime -> C TP | C NP | comma C TP | comma C NP""" + '\n'

    rule_backup = """S ->  NP VP | VP NP
    DP -> Dprime QP | Dprime AP 
    Dprime -> D NP
    PP -> Pprime ADV | Pprime TP
    Pprime -> P DP
    AP -> Aprime ADV
    Aprime -> A DP
    VP -> Vprime ADV | Vprime DP
    Vprime -> V DP | V PRN | Vprime CP 
    NP -> Nprime DP | Nprime PP | Nprime AP | Nprime VP 
    Nprime -> N PP | PP N | N CP PP | PP CP N 
    TP -> Tprime DP | Tprime Q
    Tprime -> Tum VP | Tin VP
    Tprime -> Tma AP
    Tprime -> Tna- PP
    Tprime -> Tmay VP
    Tprime -> Ttaga VP
    CP -> Cprime TP
    Cprime -> C TP | C NP """ + '\n'

    i_tag = 0
    tag_rule = []
    sentence_word_tag = ''
    #print('tag length: ', len(tag))
    while i_tag < len(tag):
        if "NN" in tag[i_tag]:
            tag_rule.append('N')
        elif "PR" in tag[i_tag]:
            tag_rule.append('N')
        elif "DT" in tag[i_tag]:
            tag_rule.append('D')
        elif "LM" in tag[i_tag]:
            tag_rule.append('C')
        elif "CCU" in tag[i_tag]:
            tag_rule.append('P')
        elif "CC" in tag[i_tag]:
            tag_rule.append('C')
        elif "VB" in tag[i_tag]:
            tag_rule.append('V')
        elif "JJ" in tag[i_tag]:
            tag_rule.append('A')
        elif "RB" in tag[i_tag]:
            tag_rule.append('ADV')
        elif "CD" in tag[i_tag]:
            tag_rule.append('Q')
        elif "TS" in tag[i_tag]:
            tag_rule.append('D')
        elif "FW" in tag[i_tag]:
            tag_rule.append('N')
        elif "PMP" in tag[i_tag]:
            tag_rule.append('Period')
        elif "PMC" in tag[i_tag]:
            tag_rule.append('C')
        elif "PM" in tag[i_tag]:
            tag_rule.append('Sym')

        i_word = 0
        word_repeated = False
        while i_word < i_tag:
            if word[i_tag] == word[i_word]:
                word_repeated = True
            i_word += 1
        #print('i_tag: ', i_tag)
        if not word_repeated:
            sentence_word_tag += tag_rule[i_tag] + " -> " + "'" + word[i_tag] + "'" + '\n'
        i_tag += 1

    # DP = D' + QP | D' + AP
    # D' = D + NP
    #
    # PP = P' + ADV | P' + TP
    # P' = P + DP
    #
    # AP = A' + ADV
    # A' = A + DP
    #
    # VP = V' + ADV | V' + DP
    # V' = V + DP ¦ V + PRN ¦ V' + CP
    #
    # NP = N' + attribute phrase
    # N' = N + PP

    sentence_split = sentence.split()
    grammar = CFG.fromstring(rule_perphrase_c + sentence_word_tag)

    # #test uncomment to test english structure
    # grammar = CFG.fromstring("""
    # S -> NP VP
    # PP -> P NP
    # NP -> 'the' N | N PP | 'the' N PP
    # VP -> V NP | V PP | V NP PP
    # N -> 'cat'
    # N -> 'dog'
    # N -> 'rug'
    # V -> 'chased'
    # V -> 'sat'
    # P -> 'in'
    # P -> 'on'""")
    # sentence_split = 'the cat chased the dog on the rug'.split()

    rd = RecursiveDescentParser(grammar)
    sr = ShiftReduceParser(grammar)
    chart_parser = nltk.ChartParser(grammar)


    earley_chart_parser = nltk.EarleyChartParser(grammar)

    chart_parser = earley_chart_parser
    print(tag_rule)
    parse_tree = []
    print('Parse')
    for tree in chart_parser.parse(sentence_split):
        parse_tree.append(tree)

    if len(parse_tree) > 0:
        print(parse_tree[0])
    else:
        print('NO TREE')

    # print('EarleyChartParser')
    # for tree in earley_chart_parser.parse(sentence_split):
    #     print(tree)

    # nltk.parse.chart.demo(1, print_times=False, trace=1,sent = sentence, numparses = 1)

    # print('sr')
    # for t in sr.parse(sentence_split):
    #     print(t)



    # print('rd')
    # for t in rd.parse(sentence_split):
    #     print(t)

    # print('generate sentence from grammar')
    # for sentence in generate(grammar, n=10):
    #     print(' '.join(sentence))

    # print('rd')
    # for t in rd.parse(sentence_split):
    #     print(t)

def get_sentence(sentence_, letter):

    word = []
    tag = []
    sentence = ''
    i_line = 0
    for word_tag in sentence_:
        word.append(word_tag[0])
        tag.append(word_tag[1])

        sentence += word_tag[0] + ' '

        i_line += 1

    #debugprint('| \t '.join(map(str, word)))
    #debugprintprint('| \t '.join(map(str, tag)))
    if not sentence == '. ':
        print('\n')
        print(letter)
        print("parse")
        print('sentence: ' + sentence)
        print('tag: ')
        print(tag)
        print('word: ')
        print(word)
        parse_word_tag(word, tag, sentence)



#Running
rules = postTagged()
fp1 = open('Translated.txt', 'w')
fp1.close()
count = 1

for toStem in rules:
    letter = chr(ord('A') - 1)
    temp_sentence = toStem
    sentence = stem(toStem)
    phrases = phrase(sentence)


    # for ph in phrases:
    #     print(ph)
    #     print('\n')

    #debugprint('sentence: ')
    #debugprint(sentence)
    #debugprint('phrases: ')
    #debugprint(phrases)
    print(count)
    print('phrases : ')
    # print(phrases)
    print('| \t '.join(map(str, phrases)))

    for ph in phrases:
        letter = chr(ord(letter) + 1)
        get_sentence(ph, letter)
    print('\n')
    count += 1


print("\nDone")
print("GOGO")

