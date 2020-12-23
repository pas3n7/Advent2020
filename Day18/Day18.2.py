from functools import reduce
import re


class expression:
	def __init__(self, expression):
		self.expression = expression

	#this will eval the whole expression, recursively
	def evalexpression(self, expression = None):
		if expression is None:
			expression = self.expression
		tmpexp = self.evalnextsub(expression)
		if tmpexp:
			#evalnexsub returned something, so try it again
			return self.evalexpression(tmpexp)
		else:
			#self.evalnextsub returned nothing, meaning there are no more parens
			return self.evalsubexpression(expression)


	#function will locate the first instance of a complete subexpression () evaluate and replace it
	def evalnextsub(self, expression):
		#look for the first set of closed parens
		match = re.search(r'\([^\(\)]+\)', expression)
		tmpexp = None
		if match:
			thisexp = expression[match.start() + 1:match.end()-1]
			tmpexp = expression[:match.start()] + str(self.evalsubexpression(thisexp)) + expression[match.end():]
		return tmpexp

	def evalsubexpression(self, expression):
				
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
			expression = expression.split(' ')
			while '+' in expression:
				multindex = expression.index('+')
				product = self.operate((expression.pop(multindex-1), expression.pop(multindex-1), expression.pop(multindex-1)))
				expression.insert(multindex-1, product)
			while '*' in expression:
				multindex = expression.index('*')
				product = self.operate((expression.pop(multindex-1), expression.pop(multindex-1), expression.pop(multindex-1)))
				expression.insert(multindex-1, product)
			tmpval = expression[0]
		else:
			print("invalid expression in evalsubexpression" + expression)
		
		return tmpval

	#given a list or a tuple of 3 elements, number, operator, number, will carry out the operation
	#at least in part 1, only have addition and multiplication
	def operate(self, expression):
		tmpval = 0
		if expression[1] == '+':
			tmpval = int(expression[0]) + int(expression[2])
		elif expression[1] == '*':
			tmpval = int(expression[0]) * int(expression[2])
		else:
			print("invalid expression in operate function")
			return None
		return tmpval


with open(r'.\Day18\input.txt') as thefile:
	rawinput = thefile.read().strip().split('\n')
#rawinput has raw text of each line per index

expressions = [expression(x) for x in rawinput]

# print([x.evalexpression() for x in expressions])

setsum = sum([x.evalexpression() for x in expressions])

print(setsum)