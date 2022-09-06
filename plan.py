from test import AllTests, Test
from rich import print
from collections import OrderedDict

class Plan(OrderedDict): 
    def __init__(self) -> None:
        self.stepExecutionOrder = []
        
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)
        
    def writePlan(self, filename: str):
        with open(filename, 'w') as writeFile: 
            writeFile.write('\n'.join(self.stepExecutionOrder) + '\n')

def calculateStepsByPrecondition(test: Test, precondition_dependent_Steps: dict) -> dict:
    if test.preconditionDescription not in precondition_dependent_Steps:
        precondition_dependent_Steps[test.preconditionDescription] = len(test.TestSteps) - 1
    else: 
        precondition_dependent_Steps[test.preconditionDescription] += len(test.TestSteps) - 1
        
    return precondition_dependent_Steps

def calculateTestsByPrecondition(test: Test, precondition_dependent_Tests: dict) -> dict:
    if test.precondition not in precondition_dependent_Tests:
        precondition_dependent_Tests[test.preconditionDescription] = 1
    else: 
        precondition_dependent_Tests[test.preconditionDescription] += 1
    
    return precondition_dependent_Tests

def calculatePreconditionExecutionOrderByRatio(test: Test, precondition_dependent_Steps: dict, precondition_dependent_Tests: dict) -> dict:
    ratio_dict = {key: precondition_dependent_Tests[key] / precondition_dependent_Steps.get(key, 0) for key in precondition_dependent_Tests.keys()}
    return {k: v for k, v in sorted(ratio_dict.items(), key=lambda item: item[1])}

def executePrecondition(plan: Plan, precondition: str, allTests: list[Test]): 
    for test in allTests: 
        if test.preconditionDescription == precondition: 
            test.precondition.update(True)
            test.TestSteps[test.precondition] = True
            plan.stepExecutionOrder.append(f'{test.SWTCNumber} - Execute Precondition: {test.preconditionDescription}')
        

def main(finalTestPlan: Plan):
    
    #Calculate the number of tests or test steps that rely on each precondition
    #Based on the number of Machines that are available to the user
    #Execute the precondition who has the most tests that rely on it 
    #   and remove it from the list, and so on, base on machine availability.
    #Process preconditions first
        #For each precondition in the list of preconditions
            #For each Test that relies on this test step (the test step is in their list of test steps): 
                #add the test and step to the test plan
            #update the status of the precondition step as passed
            #update the status of the precondition step in the test case that has the precondition as passed
            #remove the precondition step from the dictionary of enumerations:step unique identifiers
    
    #Process the remaining step lists form the stepCollection[count] = value
    #Sort  
    
    allTests = AllTests('tests.csv').allTests
    precondition_dependent_Steps = {}  
    precondition_dependent_Tests = {}
    for test in allTests:
        precondition_dependent_Steps = calculateStepsByPrecondition(test, precondition_dependent_Steps)
        precondition_dependent_Tests = calculateTestsByPrecondition(test, precondition_dependent_Tests)
        ratio_steps_tests = calculatePreconditionExecutionOrderByRatio(test, precondition_dependent_Steps, precondition_dependent_Tests)
    
    numberofMachinesAvailable = int(input("Enter the number of machines available to run tests: "))
    
    #If the user has X preconditions and Y machines, then they have X // Y clear iterations with X % Y 
    # remainder. When the number of preconditions is less than the number of machines alster the 
    # number of machines available.
    
    while len(ratio_steps_tests) > 0:
        if len(ratio_steps_tests) < numberofMachinesAvailable:
            numberofMachinesAvailable = len(ratio_steps_tests)
            
        for _ in range(numberofMachinesAvailable):
            bestPrecondition = min(ratio_steps_tests, key=ratio_steps_tests.get)
            ratio_steps_tests.pop(bestPrecondition)
            executePrecondition(finalTestPlan, bestPrecondition, allTests)
            
            for test in allTests: 
                if bestPrecondition == test.preconditionDescription:
                    print(test.getStepsStatus(True))
                    print(test.getStepsStatus(False))
                    print('-------------------------------')
                    
    finalTestPlan.writePlan('test_plan.txt')

if __name__ == "__main__":
    finalTestPlan = Plan()
    main(finalTestPlan)
    
"""

pop this precondition from the tests from the bottom of their step stacks and write to output in highest ration order


"""