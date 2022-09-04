from test import AllTestSteps, AllTests, TestSteps, TestStep, Test
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
             writeFile.writelines(self.stepExecutionOrder)
        
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
    
    allTestSteps = AllTestSteps('test_steps.csv')
    allTests = AllTests('tests.csv').allTests
    allTestStepsStore = allTestSteps.test_steps_store
    allTestStepStore = allTestSteps.test_step_store
    allTestPreconditions = allTestSteps.test_preconditions

    stepCollection = {}
    for count, (key, value) in enumerate(allTestStepStore.items(), start=1): 
        print(f"{count} = {key}:{value}")
        stepCollection[count] = value
        
    for count, (key, value) in enumerate(allTestStepsStore.items(), start=1):
        values = ", \n".join(item.asString() for item in value.asList())
        print(f'{count} = {key}:{values}')

    # for precondition in allTestPreconditions:
    #     print(precondition.TestStepID)

    
    for test in allTests:
        try:
            test.TestSteps = allTestStepsStore[test.TestStepID.strip()]
            # print(test.TestSteps)
            test.TestStepIDs = [testStep.TestStepID for testStep in test.TestSteps.asList()]
            # print(test.TestStepIDs)
            # test.printSteps()
        except Exception:
            print(f'{test} didnt work')
            
    finalTestPlan.writePlan('final_test_plan.txt')

if __name__ == "__main__":
    finalTestPlan = Plan()
    main(finalTestPlan)