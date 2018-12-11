import re
from nltk.corpus import wordnet
import csv
import yaml  # pip install pyyaml

# import enchant
# from nltk.metrics import edit_distance


replacement_patterns = [
	(r'won\'t', 'will not'),
	(r'can\'t', 'cannot'),
	(r'i\'m', 'i am'),
	(r'ain\'t', 'is not'),
	(r'(\w+)\'ll', '\g<1> will'),
	(r'(\w+)n\'t', '\g<1> not'),
	(r'(\w+)\'ve', '\g<1> have'),
	(r'(\w+)\'s', '\g<1> is'),
	(r'(\w+)\'re', '\g<1> are'),
	(r'(\w+)\'d', '\g<1> would')
]


class RegexpReplacer(object):
	""" Replaces regular expression in a text.
	replacer = RegexpReplacer()
	replacer.replace("can't is a contraction")  # 'cannot is a contraction'
	replacer.replace("I should've done that thing I didn't do")
	# 'I should have done that thing I did not do'
	"""

	def __init__(self, patterns=replacement_patterns):
		self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]

	def replace(self, text):
		s = text

		for (pattern, repl) in self.patterns:
			s = re.sub(pattern, repl, s)

		return s


####################################
#  Replacing Repeating Characters  #
####################################

class RepeatReplacer(object):
	""" Removes repeating characters until a valid word is found.
	replacer = RepeatReplacer()
	replacer.replace('looooove') # 'love'
	replacer.replace('oooooh')   # 'ooh'
	replacer.replace('goose')    # 'goose'
	"""

	def __init__(self):
		self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
		self.repl = r'\1\2\3'

	def replace(self, word):
		if wordnet.synsets(word):
			return word

		repl_word = self.repeat_regexp.sub(self.repl, word)

		if repl_word != word:
			return self.replace(repl_word)
		else:
			return repl_word


#####################################
# Spelling Correction with Enchant  #
#####################################

# class SpellingReplacer(object):
# 	""" Replaces misspelled words with a likely suggestion based on shortest
# 	edit distance.
# 	>>> replacer = SpellingReplacer()
# 	>>> replacer.replace('cookbok')
# 	'cookbook'
# 	"""
#
# 	def __init__(self, dict_name='en', max_dist=2):
# 		self.spell_dict = enchant.Dict(dict_name)
# 		self.max_dist = max_dist
#
# 	def replace(self, word):
# 		if self.spell_dict.check(word):
# 			return word
#
# 		suggestions = self.spell_dict.suggest(word)
#
# 		if suggestions and edit_distance(word, suggestions[0]) <= self.max_dist:
# 			return suggestions[0]
# 		else:
# 			return word
########################
## Replacing Synonyms ##
########################

class WordReplacer(object):
	""" WordReplacer that replaces a given word with a word from the word_map,
	or if the word isn't found, returns the word as is.
	# replacer = WordReplacer({'bday': 'birthday'})
	# replacer.replace('bday')  # 'birthday'
	"""

	def __init__(self, word_map):
		self.word_map = word_map

	def replace(self, word):
		return self.word_map.get(word, word)


class CsvWordReplacer(WordReplacer):
	""" WordReplacer that reads word mappings from a csv file.
	replacer = CsvWordReplacer('synonyms.csv')
	replacer.replace('bday')  # 'birthday'
	"""

	def __init__(self, fname):
		word_map = {}

		for line in csv.reader(open(fname)):
			word, syn = line
			word_map[word] = syn

		super(CsvWordReplacer, self).__init__(word_map)


class YamlWordReplacer(WordReplacer):
	""" WordReplacer that reads word mappings from a yaml file.
	replacer = YamlWordReplacer('synonyms.yaml')
	replacer.replace('bday')  #  'birthday'
	"""

	def __init__(self, fname):
		word_map = yaml.load(open(fname))
		super(YamlWordReplacer, self).__init__(word_map)


# rep = RegexpReplacer()
# print(rep.replace("can't is a contradicton"))
# rep = RepeatReplacer()
# print(rep.replace("ohhhh you coooome on man"))
# replacer = WordReplacer({'bday': 'birthday'})
# print(replacer.replace('bday'))
# replacer = CsvWordReplacer('synonyms.csv')
# print(replacer.replace('bday'))