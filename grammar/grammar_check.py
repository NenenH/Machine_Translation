import re
import importlib
import subprocess
import nltk

spam_loader = importlib.find_loader('language_check')
found = spam_loader is not None

if not found:
    subprocess.call(['pip', 'install', 'language_check-1.1-cp36-none-any.whl'])
import language_check


def grammar_check(text_to_check, boolean_suggestion):
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(text_to_check)

    if boolean_suggestion:
        i_matches = 0
        while i_matches < len(matches):
            print(matches[i_matches])
            i_matches += 1

    corrected = language_check.correct(text_to_check, matches)
    print("original: ", text_to_check)
    print("corrected: ", corrected)
    return corrected


def open_text(file, boolen_suggestion):
    corrected = []
    open_file = open(file, "r")

    for line in open_file:

        temp = re.findall(r'([A-Z][^\.!?]*[\.!?])', line)
        i_temp = 0

        while i_temp < len(temp):
            print("sentence " + str(i_temp) + ": ")
            temp[i_temp].encode('utf-8')
            corrected += grammar_check(temp[i_temp], boolen_suggestion)
            subprocess.call(['python', 'ginger.py', temp[i_temp]])
            print("\n")
            i_temp += 1

        if temp[0] == '.':
            break

    open_file.close()
    return corrected

def top_down(text):
    nltk.parse.chart.demo(2, print_times=False, trace=1, sent=text, numparses=1)
    nltk.parse.ShiftReduceParser(grammar_check())



open_text('text_to_grammar_check.txt', True)

#open_text(yung filename, tapos kung ipriprint pa yung suggesstions)
# open_text() magrereturn ng array ng string yung nacorrect na by sentence