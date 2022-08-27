from test import AllTestSteps, AllTests, TestSteps, TestStep, Test
from rich import print



class Plan: 
    def __init__(self) -> None:
        self.stepExecutionOrder = []
        
allTestSteps = AllTestSteps('test_steps.csv')
allTestStepsStore = allTestSteps.test_steps_store
allTestStepStore = allTestSteps.test_step_store
allTestPreconditions = allTestSteps.test_preconditions

stepCollection = {}
for count, (key, value) in enumerate(allTestStepStore.items(), start=1): 
    print(f"{count} = {key}:{value}")
    stepCollection[count] = value
    
    
for count, (key, value) in enumerate(allTestStepsStore.items(), start=1):
    print(f"{count} = {key}:{value}")

for precondition in allTestPreconditions:
    print(precondition.TestStepID)

    
    
allTests = AllTests('tests.csv').allTests
for test in allTests:
    try:

        test.TestSteps = allTestStepsStore[test.TestStepID.strip()]
        # print(test.TestSteps)
        test.TestStepIDs = [testStep.TestStepID for testStep in test.TestSteps.asList()]
        # print(test.TestStepIDs)
        test.printSteps()
    except Exception:
        print(f'{test} didnt work')
        
        


def main():
    finalTestPlan = Plan()
    
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
    
   
    
    pass

if __name__ == "__main__":
    main()