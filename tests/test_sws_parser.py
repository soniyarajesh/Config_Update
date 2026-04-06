"""
Unit tests for SWS Parser
"""

import unittest
import json
import tempfile
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from requirements.sws_parser import SWSParser, SWSRequirement


class TestSWSParser(unittest.TestCase):
    """Test cases for SWSParser class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.parser = SWSParser()
        
        # Create temporary test requirements file
        self.test_requirements = {
            "requirements": [
                {
                    "req_id": "SWS_TEST_001",
                    "title": "Test Requirement 1",
                    "description": "Test description 1",
                    "category": "Communication",
                    "priority": "High",
                    "dependencies": [],
                    "testable": True
                },
                {
                    "req_id": "SWS_TEST_002",
                    "title": "Test Requirement 2",
                    "description": "Test description 2",
                    "category": "Diagnostic",
                    "priority": "Medium",
                    "dependencies": ["SWS_TEST_001"],
                    "testable": True
                },
                {
                    "req_id": "SWS_TEST_003",
                    "title": "Test Requirement 3",
                    "description": "Test description 3",
                    "category": "Communication",
                    "priority": "Low",
                    "dependencies": [],
                    "testable": False
                }
            ]
        }
        
        # Create temporary file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump(self.test_requirements, self.temp_file)
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_parse_json_requirements(self):
        """Test parsing requirements from JSON file"""
        requirements = self.parser.parse_json_requirements(self.temp_file.name)
        
        self.assertEqual(len(requirements), 3)
        self.assertIsInstance(requirements[0], SWSRequirement)
        self.assertEqual(requirements[0].req_id, "SWS_TEST_001")
    
    def test_get_testable_requirements(self):
        """Test filtering testable requirements"""
        self.parser.parse_json_requirements(self.temp_file.name)
        testable = self.parser.get_testable_requirements()
        
        self.assertEqual(len(testable), 2)
        for req in testable:
            self.assertTrue(req.testable)
    
    def test_get_requirements_by_category(self):
        """Test filtering requirements by category"""
        self.parser.parse_json_requirements(self.temp_file.name)
        comm_reqs = self.parser.get_requirements_by_category('Communication')
        
        self.assertEqual(len(comm_reqs), 2)
        for req in comm_reqs:
            self.assertEqual(req.category, 'Communication')
    
    def test_get_requirement_by_id(self):
        """Test getting requirement by ID"""
        self.parser.parse_json_requirements(self.temp_file.name)
        req = self.parser.get_requirement_by_id('SWS_TEST_001')
        
        self.assertIsNotNone(req)
        self.assertEqual(req.req_id, 'SWS_TEST_001')
        self.assertEqual(req.title, 'Test Requirement 1')
    
    def test_get_requirement_by_invalid_id(self):
        """Test getting requirement with invalid ID"""
        self.parser.parse_json_requirements(self.temp_file.name)
        req = self.parser.get_requirement_by_id('INVALID_ID')
        
        self.assertIsNone(req)
    
    def test_validate_requirements_success(self):
        """Test validation of valid requirements"""
        self.parser.parse_json_requirements(self.temp_file.name)
        issues = self.parser.validate_requirements()
        
        self.assertEqual(len(issues['missing_fields']), 0)
        self.assertEqual(len(issues['duplicate_ids']), 0)
        self.assertEqual(len(issues['invalid_dependencies']), 0)
    
    def test_validate_duplicate_ids(self):
        """Test validation detects duplicate IDs"""
        duplicate_reqs = {
            "requirements": [
                {
                    "req_id": "SWS_DUP_001",
                    "title": "Test 1",
                    "description": "Description 1",
                    "category": "General",
                    "priority": "High",
                    "dependencies": [],
                    "testable": True
                },
                {
                    "req_id": "SWS_DUP_001",
                    "title": "Test 2",
                    "description": "Description 2",
                    "category": "General",
                    "priority": "High",
                    "dependencies": [],
                    "testable": True
                }
            ]
        }
        
        temp_dup_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump(duplicate_reqs, temp_dup_file)
        temp_dup_file.close()
        
        try:
            self.parser.parse_json_requirements(temp_dup_file.name)
            issues = self.parser.validate_requirements()
            
            self.assertGreater(len(issues['duplicate_ids']), 0)
        finally:
            os.unlink(temp_dup_file.name)
    
    def test_sws_requirement_to_dict(self):
        """Test converting SWSRequirement to dictionary"""
        req = SWSRequirement(
            req_id='TEST_001',
            title='Test',
            description='Test description',
            category='General',
            priority='High',
            dependencies=[],
            testable=True
        )
        
        req_dict = req.to_dict()
        
        self.assertIsInstance(req_dict, dict)
        self.assertEqual(req_dict['req_id'], 'TEST_001')
        self.assertEqual(req_dict['title'], 'Test')


if __name__ == '__main__':
    unittest.main()
