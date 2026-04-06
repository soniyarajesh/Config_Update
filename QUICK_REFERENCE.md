# Quick Reference Guide

## Commands

### Run Main Script
```bash
python main.py
```

### Run Usage Examples
```bash
python examples/usage_examples.py
```

### Run Individual Modules (Python REPL)
```python
# Import modules
from src.requirements.sws_parser import SWSParser
from src.testcases.test_generator import TestCaseGenerator
from src.arxml_config.arxml_updater import ARXMLUpdater

# Parse requirements
parser = SWSParser()
reqs = parser.parse_json_requirements('examples/sws_requirements/autosar_requirements.json')

# Generate test cases
gen = TestCaseGenerator()
tests = gen.generate_test_cases(reqs)
gen.save_test_cases_to_json('output.json')

# Create ARXML
updater = ARXMLUpdater()
updater.update_from_test_cases(tests)
updater.save_arxml('output.arxml')
```

## SWS Requirements JSON Schema

```json
{
  "requirements": [
    {
      "req_id": "string (required, unique)",
      "title": "string (required)",
      "description": "string (required)",
      "category": "string (optional, default: General)",
      "priority": "string (optional, default: Medium)",
      "dependencies": ["array of req_id strings (optional)"],
      "testable": "boolean (optional, default: true)"
    }
  ]
}
```

## Supported Categories

1. **Communication** - COM, CAN, LIN, FlexRay modules
   - Generates communication-specific test steps
   - Creates I-PDU configurations in ARXML

2. **Diagnostic** - DEM (Diagnostic Event Manager)
   - Generates diagnostic event test steps
   - Creates DTC (Diagnostic Trouble Code) configurations

3. **Memory** - NvM (Non-Volatile Memory)
   - Generates memory operation test steps
   - Creates memory block configurations

4. **Operating System** - AUTOSAR OS
   - Generates task/scheduling test steps
   - Creates OS configuration elements

5. **General** - Default for other modules
   - Generates generic test steps
   - Creates standard ARXML elements

## Priority Levels

- **Critical** - Must be tested first, highest priority
- **High** - Important functionality
- **Medium** - Standard functionality
- **Low** - Nice to have features

## Test Case Structure

Generated test cases include:
- `test_id`: Unique identifier (TC_[REQ_ID]_[SEQ])
- `name`: Descriptive name
- `description`: Full description
- `requirement_id`: Source requirement
- `preconditions`: List of preconditions
- `test_steps`: List of execution steps
- `expected_results`: List of expected outcomes
- `priority`: Test priority
- `category`: Test category
- `created_date`: ISO timestamp

## ARXML Structure

Generated ARXML follows AUTOSAR 4.x schema:

```xml
<AUTOSAR>
  <AR-PACKAGES>
    <AR-PACKAGE>
      <SHORT-NAME>Test_[Category]</SHORT-NAME>
      <ELEMENTS>
        <ECUC-CONTAINER-VALUE>
          <SHORT-NAME>[TestId]</SHORT-NAME>
          <PARAMETER-VALUES>
            <!-- Test parameters -->
          </PARAMETER-VALUES>
        </ECUC-CONTAINER-VALUE>
      </ELEMENTS>
    </AR-PACKAGE>
  </AR-PACKAGES>
</AUTOSAR>
```

## Filtering Examples

### By Priority
```python
generator = TestCaseGenerator()
test_cases = generator.generate_test_cases(requirements)

high_priority = generator.get_test_cases_by_priority('High')
critical = generator.get_test_cases_by_priority('Critical')
```

### By Category
```python
comm_tests = generator.get_test_cases_by_category('Communication')
diag_tests = generator.get_test_cases_by_category('Diagnostic')
```

### By Requirement ID
```python
parser = SWSParser()
parser.parse_json_requirements('requirements.json')
specific_req = parser.get_requirement_by_id('SWS_COM_001')
```

## Output Locations

| Output Type | Default Location |
|-------------|------------------|
| Test Cases JSON | `examples/testcases/generated_test_cases.json` |
| ARXML Config | `examples/arxml_files/test_configuration.arxml` |
| Custom Output | Specify path in method call |

## Common Workflows

### Workflow 1: Generate All Test Cases
1. Create/update `autosar_requirements.json`
2. Run `python main.py`
3. Review `examples/testcases/generated_test_cases.json`
4. Import `examples/arxml_files/test_configuration.arxml` to AUTOSAR tool

### Workflow 2: Filter Specific Tests
1. Parse requirements
2. Generate all test cases
3. Filter by category/priority
4. Export filtered subset
5. Use in targeted testing

### Workflow 3: Integrate with CI/CD
1. Store requirements in version control
2. Run generator in CI pipeline
3. Validate generated ARXML
4. Deploy to test environment
5. Execute test cases automatically

## Validation

### Requirements Validation
```python
parser = SWSParser()
parser.parse_json_requirements('requirements.json')
issues = parser.validate_requirements()

# Check for issues
if issues['missing_fields']:
    print("Missing fields:", issues['missing_fields'])
if issues['duplicate_ids']:
    print("Duplicate IDs:", issues['duplicate_ids'])
if issues['invalid_dependencies']:
    print("Invalid deps:", issues['invalid_dependencies'])
```

### ARXML Validation
```python
updater = ARXMLUpdater()
updater.update_from_test_cases(test_cases)
summary = updater.generate_config_summary()

print(f"Packages: {summary['packages']}")
print(f"Containers: {summary['containers']}")
print(f"Parameters: {summary['parameters']}")
```

## Tips & Best Practices

1. **Use meaningful requirement IDs**: Follow pattern `SWS_[MODULE]_[NUMBER]`
2. **Keep descriptions clear**: Write testable, specific descriptions
3. **Manage dependencies**: List all prerequisite requirements
4. **Categorize correctly**: Use appropriate AUTOSAR module categories
5. **Prioritize wisely**: Critical for safety-critical features
6. **Validate early**: Run validation after creating requirements
7. **Version control**: Track requirements and generated artifacts
8. **Review generated tests**: Verify test steps match intent
9. **Validate ARXML**: Use AUTOSAR tools to validate schema
10. **Iterate**: Refine requirements based on test results

## Troubleshooting

### Problem: Import errors
```bash
# Ensure running from project root
cd /path/to/Config_Update
python main.py
```

### Problem: File not found
```python
# Use absolute paths or ensure relative paths are correct
import os
base_dir = os.path.dirname(__file__)
req_path = os.path.join(base_dir, 'examples/sws_requirements/autosar_requirements.json')
```

### Problem: Invalid JSON
```bash
# Validate JSON syntax
python -m json.tool examples/sws_requirements/autosar_requirements.json
```

### Problem: XML validation fails
- Check AUTOSAR namespace declarations
- Verify element structure matches schema
- Use AUTOSAR-compliant XML validator

## API Reference

### SWSParser Methods
- `parse_json_requirements(file_path)` - Load requirements
- `get_testable_requirements()` - Filter testable
- `get_requirements_by_category(category)` - Filter by category
- `get_requirement_by_id(req_id)` - Get specific requirement
- `validate_requirements()` - Validate all requirements

### TestCaseGenerator Methods
- `generate_test_cases(requirements)` - Generate from list
- `generate_test_case_from_requirement(req)` - Generate single
- `save_test_cases_to_json(file_path)` - Export to JSON
- `get_test_cases_by_priority(priority)` - Filter by priority
- `get_test_cases_by_category(category)` - Filter by category

### ARXMLUpdater Methods
- `create_arxml_template()` - Create base structure
- `add_test_configuration(test_case)` - Add test config
- `update_from_test_cases(test_cases)` - Batch update
- `save_arxml(file_path)` - Export ARXML
- `load_arxml(file_path)` - Import ARXML
- `generate_config_summary()` - Get statistics
