import nltk


def postag_word(word):
    return nltk.tag.pos_tag(word)


def open_csv(file, print_, progress_bar):
    num_lines = 0
    if progress_bar:
        num_lines = sum(1 for line in open(file))
    print('start')

    open_file = open(file, 'r')
    tempword = [1]
    i = 0
    for line in open_file:

        temp = [x.strip() for x in line.split(',')]
        tempword[0] = temp[0]
        tagged_word = postag_word(tempword)
        write_postag(tagged_word)

        if progress_bar:
            printProgressBar(iteration = i, total = num_lines, prefix='Progress:', suffix='Complete', length=50)
        if print_:
            print(tempword)
            print(tagged_word[0][1])
        i += 1

    open_file.close()
    print('finished')


def write_postag(tagged_word):
    file = open('taggedenglishfromcsv.txt', 'a')
    file.write(tagged_word[0][1]+'\n')


def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
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
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='')
    # Print New Line on Complete
    if iteration == total:
        print()


open_csv('Eng_Fil_1.csv', False, True)
