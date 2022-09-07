from test import AllTests, Test, TestStep
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



def executePrecondition(plan: Plan, bestPrecondition: str, allTests: list): 
    for test in allTests: 
        if bestPrecondition == test.preconditionDescription: 
            test.precondition.update(True)
            test.TestSteps[test.precondition] = True
            plan.stepExecutionOrder.append(f'{test.SWTCNumber} - Execute Precondition: {bestPrecondition}')

def executeTestStep(plan: Plan, bestTestStep: TestStep, allTests: list, bestPrecondition): 
    for test in allTests: 
        if bestPrecondition == test.preconditionDescription:
            if bestTestStep == test.getStepsStatus(False).popitem()[0]: 
                test.TestSteps[bestTestStep] = True
                plan.stepExecutionOrder.append(f'{test.SWTCNumber} - Execute Test Step: {bestTestStep}')

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

def calculatePreconditionExecutionOrderByRatio(precondition_dependent_Steps: dict, precondition_dependent_Tests: dict) -> dict:
    ratio_dict = {key: precondition_dependent_Tests[key] / precondition_dependent_Steps.get(key, 0) for key in precondition_dependent_Tests.keys()}
    return {k: v for k, v in sorted(ratio_dict.items(), key=lambda item: item[1])}

def calculateTestsByTestStep(test: Test, test_step_dependentTests: dict) -> dict:
    next_test_Step = test.getStepsStatus(False).popitem()[0]
    print(next_test_Step)

    if next_test_Step:
        if next_test_Step not in test_step_dependentTests: 
            test_step_dependentTests[next_test_Step] = 1
        else:
            test_step_dependentTests[next_test_Step] += 1

    return test_step_dependentTests

def calcualteStepsbyTestStep(test: Test, test_step_dependentSteps: dict) -> dict:
    steps_not_executed = test.getStepsStatus(False)
    next_test_Step = steps_not_executed.popitem()[0]
    
    if next_test_Step:
        if next_test_Step not in test_step_dependentSteps:
            test_step_dependentSteps[next_test_Step] = len(steps_not_executed)
        else: 
            test_step_dependentSteps[next_test_Step] += len(steps_not_executed)

    return test_step_dependentSteps

def calculateStepExecutionOrderbyTestStep(test_step_dependentTests: dict, test_step_dependentSteps: dict):
    ratio_dict = {key: test_step_dependentTests[key] / test_step_dependentSteps.get(key, 0) for key in test_step_dependentTests.keys()}
    return {k: v for k, v in sorted(ratio_dict.items(), key=lambda item: item[1])}
        

def main(finalTestPlan: Plan):

    
    allTestsObject = AllTests('tests.csv')
    allTests = allTestsObject.tests
    minSteps = allTestsObject.minRemainingStepCount
    precondition_dependent_Steps = {}  
    precondition_dependent_Tests = {}
    for test in allTests:    
        precondition_dependent_Steps = calculateStepsByPrecondition(test, precondition_dependent_Steps)
        precondition_dependent_Tests = calculateTestsByPrecondition(test, precondition_dependent_Tests)
        ratio_precondition_by_tests_to_steps = calculatePreconditionExecutionOrderByRatio(precondition_dependent_Steps, precondition_dependent_Tests)
    
    # numberofMachinesAvailable = int(input("Enter the number of machines available to run tests: "))
    numberofMachinesAvailable = 2
    
    #If the user has X preconditions and Y machines, then they have X // Y clear iterations with X % Y 
    # remainder. When the number of preconditions is less than the number of machines alster the 
    # number of machines available.
    
    while len(ratio_precondition_by_tests_to_steps) > 0:
        if len(ratio_precondition_by_tests_to_steps) < numberofMachinesAvailable:
            numberofMachinesAvailable = len(ratio_precondition_by_tests_to_steps)
            
        for _ in range(numberofMachinesAvailable):
            bestPrecondition = min(ratio_precondition_by_tests_to_steps, key=ratio_precondition_by_tests_to_steps.get)
            ratio_precondition_by_tests_to_steps.pop(bestPrecondition)
            executePrecondition(finalTestPlan, bestPrecondition, allTests)
            
            test_step_dependentTests = {}
            test_step_dependentSteps = {}
            for test in allTests:
                
                if bestPrecondition == test.preconditionDescription:
                    print(test)
                    # print(minSteps)
                    # while minSteps > 0:
                    test_step_dependentTests = calculateTestsByTestStep(test, test_step_dependentTests)
                    test_step_dependentSteps = calcualteStepsbyTestStep(test, test_step_dependentSteps)
                    ratio_steps_by_steps_to_test = calculateStepExecutionOrderbyTestStep(test_step_dependentTests, test_step_dependentSteps)
                    #     # bestTestStep = min(ratio_steps_by_steps_to_test, key=ratio_steps_b y_steps_to_test.get)
                    print(test_step_dependentSteps)
                    print(test_step_dependentTests)
                    print(ratio_steps_by_steps_to_test)
                        
                    #     # executeTestStep(finalTestPlan, bestTestStep, allTests, bestPrecondition)
                    #     # minSteps = allTestsObject.minRemainingStepCount

    finalTestPlan.writePlan('test_plan.txt')

if __name__ == "__main__":
    finalTestPlan = Plan()
    main(finalTestPlan)
    
"""

pop this precondition from the tests from the bottom of their step stacks and write to output in highest ration order

Why is Navigate to Analysis Output not in the output dicts?

"""