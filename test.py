import itertools
		
class AllTests: 
	def __init__(self, filename: str) -> None: 
		self.allTests = []
  
		with open(filename, 'r') as testFile: 
			lines = testFile.readlines()[1:]
   
			for line in lines:
				test_items = line.split(',')
				identifiers = test_items[:3]
				test_Steps = test_items[3:]
				testSteps = []
				for index, test_Step in enumerate(test_Steps):
					test_Step = test_Step.strip('[').strip(']')
					testSteps.append(TestStep(test_Step, index is 0))
			
				self.allTests.append(Test(*identifiers, TestSteps=testSteps))

class TestStep: 
	newID = itertools.count(1).__next__
	def __init__(self, Description: str, isPrecondition: bool, passed:bool=False) -> None:
		self.TestStepID = TestStep.newID()
		self.Description = Description
		self.isPrecondition = isPrecondition
		self.passed = passed
		
	def __str__(self) -> str:
		return self.Description
	
	def __repr__(self) -> str:
		return  self.Description
		
	def update(self, newStatus: bool):
		self.passed = newStatus 
		
	def asString(self):
		return self.Description

class Test: 
	newID = itertools.count(1).__next__
	def __init__(self, SWTCNumber, TestName, TestGroup, TestSteps=None): 
		self.SWTCNumber = SWTCNumber
		self.TestNumber = Test.newID()
		self.TestName = TestName
		self.TestGroup = TestGroup
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

