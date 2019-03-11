import re
import shutil

class Object:
	def __init__(self):
		self.tagged_input = []
		self.temp_input = ""



	def setInput(self, filename):
		file = open(filename, "r")
		self.temp_input = file.read()
		file.close();



	def getTempInput(self):
		return self.temp_input

	def sentence_tokenize(self):
		self.temp_input = re.split(r'(?<!\w\.\w.)(?<![A-Z]\.)(?<![B][b]\.)(?<![G][n][g]\.)(?<![P][a][n][g]\.)(?<![G][a][t]\.)(?<![h][a][l]\.)(?<![G]\.)(?<![a][t][b][p])(?<=\.|\?)\s', self.temp_input)

	def word_tokenize(self):
		increment = 0
		paragraph = []
		for sentences in self.temp_input:
			sampleText = re.findall(r"[\w']+|[.,!?;-](?<![A-Z]\.)(?<![B][b]\.)(?<![G][n][g]\.)(?<![P][a][n][g]\.)(?<![G][a][t]\.)(?<![h][a][l]\.)(?<![G]\.)(?<=\.|\?)\s", sentences)
			for words in sampleText:
				if (words) == 'Bb':
					sampleText[increment] = 'Bb.'
				if (words) == 'Gng':
				    sampleText[increment] = 'Gng.'
				if (words) == 'Pang':
				    sampleText[increment] = 'Pang.'
				if (words) == 'Gat':
				    sampleText[increment] = 'Gat.'
				if (words) == 'hal':
				    sampleText[increment] = 'hal.'
				if (words) == 'G':
				    sampleText[increment] = 'G.'
				if (words) == 'A':
				    sampleText[increment] = 'A.'
				if (words) == 'B':
				    sampleText[increment] = 'B.'
				if (words) == 'C':
				    sampleText[increment] = 'C.'
				if (words) == 'D':
				    sampleText[increment] = 'D.'
				if (words) == 'E':
				    sampleText[increment] = 'E.'
				if (words) == 'F':
				    sampleText[increment] = 'F.'
				if (words) == 'H':
				    sampleText[increment] = 'H.'
				if (words) == 'I':
				    sampleText[increment] = 'I.'
				if (words) == 'J':
				    sampleText[increment] = 'J.'
				if (words) == 'K':
				    sampleText[increment] = 'K.'
				if (words) == 'L':
				    sampleText[increment] = 'L.'
				if (words) == 'M':
				    sampleText[increment] = 'M.'
				if (words) == 'N':
				    sampleText[increment] = 'N.'
				if (words) == 'O':
				    sampleText[increment] = 'O.'
				if (words) == 'P':
				    sampleText[increment] = 'P.'
				if (words) == 'Q':
				    sampleText[increment] = 'Q.'
				if (words) == 'R':
				    sampleText[increment] = 'R.'
				if (words) == 'S':
				    sampleText[increment] = 'S.'
				if (words) == 'T':
				    sampleText[increment] = 'T.'
				if (words) == 'U':
				    sampleText[increment] = 'U.'
				if (words) == 'V':
				    sampleText[increment] = 'V.'
				if (words) == 'W':
				    sampleText[increment] = 'W.'
				if (words) == 'X':
				    sampleText[increment] = 'X.'
				if (words) == 'Y':
				    sampleText[increment] = 'Y.'
				if (words) == 'Z':
					sampleText[increment] = 'Z.'
				increment=increment + 1

			sampleText.append('.')
			paragraph.append(sampleText)

		self.temp_input = paragraph
	
	def posTagger(self, lexicon):
		POS = open('POSTAG.txt', 'r')
		UND = open('list_of_new_undwords.txt', 'a')
		words = POS.readlines()
		# print(POS)
		tempList = []
		someBool = False
		for set in words:
			tags = set.split( )
			if lexicon.lower() == tags[1]:
			    tempList = [lexicon,tags[0]]
			    someBool = True
		if someBool is False:
			tempList = [lexicon, "N"]
			UND.write('UND' + lexicon + '\n')

		return(tempList)

		UND.close
		POS.close

	def getTaggedInput(self):
		return self.tagged_input

	def setTaggedInput(self, tagged_input):
		self.tagged_input = tagged_input

	def writePosTagged(self, taggedlist):
		shutil.os.remove('/Users/Lenovo/Desktop/python/Postagged_words.txt')

		fp = open('Postagged_words.txt', 'w')
		
		for words in taggedlist:
			fp.write(words[0] + ' ' + words[1] + '\n')

		fp.close()
