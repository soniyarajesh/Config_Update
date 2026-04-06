"""
Main orchestration script for AUTOSAR Test Case Generation and ARXML Configuration
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from requirements.sws_parser import SWSParser
from testcases.test_generator import TestCaseGenerator
from arxml_config.arxml_updater import ARXMLUpdater


def main():
    """Main execution function"""
    
    print("=" * 80)
    print("AUTOSAR SWS Test Case Generator and ARXML Configurator")
    print("=" * 80)
    print()
    
    # Step 1: Parse SWS Requirements
    print("Step 1: Parsing AUTOSAR SWS Requirements...")
    print("-" * 80)
    
    parser = SWSParser()
    requirements_file = 'examples/sws_requirements/autosar_requirements.json'
    
    if not os.path.exists(requirements_file):
        print(f"Error: Requirements file not found: {requirements_file}")
        return
    
    requirements = parser.parse_json_requirements(requirements_file)
    print(f"✓ Loaded {len(requirements)} requirements")
    
    # Validate requirements
    validation_issues = parser.validate_requirements()
    if any(validation_issues.values()):
        print("\nValidation Issues Found:")
        for issue_type, issues in validation_issues.items():
            if issues:
                print(f"  - {issue_type}: {issues}")
    else:
        print("✓ All requirements validated successfully")
    
    # Display requirements summary
    print(f"\nRequirements by Category:")
    categories = set(req.category for req in requirements)
    for category in sorted(categories):
        cat_reqs = parser.get_requirements_by_category(category)
        print(f"  - {category}: {len(cat_reqs)} requirements")
    
    testable_reqs = parser.get_testable_requirements()
    print(f"\nTestable Requirements: {len(testable_reqs)} out of {len(requirements)}")
    print()
    
    # Step 2: Generate Functional Test Cases
    print("Step 2: Generating Functional Test Cases...")
    print("-" * 80)
    
    generator = TestCaseGenerator()
    test_cases = generator.generate_test_cases(testable_reqs)
    print(f"✓ Generated {len(test_cases)} test cases")
    
    # Save test cases
    output_dir = 'examples/testcases'
    os.makedirs(output_dir, exist_ok=True)
    test_cases_file = os.path.join(output_dir, 'generated_test_cases.json')
    generator.save_test_cases_to_json(test_cases_file)
    print(f"✓ Test cases saved to: {test_cases_file}")
    
    # Display test cases summary
    print(f"\nTest Cases by Priority:")
    priorities = set(tc.priority for tc in test_cases)
    for priority in sorted(priorities):
        priority_tcs = generator.get_test_cases_by_priority(priority)
        print(f"  - {priority}: {len(priority_tcs)} test cases")
    
    print(f"\nTest Cases by Category:")
    for category in sorted(categories):
        cat_tcs = generator.get_test_cases_by_category(category)
        print(f"  - {category}: {len(cat_tcs)} test cases")
    print()
    
    # Step 3: Configure ARXML Updates
    print("Step 3: Configuring ARXML Files...")
    print("-" * 80)
    
    updater = ARXMLUpdater()
    updater.update_from_test_cases(test_cases)
    
    # Save ARXML
    arxml_output_dir = 'examples/arxml_files'
    os.makedirs(arxml_output_dir, exist_ok=True)
    arxml_file = os.path.join(arxml_output_dir, 'test_configuration.arxml')
    updater.save_arxml(arxml_file)
    print(f"✓ ARXML configuration saved to: {arxml_file}")
    
    # Display ARXML summary
    summary = updater.generate_config_summary()
    print(f"\nARXML Configuration Summary:")
    print(f"  - Packages: {summary['packages']}")
    print(f"  - Containers: {summary['containers']}")
    print(f"  - Parameters: {summary['parameters']}")
    print(f"  - Test Configurations: {len(summary['test_configurations'])}")
    print()
    
    # Final Summary
    print("=" * 80)
    print("Process Complete!")
    print("=" * 80)
    print(f"\nGenerated Files:")
    print(f"  1. Test Cases:  {test_cases_file}")
    print(f"  2. ARXML Config: {arxml_file}")
    print()
    print("Next Steps:")
    print("  - Review generated test cases")
    print("  - Validate ARXML configuration")
    print("  - Execute test cases in test environment")
    print("  - Integrate ARXML into AUTOSAR project")
    print()


if __name__ == '__main__':
    main()
