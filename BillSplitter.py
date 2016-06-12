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
		self.debts.append(Debt(lessor, self, amount))
		lessor.addLoan(self, amount)

	def addLoan(self, debtor, amount):
		self.loans.append(Debt(self, debtor, amount))
		debtor.addDebt(self, amount)


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