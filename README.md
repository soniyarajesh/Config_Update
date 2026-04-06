# AUTOSAR Config_Update

A comprehensive tool for understanding AUTOSAR SWS (Software Specification) requirements, generating functional test cases, and configuring ARXML updates based on those test cases.

## Overview

This project provides an automated workflow for:
1. **Parsing AUTOSAR SWS Requirements** - Read and validate software specification requirements
2. **Generating Functional Test Cases** - Automatically create test cases from requirements
3. **Configuring ARXML Files** - Update AUTOSAR XML configuration files based on test cases

## Features

- ✅ Parse SWS requirements from JSON format
- ✅ Validate requirements for completeness and dependencies
- ✅ Generate functional test cases automatically
- ✅ Create category-specific test steps (Communication, Diagnostic, Memory, OS)
- ✅ Generate ARXML configuration files compliant with AUTOSAR 4.x
- ✅ Support for multiple AUTOSAR modules (COM, DEM, NvM, OS, CAN)
- ✅ Comprehensive reporting and summaries

## Project Structure

```
Config_Update/
├── src/
│   ├── requirements/
│   │   ├── __init__.py
│   │   └── sws_parser.py          # SWS requirements parser
│   ├── testcases/
│   │   ├── __init__.py
│   │   └── test_generator.py       # Test case generator
│   └── arxml_config/
│       ├── __init__.py
│       └── arxml_updater.py        # ARXML configuration updater
├── examples/
│   ├── sws_requirements/
│   │   └── autosar_requirements.json  # Sample requirements
│   ├── testcases/                     # Generated test cases (output)
│   └── arxml_files/                   # Generated ARXML files (output)
├── tests/                             # Unit tests
├── main.py                            # Main orchestration script
└── README.md
```

## Installation

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses standard library only)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/soniyarajesh/Config_Update.git
cd Config_Update
```

2. Verify Python installation:
```bash
python --version
```

## Usage

### Quick Start

Run the main script to process the example requirements:

```bash
python main.py
```

This will:
1. Parse requirements from `examples/sws_requirements/autosar_requirements.json`
2. Generate test cases and save to `examples/testcases/generated_test_cases.json`
3. Create ARXML configuration in `examples/arxml_files/test_configuration.arxml`

### Using Individual Modules

#### 1. Parse SWS Requirements

```python
from src.requirements.sws_parser import SWSParser

parser = SWSParser()
requirements = parser.parse_json_requirements('path/to/requirements.json')

# Get testable requirements only
testable = parser.get_testable_requirements()

# Validate requirements
issues = parser.validate_requirements()
```

#### 2. Generate Test Cases

```python
from src.testcases.test_generator import TestCaseGenerator

generator = TestCaseGenerator()
test_cases = generator.generate_test_cases(requirements)

# Save to JSON
generator.save_test_cases_to_json('output/test_cases.json')

# Filter by priority
high_priority = generator.get_test_cases_by_priority('High')
```

#### 3. Update ARXML Configuration

```python
from src.arxml_config.arxml_updater import ARXMLUpdater

updater = ARXMLUpdater()
updater.update_from_test_cases(test_cases)

# Save ARXML file
updater.save_arxml('output/configuration.arxml')

# Get summary
summary = updater.generate_config_summary()
```

## Requirements Format

Requirements should be defined in JSON format:

```json
{
  "requirements": [
    {
      "req_id": "SWS_COM_001",
      "title": "Communication Stack Initialization",
      "description": "The communication stack shall be initialized...",
      "category": "Communication",
      "priority": "High",
      "dependencies": [],
      "testable": true
    }
  ]
}
```

### Supported Categories

- Communication (COM, CAN, etc.)
- Diagnostic (DEM)
- Memory (NvM)
- Operating System (OS)
- General (default)

### Priority Levels

- Critical
- High
- Medium
- Low

## Output Files

### Test Cases JSON

Generated test cases include:
- Test ID and name
- Description and requirement mapping
- Preconditions
- Test steps
- Expected results
- Priority and category
- Creation timestamp

### ARXML Configuration

Generated ARXML files follow AUTOSAR 4.x schema with:
- Proper namespace declarations
- AR-PACKAGES structure
- ECUC containers for test configurations
- Parameter definitions
- Category-specific configurations (I-PDU, DTC, etc.)

## Example Workflow

1. **Define Requirements**: Create or update `autosar_requirements.json` with your SWS requirements
2. **Run Generator**: Execute `python main.py` to generate test cases and ARXML
3. **Review Output**: Check generated files in `examples/testcases/` and `examples/arxml_files/`
4. **Integrate**: Import ARXML into your AUTOSAR toolchain
5. **Execute Tests**: Use generated test cases in your test framework

## Validation

The tool includes validation for:
- ✅ Missing required fields in requirements
- ✅ Invalid dependency references
- ✅ Duplicate requirement IDs
- ✅ ARXML schema compliance

## Extending the Tool

### Adding New Categories

To add support for a new AUTOSAR module category:

1. Add category-specific test step generation in `test_generator.py`
2. Add category-specific ARXML configuration in `arxml_updater.py`
3. Update the example requirements with new category examples

### Custom Test Step Templates

Modify `_generate_test_steps()` in `TestCaseGenerator` to add custom test patterns for your modules.

## Troubleshooting

### Common Issues

**Issue**: Module import errors
**Solution**: Ensure you're running from the project root directory

**Issue**: File not found errors
**Solution**: Check that example files exist in `examples/sws_requirements/`

**Issue**: XML parsing errors
**Solution**: Validate generated ARXML with an AUTOSAR-compliant XML validator

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is provided as-is for AUTOSAR development purposes.

## Contact

For questions or support, please open an issue on GitHub.

## Acknowledgments

- AUTOSAR specifications and standards
- AUTOSAR XML schema definitions
