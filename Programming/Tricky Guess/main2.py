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

words = [] #list of words that also contain abc dict

def new_abc():
	abc = [] #count a,b,c...z
	for i in range(26):
		abc.append(0)
	return abc

def count_chars(word):
	word = word.lower()
	abc = new_abc()
	for c in word:
		abc[ord(c)-ord('a')] = abc[ord(c)-ord('a')]+1
	return abc

def pseudo_bin_array_to_int(ar):
	s = ""
	for i in ar:
		s += str(i)
	return int(s, 2)

	global guess_numbers
	if word == "motbjlakfgxc":
		print("Successful Guess!")
	else:
		print("Try again")
		guess_numbers = guess_numbers + 1
		if guess_numbers == 15:
			print("Guesses more than 15")
			exit(0)

file = open("words.txt") 
word = file.readline()
while word:
	word = word.strip()

	bin = count_chars(word)
	number = pseudo_bin_array_to_int(bin)
	words.append([word, bin, number])
	word = file.readline()

words.sort(key = lambda words: words[2]) 



def find_most_simillar_strings(string, list):
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
		word_string = ''.join(s)
		result.append([string, word, word_string, max_num_of_simillar_chars])
	return result
		
only_words_list = [x[0] for x in words]


def print_mapping(source_string, dest_string):
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

	print("Mapping:",s3," -> ", s4)
	return [source_string, dest_string, s3, s4]



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
			if last_result > int(guesses[0][1])
				max_string = guesses[0][0]
			else

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