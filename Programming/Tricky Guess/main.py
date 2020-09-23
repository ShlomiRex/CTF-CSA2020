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
		self.undecided_chars = [] #Not sure what chars are

		#self.char_trying = None
		self.current_mapping = [None,None,None,None]
	
	def get_next_guess(self) -> str:
		guess = None
		guess_amount = len(self.guesses)
		print("Guess #" + str(guess_amount+1))

		if guess_amount == 15:
			print("\n\nFinal guess")
			print("Words: ", len(self.guess_word_list))
			for word in self.guess_word_list:
				# Check word has all the chars we need
				has_all_chars = True
				for secret_char in self.secret_word_chars:
					if secret_char not in word:
						has_all_chars = False
						break
				if has_all_chars:
					print("Word: ", word, " has all the secret chars")
					print("Secret chars: ", self.secret_word_chars)

					has_unwanted_char = False
					for unwanted_char in self.unwanted_chars:
						if unwanted_char in word:
							has_unwanted_char = True
							print("Word: ", word, " has unwanted char: ", unwanted_char)
							break
					
					if has_unwanted_char:
						continue
					guess = word
					break
					


		if guess_amount % 2 == 0:
			for c in self.possible_chars:
				mapping =  random.choice(self.mappings)
				src_char = mapping[2]
				dst_char = mapping[3]

				if c == src_char or c == dst_char:
					# Skip same mapping already tried
					if src_char in self.undecided_chars and dst_char in self.undecided_chars:
						continue
					if src_char in self.unwanted_chars or dst_char in self.unwanted_chars:
						print("src_char or dst_char in unwanted_chars: ", src_char, dst_char, self.unwanted_chars)
						continue
					self.current_mapping = mapping
					print("Mapping: ", self.current_mapping)
					break
			guess = mapping[0]

		else:
			guess = self.current_mapping[1]
		self.guesses.append([guess])

		print("Guesses: " + str(self.guesses))
		return guess
	
	def set_last_result(self, result: int):
		"""
		Upon receiving number of characters correct from the server, this function gets called.
		"""
		src_char = self.current_mapping[2]
		dst_char = self.current_mapping[3]

		if len(self.guesses) > 1:
			print("Mapping: ", self.current_mapping)
			if result > self.last_result:
				print("Greater result, char '" + dst_char + "' is in secret word and char '" + src_char + "' is not in secret word")
				self.secret_word_chars.append(dst_char)
				self.unwanted_chars.append(src_char)

				try:
					self.undecided_chars.remove(src_char)
				except:
					pass

				try:
					self.undecided_chars.remove(dst_char)
				except:
					pass
				
			elif result == self.last_result:
				print("Result is same as last time, char '" + src_char + "' and char '" + dst_char + "' may be both in secret word, or neither")
				self.undecided_chars.append(src_char)
				self.undecided_chars.append(dst_char)
				pass
			else:
				print("Lower result, char '" + src_char + "' is in secret word and char '" + dst_char + "' is not in secret word")
				self.secret_word_chars.append(src_char)
				self.unwanted_chars.append(dst_char)

				try:
					self.undecided_chars.remove(src_char)
				except:
					pass

				try:
					self.undecided_chars.remove(dst_char)
				except:
					pass
		self.last_result = result
		self.guesses[-1].append(result)

		print("Secret words chars: ", self.secret_word_chars)
		print("Chars not in secret word: ", self.unwanted_chars)



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
					print("ValueError exception has occured !!!")
					print(line)
					return


mappings = []
for row in csv.reader(open("out.csv", "r", newline=""), delimiter=','):
	mappings.append(row)

for x in mappings:
	x[1] = x[1].replace(' ', '')
	x[2] = x[2].replace(' ', '')
	x[3] = x[3].replace(' ', '')




"""
words1 = [x[0] for x in mappings]
words2 = [x[1] for x in mappings]

words = list((set(list(words1) + list(words2))))
"""

words = read_words()

guessMachine = GuessMachine(words, mappings)
client = Client(guessMachine)
client.start()
print("Game has ended")
