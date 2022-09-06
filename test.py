import itertools
		
class AllTests: 
	def __init__(self, filename: str) -> None: 
		self.allTests = []
  
		with open(filename, 'r') as testFile: 
			lines = testFile.readlines()[1:]
   
			for line in lines:
				test_items = line.split('[')
				identifiers = [item.strip() for item in test_items[0].split(',')[:-1]]
				test_Steps = [item.strip() for item in test_items[1].rstrip(']\n').split(',')]
				testSteps = {}
				for index, test_Step in enumerate(test_Steps):
					testSteps[TestStep(test_Step, index == 0)] = False
			
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


class Test: 
	newID = itertools.count(1).__next__
	def __init__(self, SWTCNumber, TestName, TestGroup, TestSteps=None): 
		self.SWTCNumber = SWTCNumber
		self.TestNumber = Test.newID()
		self.TestName = TestName
		self.TestGroup = TestGroup
		self.TestSteps = TestSteps #dictionary {testSteps: status}
		self.passed = None

		self.precondition = next((testStep if testStep.isPrecondition else None for testStep in self.TestSteps))
		self.preconditionDescription = next((testStep.Description if testStep.isPrecondition else None for testStep in self.TestSteps))
		
	def __repr__(self) -> str:
		return f"Test # {self.TestNumber} - {self.SWTCNumber} - {self.TestName}"
	
	def update(self, newStatus: bool):
		self.passed = newStatus 
	
	def printSteps(self): 
		print(self.TestSteps)
  
	def getallStepsStatus(self): 
		return self.TestSteps

	def getStepsStatus(self, passed: bool): 
		return dict(filter(lambda val: val[1] is passed, self.TestSteps.items()))
  
