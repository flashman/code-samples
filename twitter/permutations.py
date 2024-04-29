
def permutations(n):
    '''
    Display all permutations of the first n characters in the 
    alphabet eg ['A' 'B' 'C'  ...] in ascending order.
    '''
    charSet = [ chr(v) for v in range(65,65+n) ]
    build(charSet)


def build(charSet,s=''):
    '''Recursively build  strings of all permutations of characters in charSet'''
    if  len(charSet) == 0:
        print s
    else:
        for c in charSet:
            newCharSet =  [ d for d in charSet if d!=c ]
            build(newCharSet, s+c )
