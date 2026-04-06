"""
Example: Using the AUTOSAR Test Generator programmatically
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from requirements.sws_parser import SWSParser, SWSRequirement
from testcases.test_generator import TestCaseGenerator
from arxml_config.arxml_updater import ARXMLUpdater


def example_1_parse_requirements():
    """Example 1: Parse and validate requirements"""
    print("\n" + "="*60)
    print("Example 1: Parse and Validate Requirements")
    print("="*60)
    
    parser = SWSParser()
    requirements = parser.parse_json_requirements(
        'examples/sws_requirements/autosar_requirements.json'
    )
    
    print(f"\nTotal requirements loaded: {len(requirements)}")
    
    # Get testable requirements
    testable = parser.get_testable_requirements()
    print(f"Testable requirements: {len(testable)}")
    
    # Get requirements by category
    comm_reqs = parser.get_requirements_by_category('Communication')
    print(f"Communication requirements: {len(comm_reqs)}")
    
    # Validate
    issues = parser.validate_requirements()
    print(f"\nValidation complete - Issues found: {any(issues.values())}")


def example_2_generate_test_cases():
    """Example 2: Generate test cases"""
    print("\n" + "="*60)
    print("Example 2: Generate Test Cases")
    print("="*60)
    
    parser = SWSParser()
    requirements = parser.parse_json_requirements(
        'examples/sws_requirements/autosar_requirements.json'
    )
    
    generator = TestCaseGenerator()
    test_cases = generator.generate_test_cases(requirements)
    
    print(f"\nGenerated {len(test_cases)} test cases")
    
    # Show first test case
    if test_cases:
        tc = test_cases[0]
        print(f"\nSample Test Case:")
        print(f"  ID: {tc.test_id}")
        print(f"  Name: {tc.name}")
        print(f"  Priority: {tc.priority}")
        print(f"  Steps: {len(tc.test_steps)}")
    
    # Get high priority test cases
    high_priority = generator.get_test_cases_by_priority('High')
    print(f"\nHigh priority test cases: {len(high_priority)}")


def example_3_update_arxml():
    """Example 3: Update ARXML configuration"""
    print("\n" + "="*60)
    print("Example 3: Update ARXML Configuration")
    print("="*60)
    
    # Parse requirements
    parser = SWSParser()
    requirements = parser.parse_json_requirements(
        'examples/sws_requirements/autosar_requirements.json'
    )
    
    # Generate test cases
    generator = TestCaseGenerator()
    test_cases = generator.generate_test_cases(requirements)
    
    # Update ARXML
    updater = ARXMLUpdater()
    updater.update_from_test_cases(test_cases)
    
    # Get summary
    summary = updater.generate_config_summary()
    print(f"\nARXML Configuration Summary:")
    print(f"  Packages: {summary['packages']}")
    print(f"  Containers: {summary['containers']}")
    print(f"  Parameters: {summary['parameters']}")
    print(f"  Test Configurations: {len(summary['test_configurations'])}")


def example_4_custom_requirements():
    """Example 4: Create and use custom requirements"""
    print("\n" + "="*60)
    print("Example 4: Custom Requirements")
    print("="*60)
    
    # Create custom requirements
    custom_req = SWSRequirement(
        req_id='SWS_CUSTOM_001',
        title='Custom Test Requirement',
        description='This is a custom requirement for demonstration',
        category='General',
        priority='Medium',
        dependencies=[],
        testable=True
    )
    
    print(f"\nCreated custom requirement: {custom_req.req_id}")
    
    # Generate test case from custom requirement
    generator = TestCaseGenerator()
    test_case = generator.generate_test_case_from_requirement(custom_req)
    
    print(f"Generated test case: {test_case.test_id}")
    print(f"Test steps: {len(test_case.test_steps)}")


def example_5_filter_and_export():
    """Example 5: Filter and export specific test cases"""
    print("\n" + "="*60)
    print("Example 5: Filter and Export Test Cases")
    print("="*60)
    
    parser = SWSParser()
    requirements = parser.parse_json_requirements(
        'examples/sws_requirements/autosar_requirements.json'
    )
    
    generator = TestCaseGenerator()
    test_cases = generator.generate_test_cases(requirements)
    
    # Filter communication test cases
    comm_tests = generator.get_test_cases_by_category('Communication')
    print(f"\nCommunication test cases: {len(comm_tests)}")
    
    # Filter critical priority
    critical_tests = generator.get_test_cases_by_priority('Critical')
    print(f"Critical test cases: {len(critical_tests)}")
    
    # Export filtered test cases
    if not os.path.exists('/tmp/filtered_tests'):
        os.makedirs('/tmp/filtered_tests')
    
    # Save communication tests
    generator.test_cases = comm_tests
    generator.save_test_cases_to_json('/tmp/filtered_tests/comm_tests.json')
    print(f"\nExported communication tests to: /tmp/filtered_tests/comm_tests.json")


if __name__ == '__main__':
    print("\n" + "#"*60)
    print("# AUTOSAR Test Generator - Usage Examples")
    print("#"*60)
    
    example_1_parse_requirements()
    example_2_generate_test_cases()
    example_3_update_arxml()
    example_4_custom_requirements()
    example_5_filter_and_export()
    
    print("\n" + "#"*60)
    print("# All examples completed successfully!")
    print("#"*60)
    print()
