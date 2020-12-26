##regexreducer.py

import re

theregexstring = r"(b(b(aba|baa)|a(b(ab|(a|b)a)|a(ba|ab)))|a(b((ab|(a|b)a)b|((a|b)a|bb)a)|a(bab|(ba|bb)a)))"





def reduceregex(regex, numtoreduce = 30):

	result = regex

	#then if a(a|b), reduce to aa|ab, if a(a|b|b), reduce to (aa|ab|ab), etc
	#     if (a|b)a reduce to aa|ab also

	# result = re.sub(r"([ab]+)\(([ab]+)\|([ab]+)\)", r'\1\2|\1\3', result)

	# result = re.sub(r"\(([ab]+)\|([ab]+)\)([ab]+)", r'\1\3|\2\3', result)

	result = regex
	def regexstringconstruct(numtoreduce, side):
		#num inside >= 2
		#if side = r , it's of the form (a|b|...)a
		tmprepl = r''
		tmpstr = r'\(' + r'([ab]+)\|'*(numtoreduce-1) + r'([ab]+)\)'
		if side == 'r':
			tmpstr = tmpstr + r'([ab]+)'

			for i in range(1, numtoreduce+1):
				tmprepl +=  '\\' + str(i) + '\\' + str(numtoreduce+1) + '|'
			tmprepl = tmprepl[:-1]  # take off the trailing |


		else:
			tmpstr = r'([ab]+)' + tmpstr
			for i in range(2, numtoreduce+2):
				tmprepl += '\\1\\' + str(i) + '|'
			tmprepl = tmprepl[:-1]  # take off the trailing |
		
		return tmpstr, tmprepl

	for i in range(2, numtoreduce):
		resultlast = None
		regexr, replacementr = regexstringconstruct(i, 'r')
		regexl, replacementl = regexstringconstruct(i, 'l')
		while result != resultlast:
			resultlast = result
					#if (anynumchars) remove parens
			result = re.sub(r"\(([ab]+)\)", r'\1', result)

			#if any variation of (a|b)(a|b), reduce to  aa|ab|ba|bb
			result = re.sub(r"(\(([ab])\|([ab])\)){2}", 'aa|ab|ba|bb', result)
		#	print((regex, replacement))
			result = re.sub(regexr, replacementr, result)

			
		#	print((regex, replacement))
			result = re.sub(regexl, replacementl, result)
	return result

reduced = reduceregex(theregexstring)

print(reduced)
print('\n')


