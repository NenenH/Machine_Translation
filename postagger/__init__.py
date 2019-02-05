# import re
# import subprocess
# subprocess.call(['java', '-cp', 'stanford-postagger.jar', 'edu.stanford.nlp.tagger.maxent.MaxentTagger', '-model',
#              'filipino-left5words-owlqn2-distsim-pref6-inf2.tagger', '-textFile', 'inputText.txt', '-outputFormat',
#              'tsv', '-outputFile', 'Postagged_words.tag'])
#
# #Read tag words
# def postTagged(n):
#     rules = []
#     i = 1
#     with open('Postagged_words.tag') as fp:
#         if n > i:
#             while True:
#                 line = fp.readline()
#                 temp = re.findall(r"[\w']+|[+|,.?]", line)
#                 if temp[0] == '.' or temp[0] == '?':
#                     break
#             i += 1
#         line = fp.readline()
#         while line:
#             temp = re.findall(r"[\w']+|[-+|,.?]", line)
#             if len(temp) > 2:
#                 temp = [temp[0] + temp[1] + temp[2], temp[3] ]
#
#             rules.append(temp)
#             if temp[0] == '.' or temp[0] == '?':
#                 fp.close()
#                 return rules
#             line = fp.readline()
#
#     fp.close()
#     return rules
import nltk

print('Start')


t = "I am groot."
print(t)
text = nltk.word_tokenize("And")
print(nltk.pos_tag(text))
