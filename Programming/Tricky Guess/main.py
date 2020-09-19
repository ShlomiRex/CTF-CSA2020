def same_char(str1, str2):
	set1 = set(str1)
	set2 = set(str2)
	intersection = ''.join(sorted(set1.intersection(set2)))
	return intersection

str1 = "doypbugxqvci" # 6 
str2 = "jmofasktndxz" # 4

abc = "abcdefghijklmnopqrstuvwxyz"

for c in str1:
	abc = abc.replace(c, '')

for c in str2:
	abc = abc.replace(c, '')


print("Same chars: \t" + same_char(str1, str2))
print("ABC without chars of str1, str2: \t" + abc)

# Because the first string is 6 instead of 4 in string 2 that means string 1 is better
# Find what string 1 has that string 2 doesn't have

str3 = str1
for c in str2:
	str3 = str3.replace(c, '')

print("str1 chars that str2 doesn't have: \t" + ''.join(sorted(str3)))