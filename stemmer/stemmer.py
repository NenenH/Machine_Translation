import re

""" 
	Affixes
"""
PREFIX_SET = [
	'nakikipag', 'Nakikipag',
        'pakikipag', 'Pakikipag',
	'pinakama', 'Pinakama',
        'pagpapa', 'Pagpapa',
	'pinagka', 'Pinagka',
        'panganga', 'Panganga', 
	'makapag', 'Makapag',
        'nakapag', 'Nakapag', 
	'tagapag', 'Tagapag',
        'makipag', 'Makipag', 
	'nakipag', 'Nakipag',
        'tigapag', 'Tigapag',
	'pakiki', 'Pakiki',
        'magpa', 'Magpa',
	'napaka', 'Napaka',
        'pinaka', 'Pinaka',
	'ipinag', 'Ipinag',
        'pagka', 'Pagka', 
	'pinag', 'Pinag',
        'mapag', 'Mapag', 
	'mapa', 'Mapa',
        'taga', 'Taga',
	'ipag', 'Ipag',
        'tiga', 'Tiga',
	'pala', 'Pala',
        'pina', 'Pina',
	'pang', 'Pang',
        'naka', 'Naka',
	'nang', 'Nang',
        'mang', 'Mang',
	'sing', 'Sing',
	'ipa', 'Ipa',
        'pam', 'Pam',
	'pan', 'Pan',
        'pag', 'Pag',
	'tag', 'Tag',
        'mai', 'Mai',
	'mag', 'Mag',
        'nam', 'Nam',
	'nag', 'Nag',
        'man', 'Man',
	'may', 'May',
        'ma', 'Ma',
	'na', 'Na',
        'ni', 'Ni',
	'pa', 'Pa',
        'ka', 'Ka',
	'um', 'Um',
        'in', 'In',
	'i', 'I',
]

INFIX_SET = [
	'um', 'in',
]


def tokenizer():
    twfile = open('outputStemmer.txt', 'w')
    print("")
    print('Start')

    with open('inputStemmer.txt', 'r') as f:

        for line in f:
            sampleText = re.findall(r"[\w']+|[.,!?;-](?<![A-Z]\.)(?<![B][b]\.)(?<![G][n][g]\.)(?<![P][a][n][g]\.)(?<![G][a][t]\.)(?<![h][a][l]\.)(?<![G]\.)(?<=\.|\?)\s", line)
            print("SPLITTED!")
            print(sampleText)

            with open('outputStemmer.txt', 'a') as wf:
                print("")

                with open('outputStemmer.txt', 'a') as wf:
                    for words in sampleText:
                        print(words)
                        wf.write(words)
                        wf.write("\n")

def check_Prefix():

    twfile = open('prefixOutput.txt', 'w')
    print("")

    print("check_Prefix")
    
    with open('outputStemmer.txt', 'r') as f:
        with open('prefixOutput.txt', 'a') as wf:
            for word in f:
                print (word)
                for prefixes in PREFIX_SET:
                    prefix = re.match("(\w+)", prefixes)
                    if prefix is not None:
                        prefixword = re.match(prefix.group(), word)
                        if prefixword is not None:
                            p = prefixword.group()
                            removed = word.replace(p, "")
                            removedWhitespaces = word.replace("\n", "")
                            print(removedWhitespaces, "-", p, "-", removed)
                            wf.write(removedWhitespaces)
                            wf.write(" - ")
                            wf.write(p)
                            wf.write(" - ")
                            wf.write(removed)
                        

def check_Infix():

    twfile = open('infixOutput.txt', 'w')
    print("")

    print("check_Infix")
    
    with open('outputStemmer.txt', 'r') as f:
        with open('infixOutput.txt', 'a') as wf:
            for word in f:
                print (word)
                first_four_letters = word[:4]
                removedFirstLetter = first_four_letters[1:]
                for infixes in INFIX_SET:
                    infix = re.match("(\w+)", infixes)
                    if infix is not None:
                        infixword = re.search(infix.group(), removedFirstLetter)
                        if infixword is not None:
                                i = infixword.group()
                                removed = word.replace(i, "")
                                removedWhitespaces = word.replace("\n", "")
                                print(removedWhitespaces, "-", i, "-", removed)
                                wf.write(removedWhitespaces)
                                wf.write(" - ")
                                wf.write(i)
                                wf.write(" - ")
                                wf.write(removed)
                            
tokenizer()
check_Prefix()
check_Infix()

