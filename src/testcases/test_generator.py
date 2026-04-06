"""
Functional Test Case Generator
This module generates functional test cases based on AUTOSAR SWS requirements.
"""

import json
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from requirements.sws_parser import SWSRequirement


@dataclass
class TestCase:
    """Represents a functional test case"""
    test_id: str
    name: str
    description: str
    requirement_id: str
    preconditions: List[str]
    test_steps: List[str]
    expected_results: List[str]
    priority: str
    category: str
    created_date: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert test case to dictionary"""
        return asdict(self)


class TestCaseGenerator:
    """Generator for functional test cases from SWS requirements"""
    
    def __init__(self):
        self.test_cases: List[TestCase] = []
        self.test_counter = 0
    
    def generate_test_case_from_requirement(self, requirement: SWSRequirement) -> TestCase:
        """
        Generate a functional test case from a SWS requirement
        
        Args:
            requirement: SWSRequirement object
            
        Returns:
            TestCase object
        """
        self.test_counter += 1
        test_id = f"TC_{requirement.req_id}_{self.test_counter:03d}"
        
        # Generate test steps based on requirement description
        test_steps = self._generate_test_steps(requirement)
        expected_results = self._generate_expected_results(requirement)
        preconditions = self._generate_preconditions(requirement)
        
        test_case = TestCase(
            test_id=test_id,
            name=f"Test for {requirement.title}",
            description=f"Functional test case to verify: {requirement.description}",
            requirement_id=requirement.req_id,
            preconditions=preconditions,
            test_steps=test_steps,
            expected_results=expected_results,
            priority=requirement.priority,
            category=requirement.category,
            created_date=datetime.now().isoformat()
        )
        
        return test_case
    
    def _generate_test_steps(self, requirement: SWSRequirement) -> List[str]:
        """Generate test steps based on requirement"""
        category = requirement.category.lower()
        
        if 'communication' in category:
            return [
                "Initialize the communication module",
                "Configure communication parameters as per specification",
                "Send test message through the configured channel",
                "Verify message transmission",
                "Check for acknowledgment"
            ]
        elif 'diagnostic' in category:
            return [
                "Initialize diagnostic module",
                "Trigger diagnostic event",
                "Read diagnostic trouble code (DTC)",
                "Verify DTC storage",
                "Clear DTC and verify"
            ]
        elif 'memory' in category:
            return [
                "Initialize memory module",
                "Write test data to memory",
                "Read back data from memory",
                "Verify data integrity",
                "Perform memory cleanup"
            ]
        else:
            return [
                "Initialize the module under test",
                "Configure module parameters",
                "Execute the functionality",
                "Verify the output",
                "Cleanup and reset"
            ]
    
    def _generate_expected_results(self, requirement: SWSRequirement) -> List[str]:
        """Generate expected results based on requirement"""
        category = requirement.category.lower()
        
        if 'communication' in category:
            return [
                "Module initializes successfully",
                "Configuration is applied correctly",
                "Message is transmitted without errors",
                "Acknowledgment is received",
                "No errors reported"
            ]
        elif 'diagnostic' in category:
            return [
                "Diagnostic module initializes successfully",
                "Diagnostic event is captured",
                "Correct DTC is stored",
                "DTC can be read successfully",
                "DTC is cleared properly"
            ]
        elif 'memory' in category:
            return [
                "Memory module initializes successfully",
                "Data is written correctly",
                "Read data matches written data",
                "Data integrity is maintained",
                "Memory is cleaned up successfully"
            ]
        else:
            return [
                "Module initializes without errors",
                "Parameters are set correctly",
                "Functionality executes as expected",
                "Output meets specification requirements",
                "System returns to stable state"
            ]
    
    def _generate_preconditions(self, requirement: SWSRequirement) -> List[str]:
        """Generate preconditions based on requirement"""
        preconditions = [
            "AUTOSAR software stack is properly configured",
            "All required modules are initialized",
            "System is in a stable state"
        ]
        
        if requirement.dependencies:
            for dep in requirement.dependencies:
                preconditions.append(f"Requirement {dep} is satisfied")
        
        return preconditions
    
    def generate_test_cases(self, requirements: List[SWSRequirement]) -> List[TestCase]:
        """
        Generate test cases for multiple requirements
        
        Args:
            requirements: List of SWSRequirement objects
            
        Returns:
            List of TestCase objects
        """
        test_cases = []
        for req in requirements:
            if req.testable:
                test_case = self.generate_test_case_from_requirement(req)
                test_cases.append(test_case)
        
        self.test_cases = test_cases
        return test_cases
    
    def save_test_cases_to_json(self, output_file: str):
        """
        Save generated test cases to a JSON file
        
        Args:
            output_file: Path to output JSON file
        """
        test_cases_dict = {
            'test_suite': {
                'name': 'AUTOSAR SWS Functional Tests',
                'created_date': datetime.now().isoformat(),
                'total_tests': len(self.test_cases)
            },
            'test_cases': [tc.to_dict() for tc in self.test_cases]
        }
        
        with open(output_file, 'w') as f:
            json.dump(test_cases_dict, f, indent=2)
    
    def get_test_cases_by_priority(self, priority: str) -> List[TestCase]:
        """Get test cases filtered by priority"""
        return [tc for tc in self.test_cases if tc.priority == priority]
    
    def get_test_cases_by_category(self, category: str) -> List[TestCase]:
        """Get test cases filtered by category"""
        return [tc for tc in self.test_cases if tc.category == category]
