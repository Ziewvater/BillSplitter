class Person:
	'''
	Person who owes money to another
	'''

	def __init__(self, firstName, lastName):
		self.firstName = firstName
		self.lastName = lastName
		self.debts = []
		self.loans = []

	def __str__(self):
		return self.fullName()

	def fullName(self):
		return "{0} {1}".format(self.firstName, self.lastName)

	def addDebt(self, lessor, amount):
		newDebt = Debt(lessor, self, amount)
		self.debts.append(newDebt)
		lessor.loans.append(newDebt)

	def addLoan(self, debtor, amount):
		newLoan = Debt(self, debtor, amount)
		self.loans.append(newLoan)
		debtor.debts.append(newLoan)


class Debt:
	'''
	A debt between two given persons.
	'''

	def __init__(self, lessor, lessee, amount):
		self.lessor = lessor
		self.lessee = lessee
		self.amount = amount

	def __str__(self):
		desc = "{0} owes {1} ${2}".format(self.lessee, self.lessor, self.amount)
		return desc



if __name__ == '__main__':
	def test(condition, failMessage):
		'''
		Tests to see if the condition works and prints the given error message
		if the test fails.
		'''
		if not condition:
			print(failMessage)

	# Perform some tests
	p1 = Person("Beatrice", "Carter")
	p2 = Person("John", "Randolf")

	print("Testing adding debts")
	p1.addDebt(p2, 20)
	test(p1.debts[0].amount == 20, 'Beatrice should owe John $20')
	test(p2.loans[0].amount == 20, 'John should be owed $20 by Beatrice')

	print("Testing adding loans")
	p1.addLoan(p2, 40)
	test(p1.loans[0].amount == 40, 'Beatrice should be owed $40 by John')
	test(p2.debts[0].amount == 40, 'John should owe Beatrice $40')