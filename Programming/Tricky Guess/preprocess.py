import random
import os
import subprocess
import string as string_module
import threading
import queue
import time
import datetime

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


words = read_words()

to_write_queue = queue.Queue()

def preprocess_words(c: str):
	words_with = list(filter(lambda x: c in x , words))
	words_without = list(filter(lambda x: c not in x , words))
	print("Trying to find simillar string with src_char = "+c)
	for word_with_c in words_with:
		lst = find_most_simillar_strings(word_with_c, words_without)
		lst = list(filter(lambda x: x[3] == 11, lst))
		if lst:
			# Find out what char is changed.
			for x in lst:
				tmp_dst_string = x[1]
				simillar_chars = x[2]
				for simillar_char in simillar_chars:
					tmp_dst_string = tmp_dst_string.replace(simillar_char, '')
				dst_char = tmp_dst_string #It should be only length 1

				string = "{}, {}, {}, {}\n".format(word_with_c, x[1], c, dst_char)
				to_write_queue.put(string)
				print(word_with_c, x[1], c, dst_char)



threads = []
for c in string_module.ascii_lowercase:
	threads.append(threading.Thread(target=preprocess_words, args=(c)))

now = datetime.datetime.now()

for x in threads:
	x.start()
for x in threads:
	x.join()


with open("out.csv","w") as file:
	for x in list(to_write_queue.queue):
		file.write(x)
	file.flush()
file.close()

print("Preprocess complete!")

now2 = datetime.datetime.now()
dif = now2 - now
print(dif)

# It took 15 minutes and 8 seconds to complete - total found 1684 combinations
