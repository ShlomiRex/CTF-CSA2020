import random
import os
import subprocess
import time


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
	simillar = find_most_simillar_strings(string, words)
	found = None
	for x in simillar:
		if int(x[3]) == 11:
			found = x[1]
			break
	return found

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
	def __init__(self, guess_word_list: list):
		self.gusses = []
		self.last_result = -1
		self.guess_word_list = guess_word_list
		self.possible_chars = [] # Possible chars that can be in secret word, need to confirm
	
	def get_next_guess(self) -> str:
		guess = None
		guess_amount = len(self.gusses)
		# Number of guesses.
		if guess_amount == 0:
			while True:
				# We want to select a string which has 1 char diffirence
				guess = random.choice(self.guess_word_list)
				string = find_simillar_string_1_char_diff(guess, self.guess_word_list)
				if string:
					break
				# else, keep guessing a word untill found
		elif guess_amount == 1:
			# Find simillar string compare to previous guess (there must be one because of previous checks)
			guess = find_simillar_string_1_char_diff(self.gusses[-1][0], self.guess_word_list)

		elif guess_amount == 2:
			result0 = int(self.gusses[0][1])
			result1 = int(self.gusses[1][1])

			# s3 - source char , s4 - dst char mapping
			tmp,tmp2,s3,s4 = get_char_mapping(self.gusses[-2][0], self.gusses[-1][0])
			print("Mapping:",s3," -> ", s4)

			if len(s3) != 1 or len(s4) != 1:
				# This should never happen
				raise "Length of s3 or s4 is not 1. len(s3), len(s4) = " + str(len(s3)) + ", " + str(len(s4))
				exit(-1)

			src_char = list(s3)[0]
			dst_char = list(s4)[0]

			if result1 > result0:
				# dst char is in secret word! (src char is not in secret word - remove it)
				self.__remove_words_containing_char(src_char) #remove words containing source char
				self.__remove_words_not_containing_char(dst_char) #remove words NOT containing dst char

				for x in self.gusses:
					simillar = find_simillar_string_1_char_diff(x[0], self.guess_word_list)
					if simillar:
						print(simillar, "is simillar to", x[0])
						guess = simillar
						break
				if not guess:
					guess = get_random_word_with_simillar_string_1_char_diff(self.guess_word_list)
			elif result1 == result0:
				"""
				1. Both src char and dst char are in the secret word
				2. None of them are in the secret word
				This is the hard part! We need to check each char indevidually! (and after that guess, if we need to remove char, then the other mapped char in previous guess, is in secret word!)
				"""
				self.possible_chars.append(src_char)
				self.possible_chars.append(dst_char)

				simillar1 = find_most_simillar_strings(self.gusses[-2][0], self.guess_word_list)
				simillar2 = find_most_simillar_strings(self.gusses[-1][0], self.guess_word_list)

				print(simillar1)
				print(simillar2)

				if len(simillar1) > 0:
					print("Going to check next (char check): " + simillar1[0])
					guess = simillar1
				elif len(simillar2) > 0:
					print("Going to check next (char check): " + simillar2[0])
					guess = simillar2
				else:
					# They don't have 1 char diffirence at all. We still can't be sure about chars. Need to guess simillar string that is not already guessed
					# Select a word that contains one of the chars (but not both) AND has simillar string 1 char diff
					while True:
						filtered_words = list(self.guess_word_list) #copy list by value
						char1 = self.possible_chars[0]
						char2 = self.possible_chars[1]
						filtered_words = list(filter(lambda x: char1 in x and char2 not in x, filtered_words))
						print("10 words that contain '" + char1 + "' and not '" + char2 + " = " + random.sample(filtered_words, 10))
						# Length of filtered_words > 0 because of previous checks
						for x in filtered_words:
							string = find_simillar_string_1_char_diff(self.gusses[-1][0], self.guess_word_list)
							exit(-1)
			else:
				# src char is in secret word! (dest char is not in secret word - remove it)
				self.__remove_words_containing_char(dst_char) #remove words containing dst char
				self.__remove_words_not_containing_char(src_char) #remove words NOT containing src char

				for x in self.gusses:
					simillar = find_simillar_string_1_char_diff(x[0], self.guess_word_list)
					if simillar:
						print(simillar, "is simillar to", x[0])
						guess = simillar
						break
				if not guess:
					guess = get_random_word_with_simillar_string_1_char_diff(self.guess_word_list)
		elif guess_amount == 3:
			# If possible chars, need to check them
			pass
		else:
			pass
		self.gusses.append([guess])
		try:
			self.guess_word_list.remove(guess) # No need to guess that word again.
		except:
			pass
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
		#self.last_result_greater = (result >= self.last_result)
		self.last_result = result
		self.gusses[-1].append(result)

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

				print("Guessing:", guess_word)

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


words = read_words()

guessMachine = GuessMachine(words)
client = Client(guessMachine)
client.start()
print("Game has ended")