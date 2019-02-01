import subprocess

subprocess.call(['java', '-cp', 'stanford-postagger.jar', 'edu.stanford.nlp.tagger.maxent.MaxentTagger', '-model', 'filipino-left5words-owlqn2-distsim-pref6-inf2.tagger', '-textFile', 'text.txt', '-outputFormat', 'tsv', '-outputFile', 'text.tag'])
#java -cp "*" edu.stanford.nlp.tagger.maxent.MaxentTagger -model filipino-left5words-owlqn2-distsim-pref6-inf2.tagger -textFile text.txt -outputFormat tsv -outputFile text.tag
