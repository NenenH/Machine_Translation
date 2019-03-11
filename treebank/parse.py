from nltk import Nonterminal, nonterminals, Production, CFG
from nltk.parse.generate import generate, demo_grammar
from nltk.parse import RecursiveDescentParser
from nltk.parse import ShiftReduceParser
import nltk


def parse_word_tag(word, tag, sentence):
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
    print('tag length: ', len(tag))
    while i_tag < len(tag):
        if "NN" in tag[i_tag]:
            tag_rule.append('N')
        elif "PR" in tag[i_tag]:
            tag_rule.append('N')
        elif "DT" in tag[i_tag]:
            tag_rule.append('D')
        elif "LM" in tag[i_tag]:
            tag_rule.append('D')
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
            tag_rule.append('QP')
        elif "TS" in tag[i_tag]:
            tag_rule.append('D')
        elif "FW" in tag[i_tag]:
            tag_rule.append('D')
        elif "PMP" in tag[i_tag]:
            tag_rule.append('Period')
        elif "PMC" in tag[i_tag]:
            tag_rule.append('Comma')
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
    grammar = CFG.fromstring(rule_test_c + sentence_word_tag)

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

    parse_tree = []
    print('ChartParser')
    for tree in chart_parser.parse(sentence_split):
        parse_tree.append(tree)

    print(parse_tree[0])

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


def open_word_tag(file, progress_bar):
    num_line = 0
    if progress_bar:
        num_line = sum(1 for line in open(file)) - 1
    print('open_text')

    open_file = open(file, 'r')
    word = []
    tag = []
    sentence = ''
    i_line = 0
    for line in open_file:
        temp = [x.strip() for x in line.split('\t')]

        i_temp = 0
        word_temp = ''
        while i_temp < len(temp) - 1:
            word_temp += temp[i_temp]
            i_temp += 1
        sentence += word_temp + ' '
        if not not word_temp:
            word.append(word_temp)
            tag.append(temp[len(temp) - 1])

        over = str(i_line) + ' / ' + str(num_line)

        if progress_bar:
            print_progress_bar(iteration=i_line, total=num_line, prefix='Progress:', suffix=over, length=50)
        i_line += 1

    print('| \t '.join(map(str, word)))
    print('| \t '.join(map(str, tag)))
    print("parse")
    parse_word_tag(word, tag, sentence)


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='')
    # Print New Line on Complete
    if iteration == total:
        print()


open_word_tag('textB.tag', progress_bar=True)
