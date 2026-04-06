"""
ARXML Configuration Updater
This module updates AUTOSAR ARXML configuration files based on test cases.
"""

import xml.etree.ElementTree as ET
from typing import List, Dict, Any
import json
from testcases.test_generator import TestCase


class ARXMLUpdater:
    """Updates ARXML configuration files based on test case requirements"""
    
    # AUTOSAR namespace
    AUTOSAR_NS = {
        'ar': 'http://autosar.org/schema/r4.0',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }
    
    def __init__(self):
        self.tree = None
        self.root = None
    
    def create_arxml_template(self) -> ET.Element:
        """
        Create a basic ARXML template structure
        
        Returns:
            Root element of the ARXML structure
        """
        # Create root element with namespace
        root = ET.Element('AUTOSAR', {
            'xmlns': self.AUTOSAR_NS['ar'],
            'xmlns:xsi': self.AUTOSAR_NS['xsi'],
            'xsi:schemaLocation': 'http://autosar.org/schema/r4.0 AUTOSAR_4-2-2.xsd'
        })
        
        # Add AR-PACKAGES element
        ar_packages = ET.SubElement(root, 'AR-PACKAGES')
        
        self.root = root
        return root
    
    def add_test_configuration(self, test_case: TestCase, parent=None):
        """
        Add test configuration to ARXML based on test case
        
        Args:
            test_case: TestCase object containing test information
            parent: Parent XML element (optional)
        """
        if self.root is None:
            self.create_arxml_template()
        
        if parent is None:
            # Find or create AR-PACKAGES
            ar_packages = self.root.find('.//AR-PACKAGES')
            if ar_packages is None:
                ar_packages = ET.SubElement(self.root, 'AR-PACKAGES')
            parent = ar_packages
        
        # Create AR-PACKAGE for test category
        ar_package = ET.SubElement(parent, 'AR-PACKAGE')
        short_name = ET.SubElement(ar_package, 'SHORT-NAME')
        short_name.text = f"Test_{test_case.category.replace(' ', '_')}"
        
        # Add elements
        elements = ET.SubElement(ar_package, 'ELEMENTS')
        
        # Create test configuration container
        container_def = ET.SubElement(elements, 'ECUC-CONTAINER-VALUE')
        
        # Short name for container
        container_name = ET.SubElement(container_def, 'SHORT-NAME')
        container_name.text = test_case.test_id
        
        # Add definition reference
        definition_ref = ET.SubElement(container_def, 'DEFINITION-REF')
        definition_ref.set('DEST', 'ECUC-PARAM-CONF-CONTAINER-DEF')
        definition_ref.text = f"/AUTOSAR/TestConfig/{test_case.category}"
        
        # Add parameter values
        param_values = ET.SubElement(container_def, 'PARAMETER-VALUES')
        
        # Add test ID parameter
        self._add_parameter(param_values, 'TestId', test_case.test_id)
        self._add_parameter(param_values, 'TestName', test_case.name)
        self._add_parameter(param_values, 'RequirementId', test_case.requirement_id)
        self._add_parameter(param_values, 'Priority', test_case.priority)
        self._add_parameter(param_values, 'Category', test_case.category)
    
    def _add_parameter(self, parent, param_name: str, param_value: str):
        """Add a parameter to the ARXML configuration"""
        param = ET.SubElement(parent, 'ECUC-TEXTUAL-PARAM-VALUE')
        
        short_name = ET.SubElement(param, 'SHORT-NAME')
        short_name.text = param_name
        
        definition_ref = ET.SubElement(param, 'DEFINITION-REF')
        definition_ref.set('DEST', 'ECUC-STRING-PARAM-DEF')
        definition_ref.text = f"/AUTOSAR/TestConfig/Parameters/{param_name}"
        
        value = ET.SubElement(param, 'VALUE')
        value.text = str(param_value)
    
    def add_communication_config(self, test_case: TestCase):
        """Add communication-specific configuration"""
        if 'communication' in test_case.category.lower():
            if self.root is None:
                self.create_arxml_template()
            
            ar_packages = self.root.find('.//AR-PACKAGES')
            if ar_packages is None:
                ar_packages = ET.SubElement(self.root, 'AR-PACKAGES')
            
            # Create communication package
            comm_package = ET.SubElement(ar_packages, 'AR-PACKAGE')
            short_name = ET.SubElement(comm_package, 'SHORT-NAME')
            short_name.text = 'CommunicationConfig'
            
            elements = ET.SubElement(comm_package, 'ELEMENTS')
            
            # Add I-PDU configuration
            ipdu = ET.SubElement(elements, 'I-PDU')
            ipdu_name = ET.SubElement(ipdu, 'SHORT-NAME')
            ipdu_name.text = f"IPDU_{test_case.test_id}"
            
            length = ET.SubElement(ipdu, 'LENGTH')
            length.text = '8'
    
    def add_diagnostic_config(self, test_case: TestCase):
        """Add diagnostic-specific configuration"""
        if 'diagnostic' in test_case.category.lower():
            if self.root is None:
                self.create_arxml_template()
            
            ar_packages = self.root.find('.//AR-PACKAGES')
            if ar_packages is None:
                ar_packages = ET.SubElement(self.root, 'AR-PACKAGES')
            
            # Create diagnostic package
            diag_package = ET.SubElement(ar_packages, 'AR-PACKAGE')
            short_name = ET.SubElement(diag_package, 'SHORT-NAME')
            short_name.text = 'DiagnosticConfig'
            
            elements = ET.SubElement(diag_package, 'ELEMENTS')
            
            # Add DTC configuration
            dtc = ET.SubElement(elements, 'DIAGNOSTIC-TROUBLE-CODE')
            dtc_name = ET.SubElement(dtc, 'SHORT-NAME')
            dtc_name.text = f"DTC_{test_case.test_id}"
            
            dtc_number = ET.SubElement(dtc, 'TROUBLE-CODE')
            dtc_number.text = '0x000001'
    
    def update_from_test_cases(self, test_cases: List[TestCase]):
        """
        Update ARXML configuration based on multiple test cases
        
        Args:
            test_cases: List of TestCase objects
        """
        self.create_arxml_template()
        
        for test_case in test_cases:
            self.add_test_configuration(test_case)
            
            # Add category-specific configurations
            if 'communication' in test_case.category.lower():
                self.add_communication_config(test_case)
            elif 'diagnostic' in test_case.category.lower():
                self.add_diagnostic_config(test_case)
    
    def save_arxml(self, output_file: str):
        """
        Save ARXML configuration to file
        
        Args:
            output_file: Path to output ARXML file
        """
        if self.root is None:
            raise ValueError("No ARXML structure to save. Create or load ARXML first.")
        
        # Create tree and format
        tree = ET.ElementTree(self.root)
        ET.indent(tree, space='  ')
        
        # Write to file with XML declaration
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
    
    def load_arxml(self, input_file: str):
        """
        Load existing ARXML file
        
        Args:
            input_file: Path to input ARXML file
        """
        self.tree = ET.parse(input_file)
        self.root = self.tree.getroot()
    
    def generate_config_summary(self) -> Dict[str, Any]:
        """
        Generate a summary of the ARXML configuration
        
        Returns:
            Dictionary with configuration summary
        """
        if self.root is None:
            return {'error': 'No ARXML loaded'}
        
        summary = {
            'packages': 0,
            'containers': 0,
            'parameters': 0,
            'test_configurations': []
        }
        
        # Count packages
        packages = self.root.findall('.//AR-PACKAGE')
        summary['packages'] = len(packages)
        
        # Count containers
        containers = self.root.findall('.//ECUC-CONTAINER-VALUE')
        summary['containers'] = len(containers)
        
        # Count parameters
        parameters = self.root.findall('.//ECUC-TEXTUAL-PARAM-VALUE')
        summary['parameters'] = len(parameters)
        
        # Extract test configurations
        for container in containers:
            name_elem = container.find('SHORT-NAME')
            if name_elem is not None and name_elem.text:
                summary['test_configurations'].append(name_elem.text)
        
        return summary
