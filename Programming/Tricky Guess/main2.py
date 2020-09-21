"""
Shlomi Domnenko

Observations:
* ALL of the words are unique, so that, in each string, no 2 or more same characters appear.
* The result of guessing is number of characters, therefor it naturally tends to count the number of chracters in the guess string. This results in the 'binary' (no 2 same chars) array.
* If you do 10,000 (number of words) divided by 2^15 (15 = number of guesses) you get 0.6 which means it is meant to be binary search.
* We should look at what information we can get from the result of the guess.

vpzytcirhnwj
7 -> We got 7 chars correct
wubqyertjlzg
6 -> We got 6 chars corret

Why the decrease? Let's compare:
vpzytcirhnwj --- sort ---> chijnprtvwyz
wubqyertjlzg --- sort ---> begjlqrtuwyz

Characters that are same:            z, y, w, t, r, j (Total: 6)
Characters that are not in both:     b, c, e, h, g, i, l, n, p, q, u, v (Total: 12)
"""

"""
Random Guess Run Example

doypbugxqvci
6

jmofasktndxz
4

hmfzpoujlisn
3

jvotwpabkcne
5

nxmhviqtyjso
5

txuzslhiacrn
7

ewrhsqvocimn
5

foythegmwjbl
5

owfkyeqtzdan
5

vdjmfgiounaw
5

ckdqnfmhoivu
5

ibasfrmzqjxc
5

rudyhefojnzl
5

pnduqcbhreyi
6

ietbqaysmjpk
4

"""

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




"""
only_words_list = [x[0] for x in words]
first_guess_word = random.choice(only_words_list)

# Second guess word = furthest from the first guess, biggest impact
simillar_strings = find_most_simillar_strings(first_guess_word, only_words_list)
max_num_of_simillar_chars = min(x[3] for x in simillar_strings)
string = None
for x in simillar_strings:
	if x[3] == max_num_of_simillar_chars:
		string = x
		break

second_guess_word = string[1]
"""

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
	
	def get_next_guess(self) -> str:
		guess = None
		guess_amount = len(self.gusses)
		# Number of guesses.
		if guess_amount == 0:
			while True:
				# We want to select a string which has 1 char diffirence
				guess = random.choice(self.guess_word_list)
				simillar = find_most_simillar_strings(guess, self.guess_word_list)
				found = False
				for x in simillar:
					if int(x[3]) == 11:
						found = True
						break
				if found:
					break
		elif guess_amount == 1:
			simillar = find_most_simillar_strings(self.gusses[0][0], self.guess_word_list)
			for x in simillar:
				if int(x[3]) == 11:
					guess = x[1]
					break
		elif guess_amount == 2:
			result0 = int(self.gusses[0][1])
			result1 = int(self.gusses[1][1])

			tmp,tmp2,s3,s4 = get_char_mapping(self.gusses[0][0], self.gusses[1][0])
			print("Mapping:",s3," -> ", s4)

			if result1 > result0:
				# dst char is in secret word! (src char is not in secret word)
				self.__remove_words_containing_char(list(s3)[0])
				pass
			elif result1 == result0:
				# 1. Both src char and dst char are in the secret word
				# 2. None of them are in the secret word
				# This is the hard part! We need to check each char indevidually! (and after that guess, if we need to remove char, then the other mapped char in previous guess, is in secret word!)
				possible_char1 = list(s3)[0]
				possible_char2 = list(s3)[1]
				pass
			else:
				# src char is in secret word! (dest char is not in secret word)
				self.__remove_words_containing_char(list(s3)[0])
				pass
		else:
			pass
		self.gusses.append([guess])
		self.guess_word_list.remove(guess) # No need to guess that word again.
		return guess
	
	def __remove_words_containing_char(self, char: str):
		words_to_remove = []
		for x in self.guess_word_list:
			if char in x:
				words_to_remove.append(x)
		for x in words_to_remove:
			self.guess_word_list.remove(x)
		print("Removed " + str(len(words_to_remove)) + " words (containing '" + char + "'), left: " + str(len(self.guess_word_list)) + "/10000")
	
	def set_last_result(self, result: int):
		"""
		Upon receiving number of characters correct from the server, this function gets called.
		"""
		#self.last_result_greater = (result >= self.last_result)
		self.last_result = result
		self.gusses[-1].append(result)
		print("Guesses: ", self.gusses)

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





"""
# Talk with server
cmd = "nc tricky-guess.csa-challenge.com 2222"
cmd2 = ['nc','tricky-guess.csa-challenge.com', '2222']

proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stdin=subprocess.PIPE, shell=True)


#Skip introduction
while True:
	line = proc.stdout.readline()
	if not line:
		break

	print(line.decode())

	if b"GO !" in line:
		#Begin guess game
		break

guesses = []
guess_word_list = only_words_list
only_diffirence = None
last_result = -1
last_result_greater = None



# 15 Tries
for i in range(16):
	guess_word = None

	if i == 0:
		guess_word = first_guess_word
	elif i == 1:
		guess_word = second_guess_word
	elif i == 2:
		if last_result_greater:
			#print("Guess 2 is better than 1")
			simillar_strings = find_most_simillar_strings(second_guess_word, guess_word_list)
		else:
			#print("Guess 1 is better than 2")
			simillar_strings = find_most_simillar_strings(first_guess_word, guess_word_list)
		max_num_of_simillar_chars = max(x[3] for x in simillar_strings)
		max_simillar_strings = []
		for ss in simillar_strings:
			if ss[3] == max_num_of_simillar_chars:
				max_simillar_strings.append(ss)

		guess_word = max_simillar_strings[0][1]

		only_diffirence = set(guess_word)
		if last_result_greater == False:
			for c in first_guess_word:
				if c in only_diffirence:
					only_diffirence.remove(c)
		else:
			for c in second_guess_word:
				if c in only_diffirence:
					only_diffirence.remove(c)
		print("Only diffirence is:", only_diffirence)
	elif i == 3:
		results = [x[1] for x in guesses]
		max = -1
		max_string = None

		if int(guesses[0][1]) > int(guesses[1][1]):
			if last_result > int(guesses[0][1]):
				max_string = guesses[0][0]
			else:
				pass

		for x in guesses:
			if x[1] >= max:
				max = x[1]
				max_string = x[0]
				break

		if last_result > max:
			#Better
			print("Last result: {0} is better than{1}, secret word possible contains: {2}", last_result, max, only_diffirence)
		elif last_result == max:
			#Middle
			print("Mapping didn't change")
			print_mapping(max_string, guesses[:-1][0])
		elif last_result < max:
			#Worse
			print("Last result worse, secret word possible doesn't contain: ", only_diffirence)
		else:
			print("WTF")
		
		break
	else:
		break

	#Remove the guess word from possible words to guess
	guess_word_list.remove(guess_word)

	print("Guessing:", guess_word)
	guess_word = guess_word.encode()

	#Write guess
	bytes_written = proc.stdin.write(guess_word)
	proc.stdin.flush() #Very important, took me a lot of time to find the problem. Must write now instead of buffer filling. 

	#Read result
	line = proc.stdout.readline().decode().strip()
	try:
		result = int(line)
		print(str(result))
		if result > last_result:
			last_result_greater = True
		else:
			last_result_greater = False
		last_result = result
		guesses.append([guess_word.decode().strip(), result])
	except ValueError:
		# Read last line
		print(line)
		break

print("Guess results:\n",guesses)
"""