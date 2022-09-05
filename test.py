import itertools



# Linked List Node
class Node:
	def __init__(self, data):
		self.data = data
		self.next = None


# Create & Handle List operations
class LinkedList:
	def __init__(self):
		self.head = None

	# Method to display the list
	def printList(self):
		temp = self.head
		while temp:
			print(temp.data, end=" ")
			temp = temp.next

	def reverse(self): 
		prev = None
		current = self.head
		while (current is not None): 
			next = current.next
			current.next = prev
			prev = current
			current = next
		self.head = prev

	# Method to add element to list
	def addToList(self, newData):
		newNode = Node(newData)
		if self.head is None:
			self.head = newNode
			return

		last = self.head
		while last.next:
			last = last.next

		last.next = newNode

# Function to merge the lists
# Takes two lists which are sorted
# joins them to get a single sorted list
def mergeLists(headA, headB):

	# A dummy node to store the result
	dummyNode = Node(0)

	# Tail stores the last node
	tail = dummyNode
	while True:

		# If any of the list gets completely empty
		# directly join all the elements of the other list
		if headA is None:
			tail.next = headB
			break
		if headB is None:
			tail.next = headA
			break

		# Compare the data of the lists and whichever is smaller is
		# appended to the last of the merged list and the head is changed
		if headA.data[0] < headB.data[0]:

			tail.next = headA
			headA = headA.next
		elif headA.data[0] > headB.data[0]:

			tail.next = headB
			headB = headB.next

		else:
			tail.next = headB
			headB = headB.next

		# Advance the tail
		tail = tail.next

	# Returns the head of the merged list
	return dummyNode.next

class AllTestSteps: 
	def __init__(self, filename: str) -> None: 
		test_steps_store = {}
		test_step_store = {}
		test_preconditions = []
		
		with open(filename, 'r') as testStepsFile:
			lines = testStepsFile.readlines()[1:]
			for line in lines:  
				split_line = line.split(',')
				testStepsID = split_line[0]
				precondition = split_line[1]
				preconditionStep = TestStep(precondition, True)
				# [preconditionStep] 
				testSteps = [preconditionStep] + [TestStep(testStep, False) for testStep in split_line[2:]]
				test_preconditions.append(preconditionStep)
				
				for testStep in testSteps: 
					if testStep.Description in test_step_store: 
						test_step_store[testStep.Description.strip()].append(testStep.TestStepID)
					else: 
						test_step_store[testStep.Description.strip()] = [testStep.TestStepID]
				
				test_steps_store[testStepsID] = TestSteps(testStepsID, precondition, testSteps)
		
		self.test_steps_store = test_steps_store
		self.test_step_store = test_step_store
		self.test_preconditions = test_preconditions
		
class AllTests: 
	def __init__(self, filename: str) -> None: 
		with open(filename, 'r') as testFile: 
			lines = testFile.readlines()[1:]
			self.allTests = [Test(*line.split(',')) for line in lines]
			
class TestSteps(LinkedList): 
	def __init__(self, TestStepsID, Precondition, TestSteps) -> None:
		self.TestStepsID = TestStepsID
		self.Precondition = Precondition
		self.TestSteps = TestSteps
		self.head = Node((self.TestSteps[0].TestStepID, self.TestSteps[0]))
		self.SWTCNumber = None

		for testStep in self.TestSteps[1:]: 
			self.addToList((testStep.TestStepID, testStep))
			
		
	# def __repr__(self) -> str:
	#     test_step_repr = f"Test Steps ID: {self.TestStepsID} \nPrecondition: {self.Precondition} \nTestSteps:"
	#     for step in self.TestSteps: 
	#         test_step_repr += f"\n\t{step}"
	#     return test_step_repr
	
	def asList(self) -> list:
		return list(self.TestSteps)

class TestStep: 
	newID = itertools.count().__next__
	def __init__(self, Description: str, isPrecondition: bool, passed:bool=False) -> None:
		self.TestStepID = TestStep.newID()
		self.Description = Description
		self.isPrecondition = isPrecondition
		self.passed = passed
		
	def __str__(self) -> str:
		return self.Description
	
	def __repr__(self) -> str:
		return  f"{str(self.passed).upper()} ------ Description: {self.Description}"
		
	def update(self, newStatus: bool):
		self.passed = newStatus 
		
	def asString(self):
		return self.Description

class Test: 
	newID = itertools.count(1).__next__
	def __init__(self, SWTCNumber, TestName, TestGroup, TestStepID, TestSteps=None): 
		self.SWTCNumber = SWTCNumber
		self.TestNumber = Test.newID()
		self.TestName = TestName
		self.TestGroup = TestGroup
		self.TestStepID = TestStepID
		self.TestSteps = TestSteps
		self.TestStepIDs = None
		self.TestStepsStatus = []
		self.passed = None
		
	def __repr__(self) -> str:
		return f"Test # {self.TestNumber} - {self.SWTCNumber} - {self.TestName}"
	
	def update(self, newStatus: bool):
		self.passed = newStatus 
	
	def printSteps(self): 
		print(self.TestSteps)

