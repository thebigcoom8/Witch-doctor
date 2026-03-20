import json
import logging
from typing import Dict, List, Any, Optional


class DataValidator:
    """
    Validates scraped data against expected schemas.
    Ensures data consistency and quality before cleaning/processing.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.errors = []
        self.warnings = []
        
        # Define expected schemas for each scraper
        self.schemas = {
            "tripsit": self._get_tripsit_schema(),
            "pubchem": self._get_pubchem_schema(),
            "medlineplus": self._get_medlineplus_schema(),
            "nida": self._get_nida_schema(),
            "diy_hrt": self._get_diy_hrt_schema(),
        }

    def validate_all_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate all scraped data."""
        self.logger.info("Starting data validation...")
        self.errors = []
        self.warnings = []
        
        validation_results = {}
        
        for scraper_name, scraper_data in data.items():
            if scraper_name in self.schemas:
                validation_results[scraper_name] = self.validate_scraper_data(
                    scraper_name, scraper_data
                )
            else:
                self.logger.warning(f"Unknown scraper: {scraper_name}")
        
        return {
            "results": validation_results,
            "errors": self.errors,
            "warnings": self.warnings,
            "valid": len(self.errors) == 0,
        }

    def validate_scraper_data(self, scraper_name: str, data: Any) -> Dict[str, Any]:
        """Validate data from a specific scraper."""
        self.logger.info(f"Validating {scraper_name} data...")
        
        if scraper_name not in self.schemas:
            error = f"Unknown scraper: {scraper_name}"
            self.errors.append(error)
            return {"valid": False, "error": error}
        
        schema = self.schemas[scraper_name]
        return self._validate_against_schema(scraper_name, data, schema)

    def _validate_against_schema(self, scraper_name: str, data: Any, schema: Dict) -> Dict[str, Any]:
        """Validate data against a schema."""
        results = {
            "valid": True,
            "scraper": scraper_name,
            "checks": {},
        }
        
        try:
            # Check if data is dict
            if not isinstance(data, dict):
                error = f"{scraper_name}: Expected dict, got {type(data)}"
                self.errors.append(error)
                results["valid"] = False
                return results
            
            # Check required fields
            for field in schema.get("required", []):
                if field not in data:
                    error = f"{scraper_name}: Missing required field '{field}'"
                    self.errors.append(error)
                    results["valid"] = False
                results["checks"][f"required_{field}"] = field in data
            
            # Validate field types
            for field, expected_type in schema.get("types", {}).items():
                if field in data:
                    if not isinstance(data[field], expected_type):
                        warning = f"{scraper_name}: Field '{field}' type mismatch (expected {expected_type.__name__}, got {type(data[field]).__name__})"
                        self.warnings.append(warning)
                    results["checks"][f"type_{field}"] = isinstance(data[field], expected_type)
            
            # Custom validators
            for check_name, check_func in schema.get("validators", {}).items():
                try:
                    passed = check_func(data)
                    results["checks"][check_name] = passed
                    if not passed:
                        warning = f"{scraper_name}: Validation check '{check_name}' failed"
                        self.warnings.append(warning)
                except Exception as e:
                    error = f"{scraper_name}: Validation check '{check_name}' raised exception: {e}"
                    self.errors.append(error)
                    results["valid"] = False
            
            # Check for empty data
            if len(data) == 0:
                warning = f"{scraper_name}: Empty data"
                self.warnings.append(warning)
                results["checks"]["empty"] = False
            else:
                results["checks"]["empty"] = True
            
            self.logger.info(f"Validation complete for {scraper_name}: valid={results['valid']}")
            return results
            
        except Exception as e:
            error = f"{scraper_name}: Unexpected validation error: {e}"
            self.errors.append(error)
            results["valid"] = False
            return results

    def _get_tripsit_schema(self) -> Dict:
        """Schema for TripSit scraper data."""
        return {
            "required": ["drugs", "interactions"],
            "types": {
                "drugs": list,
                "interactions": list,
            },
            "validators": {
                "has_drugs": lambda d: isinstance(d.get("drugs"), list) and len(d.get("drugs", [])) > 0,
                "drug_structure": lambda d: self._validate_drug_structure(d.get("drugs", [])),
            },
        }

    def _get_pubchem_schema(self) -> Dict:
        """Schema for PubChem scraper data."""
        return {
            "required": ["compounds"],
            "types": {
                "compounds": list,
            },
            "validators": {
                "has_compounds": lambda d: isinstance(d.get("compounds"), list),
                "compound_structure": lambda d: self._validate_compound_structure(d.get("compounds", [])),
            },
        }

    def _get_medlineplus_schema(self) -> Dict:
        """Schema for MedlinePlus scraper data."""
        return {
            "required": ["medications"],
            "types": {
                "medications": list,
                "interactions": list,
            },
            "validators": {
                "has_medications": lambda d: isinstance(d.get("medications"), list),
                "medication_structure": lambda d: self._validate_medication_structure(d.get("medications", [])),
            },
        }

    def _get_nida_schema(self) -> Dict:
        """Schema for NIDA scraper data."""
        return {
            "required": ["substances"],
            "types": {
                "substances": list,
                "research": list,
            },
            "validators": {
                "has_substances": lambda d: isinstance(d.get("substances"), list),
                "substance_structure": lambda d: self._validate_substance_structure(d.get("substances", [])),
            },
        }

    def _get_diy_hrt_schema(self) -> Dict:
        """Schema for DIY HRT scraper data."""
        return {
            "required": ["medications", "protocols"],
            "types": {
                "medications": list,
                "protocols": list,
                "resources": list,
            },
            "validators": {
                "has_medications": lambda d: isinstance(d.get("medications"), list),
                "has_protocols": lambda d: isinstance(d.get("protocols"), list),
            },
        }

    def _validate_drug_structure(self, drugs: List[Dict]) -> bool:
        """Validate structure of drug entries."""
        try:
            required_fields = {"name", "aliases", "categories"}
            for drug in drugs:
                if not isinstance(drug, dict):
                    return False
                if not required_fields.issubset(set(drug.keys())):
                    return False
            return True
        except:
            return False

    def _validate_compound_structure(self, compounds: List[Dict]) -> bool:
        """Validate structure of compound entries."""
        try:
            required_fields = {"cid", "molecular_weight", "iupac_name"}
            for compound in compounds:
                if not isinstance(compound, dict):
                    return False
                if not any(field in compound for field in required_fields):
                    return False
            return True
        except:
            return False

    def _validate_medication_structure(self, medications: List[Dict]) -> bool:
        """Validate structure of medication entries."""
        try:
            for med in medications:
                if not isinstance(med, dict):
                    return False
                if "name" not in med:
                    return False
            return True
        except:
            return False

    def _validate_substance_structure(self, substances: List[Dict]) -> bool:
        """Validate structure of substance entries."""
        try:
            for substance in substances:
                if not isinstance(substance, dict):
                    return False
                if "name" not in substance:
                    return False
            return True
        except:
            return False

    def report(self) -> str:
        """Generate validation report."""
        report = []
        report.append("\n" + "="*50)
        report.append("DATA VALIDATION REPORT")
        report.append("="*50)
        
        if self.errors:
            report.append(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                report.append(f"  - {error}")
        
        if self.warnings:
            report.append(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                report.append(f"  - {warning}")
        
        if not self.errors and not self.warnings:
            report.append("\n✅ All validation checks passed!")
        
        report.append("="*50 + "\n")
        return "\n".join(report)

    def save_report(self, filepath: str) -> bool:
        """Save validation report to file."""
        try:
            with open(filepath, 'w') as f:
                f.write(self.report())
            self.logger.info(f"Saved validation report to {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving report: {e}")
            return False
