"""
AUTOSAR SWS Requirements Parser
This module handles parsing and understanding of AUTOSAR Software Specification (SWS) requirements.
"""

import json
import re
from typing import List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class SWSRequirement:
    """Represents a single SWS requirement"""
    req_id: str
    title: str
    description: str
    category: str
    priority: str
    dependencies: List[str]
    testable: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert requirement to dictionary"""
        return asdict(self)


class SWSParser:
    """Parser for AUTOSAR SWS requirements"""
    
    def __init__(self):
        self.requirements: List[SWSRequirement] = []
    
    def parse_json_requirements(self, json_file_path: str) -> List[SWSRequirement]:
        """
        Parse SWS requirements from a JSON file
        
        Args:
            json_file_path: Path to the JSON file containing SWS requirements
            
        Returns:
            List of SWSRequirement objects
        """
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        requirements = []
        for req_data in data.get('requirements', []):
            req = SWSRequirement(
                req_id=req_data.get('req_id', ''),
                title=req_data.get('title', ''),
                description=req_data.get('description', ''),
                category=req_data.get('category', 'General'),
                priority=req_data.get('priority', 'Medium'),
                dependencies=req_data.get('dependencies', []),
                testable=req_data.get('testable', True)
            )
            requirements.append(req)
        
        self.requirements = requirements
        return requirements
    
    def get_testable_requirements(self) -> List[SWSRequirement]:
        """
        Filter and return only testable requirements
        
        Returns:
            List of testable SWSRequirement objects
        """
        return [req for req in self.requirements if req.testable]
    
    def get_requirements_by_category(self, category: str) -> List[SWSRequirement]:
        """
        Get requirements filtered by category
        
        Args:
            category: Category to filter by
            
        Returns:
            List of SWSRequirement objects in the specified category
        """
        return [req for req in self.requirements if req.category == category]
    
    def get_requirement_by_id(self, req_id: str) -> SWSRequirement:
        """
        Get a specific requirement by ID
        
        Args:
            req_id: Requirement ID to search for
            
        Returns:
            SWSRequirement object or None if not found
        """
        for req in self.requirements:
            if req.req_id == req_id:
                return req
        return None
    
    def validate_requirements(self) -> Dict[str, List[str]]:
        """
        Validate requirements for completeness and consistency
        
        Returns:
            Dictionary with validation results
        """
        issues = {
            'missing_fields': [],
            'invalid_dependencies': [],
            'duplicate_ids': []
        }
        
        req_ids = set()
        for req in self.requirements:
            # Check for duplicate IDs
            if req.req_id in req_ids:
                issues['duplicate_ids'].append(req.req_id)
            req_ids.add(req.req_id)
            
            # Check for missing fields
            if not req.req_id or not req.title or not req.description:
                issues['missing_fields'].append(req.req_id)
            
            # Check for invalid dependencies
            for dep in req.dependencies:
                if dep not in req_ids:
                    issues['invalid_dependencies'].append(
                        f"{req.req_id} depends on non-existent {dep}"
                    )
        
        return issues
