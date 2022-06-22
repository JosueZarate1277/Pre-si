import re
patterns = [ 'fox', 'dog', 'horse' ]
text = 'The quick brown fox jumps over the lazy dog.'
for pattern in patterns:
    print('Searching for "%s" in "%s" ->' % (pattern, text)) #Prints on console the assigned string,
                                                             #replacing the '%s' with the variables assigned
                                                             #as arguments, in an orderly manner
    if re.search(pattern, text):
        print('Matched!')
    else:
        print('Not Matched!')