import re                                #Regular Expressions' library

def text_match(text):
    patterns = '^[a-z]+_[a-z]+$'         #Define characters to find on the text
    if not re.search(patterns, text):    #Inverted logic for search
        return 'Found a match!'          #Prints if match is not found
    else:
        return('Not matched!')           #Prints if match is found

print(text_match("aab_cbbbc"))
print(text_match("aab_Abbbc"))
print(text_match("Aaab_abbbc"))