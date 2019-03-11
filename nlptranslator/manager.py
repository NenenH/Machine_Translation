from object import Object

class Manager:
	def __init__(self):
		self.manager_input = ""
		self.object = Object

	def init(self):
		self.manager_input = "input.txt"

	def execute(self):
		taggedlist = []
		self.object.setInput(self, "input.txt")
		self.object.sentence_tokenize(self)
		self.object.word_tokenize(self)

		print(self.object.getTempInput(self))

		for sentence in self.object.getTempInput(self):
			for word in sentence:
				taggedlist.append(self.object.posTagger(self,word))

		self.object.setTaggedInput(self, taggedlist)

		self.object.writePosTagged(self, taggedlist)