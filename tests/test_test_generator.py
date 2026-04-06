"""
Unit tests for Test Generator
"""

import unittest
import json
import tempfile
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from requirements.sws_parser import SWSRequirement
from testcases.test_generator import TestCaseGenerator, TestCase


class TestTestCaseGenerator(unittest.TestCase):
    """Test cases for TestCaseGenerator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = TestCaseGenerator()
        
        # Create sample requirements
        self.comm_req = SWSRequirement(
            req_id='SWS_COM_001',
            title='Communication Test',
            description='Test communication module',
            category='Communication',
            priority='High',
            dependencies=[],
            testable=True
        )
        
        self.diag_req = SWSRequirement(
            req_id='SWS_DEM_001',
            title='Diagnostic Test',
            description='Test diagnostic module',
            category='Diagnostic',
            priority='Medium',
            dependencies=['SWS_COM_001'],
            testable=True
        )
        
        self.non_testable_req = SWSRequirement(
            req_id='SWS_DOC_001',
            title='Documentation Requirement',
            description='Update documentation',
            category='Documentation',
            priority='Low',
            dependencies=[],
            testable=False
        )
    
    def test_generate_test_case_from_requirement(self):
        """Test generating a single test case"""
        test_case = self.generator.generate_test_case_from_requirement(self.comm_req)
        
        self.assertIsInstance(test_case, TestCase)
        self.assertTrue(test_case.test_id.startswith('TC_SWS_COM_001'))
        self.assertEqual(test_case.requirement_id, 'SWS_COM_001')
        self.assertEqual(test_case.priority, 'High')
        self.assertEqual(test_case.category, 'Communication')
    
    def test_generate_test_cases(self):
        """Test generating multiple test cases"""
        requirements = [self.comm_req, self.diag_req, self.non_testable_req]
        test_cases = self.generator.generate_test_cases(requirements)
        
        # Should only generate for testable requirements
        self.assertEqual(len(test_cases), 2)
        
        for tc in test_cases:
            self.assertIsInstance(tc, TestCase)
            self.assertGreater(len(tc.test_steps), 0)
            self.assertGreater(len(tc.expected_results), 0)
    
    def test_communication_test_steps(self):
        """Test communication-specific test step generation"""
        test_case = self.generator.generate_test_case_from_requirement(self.comm_req)
        
        self.assertIn('communication', ' '.join(test_case.test_steps).lower())
        self.assertIn('message', ' '.join(test_case.test_steps).lower())
    
    def test_diagnostic_test_steps(self):
        """Test diagnostic-specific test step generation"""
        test_case = self.generator.generate_test_case_from_requirement(self.diag_req)
        
        steps_text = ' '.join(test_case.test_steps).lower()
        self.assertIn('diagnostic', steps_text)
    
    def test_preconditions_with_dependencies(self):
        """Test precondition generation with dependencies"""
        test_case = self.generator.generate_test_case_from_requirement(self.diag_req)
        
        preconditions_text = ' '.join(test_case.preconditions)
        self.assertIn('SWS_COM_001', preconditions_text)
    
    def test_save_test_cases_to_json(self):
        """Test saving test cases to JSON file"""
        requirements = [self.comm_req, self.diag_req]
        self.generator.generate_test_cases(requirements)
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        temp_file.close()
        
        try:
            self.generator.save_test_cases_to_json(temp_file.name)
            
            # Verify file was created and has valid JSON
            self.assertTrue(os.path.exists(temp_file.name))
            
            with open(temp_file.name, 'r') as f:
                data = json.load(f)
            
            self.assertIn('test_suite', data)
            self.assertIn('test_cases', data)
            self.assertEqual(len(data['test_cases']), 2)
        finally:
            os.unlink(temp_file.name)
    
    def test_get_test_cases_by_priority(self):
        """Test filtering test cases by priority"""
        requirements = [self.comm_req, self.diag_req]
        self.generator.generate_test_cases(requirements)
        
        high_priority = self.generator.get_test_cases_by_priority('High')
        medium_priority = self.generator.get_test_cases_by_priority('Medium')
        
        self.assertEqual(len(high_priority), 1)
        self.assertEqual(len(medium_priority), 1)
        self.assertEqual(high_priority[0].priority, 'High')
    
    def test_get_test_cases_by_category(self):
        """Test filtering test cases by category"""
        requirements = [self.comm_req, self.diag_req]
        self.generator.generate_test_cases(requirements)
        
        comm_tests = self.generator.get_test_cases_by_category('Communication')
        diag_tests = self.generator.get_test_cases_by_category('Diagnostic')
        
        self.assertEqual(len(comm_tests), 1)
        self.assertEqual(len(diag_tests), 1)
        self.assertEqual(comm_tests[0].category, 'Communication')
    
    def test_test_case_to_dict(self):
        """Test converting TestCase to dictionary"""
        test_case = self.generator.generate_test_case_from_requirement(self.comm_req)
        tc_dict = test_case.to_dict()
        
        self.assertIsInstance(tc_dict, dict)
        self.assertEqual(tc_dict['requirement_id'], 'SWS_COM_001')
        self.assertIn('test_steps', tc_dict)
        self.assertIn('expected_results', tc_dict)


if __name__ == '__main__':
    unittest.main()
