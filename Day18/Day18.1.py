from functools import reduce

with open(r'.\Day18\input.txt') as thefile:
	rawinput = thefile.read().strip().replace(' ', '').split('\n')
#rawinput has raw text of each line per index


#function will locate the first instance of a complete subexpression () evaluate and replace it
def evalnextsub(expression):
	#dothings
	return

#given an expression (which must not contain parentheses), return the result
def evalexpression(expression):
	
	def operate2(num, expression = None):
		#to allow for first run, if expression is not provided, return the num
		#expression is expected as (operator, number)
		#this is intended to work with reduce after zipping an expression with itself. 
		tmpval = None
		if expression is None:
			tmpval = int(num)
		else:
			if expression[0] == '+':
				tmpval = num + int(expression[1])
			elif expression[0] == '*':
				tmpval = num * int(expression[1])
		return tmpval

	
	tmpval = False
	if expression.find('(') == -1 and  expression.find(')') == -1:
		expression = list(expression)
		tupexp = list(zip(expression[1::2], expression[2::2]))
		tmpval = reduce(operate2, tupexp, int(expression[0]))
			
	else:
		print("invalid expression in evalexpression")
	
	return tmpval

#given a list or a tuple of 3 elements, number, operator, number, will carry out the operation
#at least in part 1, only have addition and multiplication
def operate(expression):
	tmpval = 0
	if expression[1] == '+':
		tmpval = int(expression[0]) + int(expression[2])
	elif expression[1] == '*':
		tmpval = int(expression[0]) * int(expression[2])
	else:
		print("invalid expression in operate function")
		return None
	return tmpval


	

print(evalexpression('2*9+5'))
