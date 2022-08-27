import itertools


class AllTestSteps: 
    def __init__(self, filename: str) -> None: 
        test_steps_store = {}
        test_step_store = {}
        
        with open(filename, 'r') as testStepsFile:
            lines = testStepsFile.readlines()[1:]
            for line in lines: 
                split_line = line.split(',')
                testStepsID = split_line[0]
                precondition = split_line[1]
                testSteps = [TestStep(testStep) for testStep in split_line[1:]]
                
                for testStep in testSteps: 
                    if testStep.Description in test_step_store: 
                        test_step_store[testStep.Description.strip()].append(testStep.TestStepID)
                    else: 
                        test_step_store[testStep.Description.strip()] = [testStep.TestStepID]
                
                test_steps_store[testStepsID] = TestSteps(testStepsID, precondition, testSteps)
        
        self.test_steps_store = test_steps_store
        self.test_step_store = test_step_store

class AllTests: 
    def __init__(self, filename: str) -> None: 
        with open(filename, 'r') as testFile: 
            lines = testFile.readlines()[1:]
            self.allTests = [Test(*line.split(',')) for line in lines]
            
class TestSteps: 
    def __init__(self, TestStepsID, Precondition, TestSteps) -> None:
        self.TestStepsID = TestStepsID
        self.Precondition = Precondition
        self.TestSteps = TestSteps
        
    def __repr__(self) -> str:
        test_step_repr = f"Test Steps ID: {self.TestStepsID} \nPrecondition: {self.Precondition} \nTestSteps:"
        for step in self.TestSteps: 
            test_step_repr += f"\n\t{step}"
        return test_step_repr
    
    def asList(self) -> list:
        return list(self.TestSteps)

class TestStep: 
    newID = itertools.count().__next__
    def __init__(self, Description) -> None:
        self.TestStepID = TestStep.newID()
        self.Description = Description
        
    def __repr__(self) -> str:
        return f"Step ID: {self.TestStepID}, Description: {self.Description}"
            
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
        
    def __repr__(self) -> str:
        return f"Test # {self.TestNumber} - {self.SWTCNumber} - {self.TestName}"
    
    def printSteps(self): 
        print(self.TestSteps)
        
allTestSteps = AllTestSteps('test_steps.csv')
allTestStepsStore = allTestSteps.test_steps_store
allTestStepStore = allTestSteps.test_step_store
for key, value in allTestStepStore.items(): 
    print(f"{key}:{value}")
    
allTests = AllTests('tests.csv').allTests
for test in allTests:
    try:
        
        test.TestSteps = allTestStepsStore[test.TestStepID.strip()]
        print(test.TestSteps)
        test.TestStepIDs = [testStep.TestStepID for testStep in test.TestSteps.asList()]
        print(test.TestStepIDs)
        test.printSteps()
    except Exception:
        print(f'{test} didnt work')

        