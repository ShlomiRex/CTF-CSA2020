import random
import os
import subprocess
import string as string_module
import csv

def find_most_simillar_strings(string, list):
	"""
	Returns list of items with size 4.

	Index 0: Original string.
	Index 1: Compared string.
	Index 2: Chars that are simillar.
	Index 3: Count chars that are simillar.
	"""
	unique_chars = set(string)
	result = []
	max = -1
	for word in list:
		s = set(word)
		s = s.intersection(unique_chars)
		max_num_of_simillar_chars = len(s)
		if max_num_of_simillar_chars > max:
			max = max_num_of_simillar_chars
		# Remove dup
		if max_num_of_simillar_chars == 12:
			continue
		simillar_chars = ''.join(sorted(s))
		result.append([string, word, simillar_chars, max_num_of_simillar_chars])
	return result

def find_simillar_string_1_char_diff(string: str, words: list):
	"""
	Returns 3 parameters:
	1. Simillar string.
	2. Source char that is mapped from.
	3. Destination char that is mapped to.
	"""
	simillar = find_most_simillar_strings(string, words)
	for x in simillar:
		if int(x[3]) == 11:
			source = x[0]
			simillar_string = x[1]
			simillar_chars = x[2]

			if simillar_string == string:
				continue
			src_char = None
			for c in source:
				if src_char:
					break
				for c2 in simillar_chars:
					if c != c2:
						src_char = c
						break

			dst_char = None
			for c in simillar_string:
				if dst_char:
					break
				for c2 in simillar_chars:
					if c != c2:
						dst_char = c
						break
			
			return simillar_string, src_char, dst_char
	return None, None, None

def search_simillar_1_char_diff(string: str, src_char: str, words: list):
	"""
	The source string has 'char' and the result does not have 'char' but instead diffirent mapping.
	"""
	if src_char not in string:
		return None, None, None
	simillar = find_most_simillar_strings(string, words)
	for x in simillar:
		if int(x[3]) == 11:
			source = x[0]
			simillar_string = x[1]
			simillar_chars = x[2]

			if simillar_string == string:
				continue
			if src_char in source:
				continue

			return simillar_string, simillar_chars, src_char
	return None, None, None

def get_random_word_with_simillar_string_1_char_diff(words: list):
	for x in words:
		simillar = find_simillar_string_1_char_diff(x, words)
		if simillar:
			print(simillar, " is simillar to ", x)
			return x
	return None

def get_char_mapping(source_string, dest_string):
	s1 = set(source_string)
	s2 = set(dest_string)
	s3 = s1.copy()
	s4 = s2.copy()

	for c in s1:
		if c in s2:
			s3.remove(c)
	
	for c in s2:
		if c in s1:
			s4.remove(c)

	#print("Mapping:",s3," -> ", s4)
	return [source_string, dest_string, s3, s4]

def read_words() -> list:
	"""
	Return list of words from the words.txt file.
	"""
	words = []
	file = open("words.txt") 
	word = file.readline()
	while word:
		word = word.strip()

		words.append(word)
		word = file.readline()
	return words

class GuessMachine:
	def __init__(self, guess_word_list: list, mappings: list):
		self.guesses = []
		self.last_result = -1
		self.guess_word_list = guess_word_list
		self.mappings = mappings
		self.secret_word_chars = [] #100% chars confirmed
		self.unwanted_chars = [] #100% chars not in secret word
		self.possible_chars = set(string_module.ascii_lowercase) 

		#self.char_trying = None
		self.trying_map_chars = [None,None]
	
	def get_next_guess(self) -> str:
		guess = None
		guess_amount = len(self.guesses)
		print("Guess #" + str(guess_amount))

		if guess_amount % 2 == 0:
			self.trying_map_chars[0] = self.possible_chars.pop()
			while True:
				# We want to select a string which has 1 char diffirence
				guess = random.choice(self.guess_word_list)
				if self.trying_map_chars[0] not in guess:
					continue
				string, src_char, dst_char = find_simillar_string_1_char_diff(guess, self.guess_word_list)
				if string and self.trying_map_chars[0] not in string:
					break
				# else, keep guessing a word untill found

		else:
			for c in self.possible_chars:
				string, src_char, dst_char = find_simillar_string_1_char_diff(self.guesses[0][0], self.guess_word_list)
				if c == dst_char:
					print(self.guesses[0][0], string, src_char, dst_char)
					try:
						self.trying_map_chars[0] = src_char
						self.trying_map_chars[1] = dst_char
						self.possible_chars.remove(src_char)
						self.possible_chars.remove(dst_char)
						guess = string
					except:
						pass
					break
			"""
			self.char_trying = self.possible_chars.pop()
			for x in self.guesses:
				word = x[0]
				if self.char_trying in word:
					#THE PROBLEM HERE IS THAT SRC_CHAR IS NOT EQUAL TO SELF.CHAR_TRYING. WE NEED TO FIX THIS ASAP
					simillar_string, src_char, dst_char = find_simillar_string_1_char_diff(word, self.guess_word_list)
					if simillar_string:
						guess = simillar_string
						self.trying_map_chars[0] = src_char
						self.trying_map_chars[1] = dst_char
						print("Mapping: '" + src_char + "' -> '" + dst_char +"'")
						break
		"""
		self.guesses.append([guess])
		try:
			self.guess_word_list.remove(guess) # No need to guess that word again.
		except:
			pass

		print("Guesses: " + str(self.guesses))
		return guess
	
	def __remove_words_containing_char(self, char: str):
		words_to_remove = []
		for x in self.guess_word_list:
			if char in x:
				words_to_remove.append(x)
		for x in words_to_remove:
			self.guess_word_list.remove(x)
		print("Removed " + str(len(words_to_remove)) + " words containing '" + char + "', left: " + str(len(self.guess_word_list)) + "/10000")
	
	def __remove_words_not_containing_char(self, char: str):
		words_to_remove = []
		for x in self.guess_word_list:
			if char not in x:
				words_to_remove.append(x)
		for x in words_to_remove:
			self.guess_word_list.remove(x)
		print("Removed " + str(len(words_to_remove)) + " words NOT containing '" + char + "', left: " + str(len(self.guess_word_list)) + "/10000")

	def set_last_result(self, result: int):
		"""
		Upon receiving number of characters correct from the server, this function gets called.
		"""
		src_char = self.trying_map_chars[0]
		dst_char = self.trying_map_chars[1]
		if len(self.guesses) > 1:
			print("Mapping: '{}' -> '{}'".format(src_char, dst_char))
			if result > self.last_result:
				print("Greater result, char '" + dst_char + "' is in secret word and char '" + src_char + "' is not in secret word")
				self.__remove_words_not_containing_char(dst_char)
				self.secret_word_chars.append(dst_char)

				self.__remove_words_containing_char(src_char)
				self.unwanted_chars.append(src_char)
			elif result == self.last_result:
				print("Result is same as last time")
				pass
			else:
				print("Lower result, char '" + src_char + "' is in secret word and char '" + dst_char + "' is not in secret word")
				self.__remove_words_not_containing_char(src_char)
				self.secret_word_chars.append(src_char)

				self.__remove_words_containing_char(dst_char)
				self.unwanted_chars.append(dst_char)
		self.last_result = result
		self.guesses[-1].append(result)

		print("Secret words chars: " + str(self.secret_word_chars))
		print("Chars not in secret word: " + str(self.unwanted_chars))



class Client:
	def __init__(self, guessMachine: GuessMachine):
		self.guess_machine = guessMachine
		pass

	def start(self):
		cmd = "nc tricky-guess.csa-challenge.com 2222"
		proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stdin=subprocess.PIPE, shell=True)
		
		#Skip introduction
		while True:
			line = proc.stdout.readline().decode().rstrip()
			print(line)
			if "GO !" in line:
				break

		#The loop.
		while True:
			for i in range(16):
				guess_word = self.guess_machine.get_next_guess()
				if not guess_word:
					print("Stopped running, guess word is None.")
					return

				#Write guess
				proc.stdin.write(guess_word.encode())
				proc.stdin.flush() #Very important, took me a lot of time to find the problem. Must write now instead of buffer filling. 

				#Read result
				line = proc.stdout.readline().decode().strip()
				try:
					result = int(line)
					print(str(result))
					self.guess_machine.set_last_result(result)
				except ValueError:
					# Read last line
					print("ValueError exception has occured")
					print(line)
					return


mappings = []
for row in csv.reader(open("out.csv", "r", newline=""), delimiter=','):
	mappings.append(row)

for x in mappings:
	x[1] = x[1].replace(' ', '')
	x[2] = x[2].replace(' ', '')
	x[3] = x[3].replace(' ', '')





words1 = [x[0] for x in mappings]
words2 = [x[1] for x in mappings]

words = list((set(list(words1) + list(words2))))

#words = read_words()

guessMachine = GuessMachine(words, mappings)
client = Client(guessMachine)
client.start()
print("Game has ended")
