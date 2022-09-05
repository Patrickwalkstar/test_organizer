from test import AllTestSteps, AllTests, LinkedList, TestSteps, TestStep, Test, mergeLists
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
    
    
    for test in allTests:
        try:
            test.TestSteps = allTestStepsStore[test.TestStepID.strip()]
            test.TestSteps.SWTCNumber = test.SWTCNumber
            # print(test.TestSteps)
            test.TestStepIDs = [testStep.TestStepID for testStep in test.TestSteps.asList()]
            # print(test.TestStepIDs)
            # test.printSteps()
        except Exception:
            print(f'{test} didnt work')
            
            
    # for test in allTests: 
    #     print(test.TestSteps.printList())
    
    
    current_list = allTests[0].TestSteps.head
    for test in allTests[1:]: 
        next_list = test.TestSteps.head
        common_list = mergeLists(current_list, next_list)
        current_list = common_list
        
        
    new_linked_list = LinkedList()
    new_linked_list.head = current_list
    new_linked_list.printList()

    finalTestPlan.writePlan('final_test_plan.txt')

if __name__ == "__main__":
    finalTestPlan = Plan()
    main(finalTestPlan)
    
    