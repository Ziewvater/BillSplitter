class Person:
	'''
	Person who owes money to another
	'''

	# Running count of `Person`s created during the running of the program.
	# Used for creating the unique IDs for new `Person` objects.
	globalIDCount = 0

	def __init__(self, firstName, lastName):
		self.firstName = firstName
		self.lastName = lastName

		# Give unique ID to user
		Person.globalIDCount += 1
		self.id = Person.globalIDCount

	def __str__(self):
		return self.fullName()

	def __eq__(self, other):
		return (self.id == other.id) and (self.fullName() == other.fullName())

	def fullName(self):
		return "{0} {1}".format(self.firstName, self.lastName)


class Debt:
	'''
	A debt between two given persons.
	'''

	def __init__(self, lender, debtor, amount):
		self.lender = lender
		self.debtor = debtor
		self.amount = amount

	def __str__(self):
		desc = "<Debt>: {0} owes {1} ${2}".format(self.debtor, self.lender, self.amount)
		return desc

	def participants(self):
		return [self.lender, self.debtor]


class DebtGraph:
	'''
	Maps the debts between persons
	'''

	def __init__(self):
		self.persons = []
		self.debts = []

	def addPerson(self, person):
		'''
		Adds a person to the graph
		'''
		self.persons.append(person)

	def addNewDebt(self, lender, debtor, amount):
		 self.debts.append(Debt(lender, debtor, amount))

	def debtsBetween(self, person1, person2):
		def contains(debt):
			index1 = debt.participants().index(person1)
			index2 = debt.participants().index(person2)
			return index1 is not None and index2 is not None

		return filter(contains, self.debts)

	def validateDebts(self, person1, person2):
		p1p2Debts = self.debtsBetween(person1, person2)
		p1Owes = sum(map(lambda x: x.amount, filter(lambda x: x.debtor == person1, p1p2Debts)))
		p2Owes = sum(map(lambda x: x.amount, filter(lambda x: x.debtor == person2, p1p2Debts)))
		print "P1 owes {0}".format(p1Owes)
		print "P2 owes {0}".format(p2Owes)

	def reduceDebts(self, person1, person2):
		'''
		Reduces the loan amounts between the given two persons.

		return: GraphResult with the debt.
		'''
		p1p2Debts = self.debtsBetween(person1, person2)
		p1Owes = sum(map(lambda x: x.amount, filter(lambda x: x.debtor == person1, p1p2Debts)))
		p2Owes = sum(map(lambda x: x.amount, filter(lambda x: x.debtor == person2, p1p2Debts)))

		if p1Owes > p2Owes:
			# p1 owes more to p2
			debt = Debt(person2, person1, p2Owes - p1Owes)
			return GraphResult(GraphResult.ResultType.Debt, debt)
		elif p2Owes > p1Owes:
			# p2 owes more to p1
			debt = Debt(person1, person2, p2Owes - p1Owes)
			return GraphResult(GraphResult.ResultType.Debt, debt)
		else:
			# total diff is 0, nobody owes anyone
			return GraphResult(GraphResult.ResultType.Resolved)

class GraphResult:
	
	class ResultType:
		Debt = "DEBT"
		Resolved = "RESOLVED"

	def __init__(self, type, debt=None):
		self.type = type
		self.debt = debt

	def __str__(self):
		if self.type == GraphResult.ResultType.Debt:
			return "[{0}]: {1}".format(self.type, self.debt)
		else:
			return "[{0}]".format(self.type)


if __name__ == '__main__':
	def test(condition, failMessage, failEvaluation = None):
		'''
		Tests to see if the condition works and prints the given error message
		if the test fails.
		'''
		if not condition:
			print failMessage
			if failEvaluation is not None:
				print "[FAIL] " + failEvaluation
			return False
		else:
			return True

	print("Testing graph reduction")
	graph = DebtGraph()
	gp1 = Person("Nebra", "Jillkinson")
	gp2 = Person("Bravid", "Jenderson")
	graph.addPerson(gp1)
	graph.addPerson(gp2)
	graph.addNewDebt(gp1, gp2, 150)
	graph.addNewDebt(gp1, gp2, 175)
	graph.addNewDebt(gp2, gp1, 200)

	result = graph.reduceDebts(gp1, gp2)
	test(result.type == GraphResult.ResultType.Debt, "Result type should have been DEBT")
	test(result.debt.lender == gp1, "lender from graph should be Nebra", "lender from graph is {0}".format(result.debt.lender))
	test(result.debt.debtor == gp2, "debtor from graph should be Bravid", "debtor from graph is {0}".format(result.debt.debtor))
	test(result.debt.amount == ((150 + 175) - 200), "Amount should be "+str((150 + 175) - 200))

	print("\nValidation of debts")
	graph.validateDebts(gp1, gp2)