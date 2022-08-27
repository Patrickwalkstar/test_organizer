from test import AllTestSteps, AllTests, TestSteps, TestStep, Test
from rich import print

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
        # test.printSteps()
    except Exception:
        print(f'{test} didnt work')
        
        
