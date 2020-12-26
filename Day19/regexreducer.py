##regexreducer.py
import re

theregexstring = r"((b(a(bb|ab)|b((a|b)(a|b)))|a(b(bb)|a(bb|a(a|b))))b|(((aa|ab)a|(bb)b)b|(((a|b)a|bb)a)a)a)"


#if (anynumchars) remove parens
result = re.sub(r"\(([ab]+)\)", r'\1', theregexstring)

#if any variation of (a|b)(a|b), reduce to  aa|ab|ba|bb
result = re.sub(r"\(([ab])\|([ab])\)", 'aa|ab|ba|bb', result)

#then if a(a|b), reduce to aa|ab, if a(a|b|b), reduce to (aa|ab|ab), etc
#     if (a|b)a reduce to aa|ab also

# result = re.sub(r"([ab]+)\(([ab]+)\|([ab]+)\)", r'\1\2|\1\3', result)

# result = re.sub(r"\(([ab]+)\|([ab]+)\)([ab]+)", r'\1\3|\2\3', result)

print(result)


insidegeneral = r'([ab]+)'

def regexstringconstruct(numinside, side):
	#num inside >= 2
	#if side = r , it's of the form (a|b|...)a
	tmprepl = r''
	tmpstr = r'\(' + r'([ab]+)\|'*(numinside-1) + r'([ab]+)\)'
	if side == 'r':
		tmpstr = tmpstr + r'([ab]+)'

		for i in range(1, numinside+1):
			tmprepl +=  '\\' + str(i) + '\\' + str(numinside+1) + '|'
		tmprepl = tmprepl[:-1]  # take off the trailing |


	else:
		tmpstr = r'([ab]+)' + tmpstr
		for i in range(2, numinside+2):
			tmprepl += '\\1\\' + str(i) + '|'
		tmprepl = tmprepl[:-1]  # take off the trailing |
	
	return tmpstr, tmprepl

for i in range(2, 30):
	resultlast = None
	regexr, replacementr = regexstringconstruct(i, 'r')
	regexl, replacementl = regexstringconstruct(i, 'l')
	while result != resultlast:
		resultlast = result
		
	#	print((regex, replacement))
		result = re.sub(regexr, replacementr, result)

		
	#	print((regex, replacement))
		result = re.sub(regexl, replacementl, result)
		
print(result)