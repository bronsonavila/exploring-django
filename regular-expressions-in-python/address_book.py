import re

names_file = open('names.txt', encoding='utf-8')
data = names_file.read()
names_file.close()

# print(re.match(r'Love', data))
# print(re.search(r'Kenneth', data))
# print(re.search(r'\(\d\d\d\) \d\d\d-\d\d\d\d', data))
# print(re.findall(r'\(?\d{3}\)?-?\s?\d{3}-\d{4}', data))
# print(re.findall(r'\w*, \w+', data))
# print(re.findall(r'[-\w\d+.]+@[-\w\d.]+', data))
# print(re.findall(r'\b[trehous]{9}\b', data, re.I))
# print(re.findall(r'\b@[-\w\d.]*[^gov\t]+\b', data))

# print(re.findall(r'''
#   \b[-\w]+, # Find a word boundary, one or more hyphens or word characters, and a comma.
#   \s        # Find one white space.
#   [-\w ]+   # Find one or more hyphens, word characters, or explicit space characters.
#   [^\t\n]   # Ignore tabs and newlines.
# ''', data, re.X))

line = re.compile(r'''
    ^(?P<name>(?P<last>[-\w ]*),\s(?P<first>[-\w ]+))\t # Name (with subgroups)
    (?P<email>[-\w\d.+]+@[-\w\d.]+)\t                   # Email
    (?P<phone>\(?\d{3}\)?-?\s?\d{3}-\d{4})?\t           # Phone
    (?P<job>[\w\s]+,\s[\w\s.]+)\t?                      # Job and company
    (?P<twitter>@[\w\d]+)?$                             # Twitter
''', re.X | re.M)

# print(re.search(line, data).groupdict())
# print(line.search(data).groupdict())

for match in line.finditer(data):
    print(match.group('name'))

for match in line.finditer(data):
    print('{first} {last} <{email}>'.format(**match.groupdict()))
