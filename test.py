import re

regex = r".+(html)"
target1 = r"2"
line = r'/pages/index.html'

suffix = re.match(regex, line)

if suffix:
    print("Found:", suffix.group(1))
else:
    print("Wrong")
