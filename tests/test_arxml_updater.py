"""
Unit tests for ARXML Updater
"""

import unittest
import tempfile
import os
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from testcases.test_generator import TestCase
from arxml_config.arxml_updater import ARXMLUpdater


class TestARXMLUpdater(unittest.TestCase):
    """Test cases for ARXMLUpdater class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.updater = ARXMLUpdater()
        
        # Create sample test cases
        self.comm_test = TestCase(
            test_id='TC_COM_001',
            name='Communication Test',
            description='Test communication',
            requirement_id='SWS_COM_001',
            preconditions=['System initialized'],
            test_steps=['Step 1', 'Step 2'],
            expected_results=['Result 1', 'Result 2'],
            priority='High',
            category='Communication',
            created_date='2026-04-06T00:00:00'
        )
        
        self.diag_test = TestCase(
            test_id='TC_DEM_001',
            name='Diagnostic Test',
            description='Test diagnostic',
            requirement_id='SWS_DEM_001',
            preconditions=['System initialized'],
            test_steps=['Step 1', 'Step 2'],
            expected_results=['Result 1', 'Result 2'],
            priority='Medium',
            category='Diagnostic',
            created_date='2026-04-06T00:00:00'
        )
    
    def test_create_arxml_template(self):
        """Test creating ARXML template structure"""
        root = self.updater.create_arxml_template()
        
        self.assertIsNotNone(root)
        self.assertEqual(root.tag, 'AUTOSAR')
        
        # Check for AR-PACKAGES
        ar_packages = root.find('.//AR-PACKAGES')
        self.assertIsNotNone(ar_packages)
    
    def test_add_test_configuration(self):
        """Test adding test configuration to ARXML"""
        self.updater.create_arxml_template()
        self.updater.add_test_configuration(self.comm_test)
        
        # Verify configuration was added
        container = self.updater.root.find('.//ECUC-CONTAINER-VALUE')
        self.assertIsNotNone(container)
        
        short_name = container.find('SHORT-NAME')
        self.assertEqual(short_name.text, 'TC_COM_001')
    
    def test_add_communication_config(self):
        """Test adding communication-specific configuration"""
        self.updater.add_communication_config(self.comm_test)
        
        # Check for I-PDU element
        ipdu = self.updater.root.find('.//I-PDU')
        self.assertIsNotNone(ipdu)
        
        ipdu_name = ipdu.find('SHORT-NAME')
        self.assertIn('TC_COM_001', ipdu_name.text)
    
    def test_add_diagnostic_config(self):
        """Test adding diagnostic-specific configuration"""
        self.updater.add_diagnostic_config(self.diag_test)
        
        # Check for DTC element
        dtc = self.updater.root.find('.//DIAGNOSTIC-TROUBLE-CODE')
        self.assertIsNotNone(dtc)
        
        dtc_name = dtc.find('SHORT-NAME')
        self.assertIn('TC_DEM_001', dtc_name.text)
    
    def test_update_from_test_cases(self):
        """Test updating ARXML from multiple test cases"""
        test_cases = [self.comm_test, self.diag_test]
        self.updater.update_from_test_cases(test_cases)
        
        # Verify multiple configurations were added
        containers = self.updater.root.findall('.//ECUC-CONTAINER-VALUE')
        self.assertEqual(len(containers), 2)
    
    def test_save_arxml(self):
        """Test saving ARXML to file"""
        self.updater.create_arxml_template()
        self.updater.add_test_configuration(self.comm_test)
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.arxml')
        temp_file.close()
        
        try:
            self.updater.save_arxml(temp_file.name)
            
            # Verify file was created
            self.assertTrue(os.path.exists(temp_file.name))
            
            # Verify it's valid XML
            tree = ET.parse(temp_file.name)
            root = tree.getroot()
            self.assertIn('AUTOSAR', root.tag)
        finally:
            os.unlink(temp_file.name)
    
    def test_load_arxml(self):
        """Test loading existing ARXML file"""
        # Create and save ARXML
        self.updater.create_arxml_template()
        self.updater.add_test_configuration(self.comm_test)
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.arxml')
        temp_file.close()
        
        try:
            self.updater.save_arxml(temp_file.name)
            
            # Load it in new updater
            new_updater = ARXMLUpdater()
            new_updater.load_arxml(temp_file.name)
            
            self.assertIsNotNone(new_updater.root)
            self.assertIn('AUTOSAR', new_updater.root.tag)
        finally:
            os.unlink(temp_file.name)
    
    def test_generate_config_summary(self):
        """Test generating configuration summary"""
        test_cases = [self.comm_test, self.diag_test]
        self.updater.update_from_test_cases(test_cases)
        
        summary = self.updater.generate_config_summary()
        
        self.assertIn('packages', summary)
        self.assertIn('containers', summary)
        self.assertIn('parameters', summary)
        self.assertIn('test_configurations', summary)
        
        self.assertGreater(summary['packages'], 0)
        self.assertGreater(summary['containers'], 0)
    
    def test_save_without_arxml_raises_error(self):
        """Test saving without creating ARXML structure raises error"""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.arxml')
        temp_file.close()
        
        try:
            with self.assertRaises(ValueError):
                self.updater.save_arxml(temp_file.name)
        finally:
            os.unlink(temp_file.name)
    
    def test_arxml_namespace(self):
        """Test ARXML has correct namespace"""
        root = self.updater.create_arxml_template()
        
        # Check for AUTOSAR namespace
        self.assertIn('http://autosar.org/schema/r4.0', root.attrib.values())


if __name__ == '__main__':
    unittest.main()
