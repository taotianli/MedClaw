#!/usr/bin/env python3
"""
Clinical Data Utilities for MedClaw
Provides helper functions for FHIR and HL7 message processing
"""

from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from fhir.resources.bundle import Bundle
from typing import Dict, List, Optional
import json
from datetime import datetime


def create_patient_resource(patient_data: Dict) -> Patient:
    """
    Create a FHIR Patient resource.

    Args:
        patient_data: Dictionary with patient information

    Returns:
        FHIR Patient resource
    """
    patient = Patient(**{
        "id": patient_data.get("id", "unknown"),
        "name": [{
            "use": "official",
            "family": patient_data.get("family_name", ""),
            "given": patient_data.get("given_names", [])
        }],
        "gender": patient_data.get("gender", "unknown"),
        "birthDate": patient_data.get("birth_date", "")
    })

    return patient


def parse_patient_resource(patient_json: str) -> Dict:
    """
    Parse FHIR Patient resource from JSON.

    Args:
        patient_json: JSON string of Patient resource

    Returns:
        Dictionary with extracted patient information
    """
    patient = Patient.parse_raw(patient_json)

    patient_info = {
        "id": patient.id,
        "gender": patient.gender,
        "birth_date": str(patient.birthDate) if patient.birthDate else None,
        "names": []
    }

    if patient.name:
        for name in patient.name:
            name_info = {
                "use": name.use,
                "family": name.family,
                "given": name.given
            }
            patient_info["names"].append(name_info)

    return patient_info


def create_observation_resource(observation_data: Dict) -> Observation:
    """
    Create a FHIR Observation resource.

    Args:
        observation_data: Dictionary with observation information

    Returns:
        FHIR Observation resource
    """
    observation = Observation(**{
        "id": observation_data.get("id", "unknown"),
        "status": observation_data.get("status", "final"),
        "code": {
            "coding": [{
                "system": observation_data.get("code_system", "http://loinc.org"),
                "code": observation_data.get("code", ""),
                "display": observation_data.get("code_display", "")
            }]
        },
        "subject": {
            "reference": observation_data.get("patient_reference", "")
        },
        "effectiveDateTime": observation_data.get("effective_date_time", datetime.now().isoformat())
    })

    # Add value if provided
    if "value_quantity" in observation_data:
        observation.valueQuantity = observation_data["value_quantity"]

    return observation


def parse_observation_resource(observation_json: str) -> Dict:
    """
    Parse FHIR Observation resource from JSON.

    Args:
        observation_json: JSON string of Observation resource

    Returns:
        Dictionary with extracted observation information
    """
    observation = Observation.parse_raw(observation_json)

    obs_info = {
        "id": observation.id,
        "status": observation.status,
        "effective_date_time": str(observation.effectiveDateTime) if observation.effectiveDateTime else None,
        "subject_reference": observation.subject.reference if observation.subject else None,
        "code": None,
        "value": None
    }

    # Extract code
    if observation.code and observation.code.coding:
        coding = observation.code.coding[0]
        obs_info["code"] = {
            "system": coding.system,
            "code": coding.code,
            "display": coding.display
        }

    # Extract value
    if observation.valueQuantity:
        obs_info["value"] = {
            "value": float(observation.valueQuantity.value),
            "unit": observation.valueQuantity.unit,
            "system": observation.valueQuantity.system
        }

    return obs_info


def parse_fhir_bundle(bundle_json: str) -> Dict:
    """
    Parse FHIR Bundle and extract resources.

    Args:
        bundle_json: JSON string of Bundle resource

    Returns:
        Dictionary with bundle information and resources
    """
    bundle = Bundle.parse_raw(bundle_json)

    bundle_info = {
        "type": bundle.type,
        "total": bundle.total,
        "resources": []
    }

    if bundle.entry:
        for entry in bundle.entry:
            if entry.resource:
                resource_info = {
                    "resource_type": entry.resource.resource_type,
                    "id": entry.resource.id
                }
                bundle_info["resources"].append(resource_info)

    return bundle_info


def anonymize_fhir_patient(patient: Patient) -> Patient:
    """
    Anonymize FHIR Patient resource by removing identifying information.

    Args:
        patient: FHIR Patient resource

    Returns:
        Anonymized Patient resource
    """
    # Remove names
    if patient.name:
        for name in patient.name:
            name.family = "ANONYMOUS"
            name.given = ["ANON"]

    # Remove identifiers
    patient.identifier = None

    # Remove contact information
    patient.telecom = None
    patient.address = None

    # Keep only essential clinical data
    # (gender, birthDate can be kept for clinical analysis)

    return patient


def extract_vital_signs(observations: List[Observation]) -> Dict:
    """
    Extract vital signs from list of Observation resources.

    Args:
        observations: List of FHIR Observation resources

    Returns:
        Dictionary of vital signs
    """
    vital_signs = {
        "blood_pressure_systolic": None,
        "blood_pressure_diastolic": None,
        "heart_rate": None,
        "respiratory_rate": None,
        "temperature": None,
        "oxygen_saturation": None
    }

    # Common LOINC codes for vital signs
    vital_sign_codes = {
        "8480-6": "blood_pressure_systolic",
        "8462-4": "blood_pressure_diastolic",
        "8867-4": "heart_rate",
        "9279-1": "respiratory_rate",
        "8310-5": "temperature",
        "2708-6": "oxygen_saturation"
    }

    for obs in observations:
        if obs.code and obs.code.coding:
            code = obs.code.coding[0].code
            if code in vital_sign_codes:
                key = vital_sign_codes[code]
                if obs.valueQuantity:
                    vital_signs[key] = {
                        "value": float(obs.valueQuantity.value),
                        "unit": obs.valueQuantity.unit,
                        "date": str(obs.effectiveDateTime) if obs.effectiveDateTime else None
                    }

    return vital_signs


def validate_fhir_resource(resource_json: str, resource_type: str) -> Dict:
    """
    Validate FHIR resource against schema.

    Args:
        resource_json: JSON string of FHIR resource
        resource_type: Type of resource (e.g., 'Patient', 'Observation')

    Returns:
        Dictionary with validation results
    """
    try:
        if resource_type == "Patient":
            Patient.parse_raw(resource_json)
        elif resource_type == "Observation":
            Observation.parse_raw(resource_json)
        elif resource_type == "Bundle":
            Bundle.parse_raw(resource_json)
        else:
            return {"valid": False, "error": f"Unknown resource type: {resource_type}"}

        return {"valid": True, "error": None}

    except Exception as e:
        return {"valid": False, "error": str(e)}


def convert_hl7_to_fhir_patient(hl7_message: str) -> Optional[Patient]:
    """
    Convert HL7 v2 PID segment to FHIR Patient resource.

    Note: This is a simplified conversion. Full HL7 parsing requires hl7apy.

    Args:
        hl7_message: HL7 v2 message string

    Returns:
        FHIR Patient resource or None
    """
    try:
        # This is a simplified example
        # In production, use hl7apy for proper parsing
        lines = hl7_message.split('\n')

        for line in lines:
            if line.startswith('PID'):
                fields = line.split('|')

                # Extract patient name (PID-5)
                if len(fields) > 5:
                    name_parts = fields[5].split('^')
                    family_name = name_parts[0] if len(name_parts) > 0 else ""
                    given_name = name_parts[1] if len(name_parts) > 1 else ""

                    patient = Patient(**{
                        "name": [{
                            "use": "official",
                            "family": family_name,
                            "given": [given_name]
                        }]
                    })

                    # Extract gender (PID-8)
                    if len(fields) > 8:
                        gender_map = {"M": "male", "F": "female", "O": "other", "U": "unknown"}
                        gender = gender_map.get(fields[8], "unknown")
                        patient.gender = gender

                    # Extract birth date (PID-7)
                    if len(fields) > 7 and fields[7]:
                        # HL7 date format: YYYYMMDD
                        birth_date = fields[7][:8]
                        if len(birth_date) == 8:
                            formatted_date = f"{birth_date[:4]}-{birth_date[4:6]}-{birth_date[6:8]}"
                            patient.birthDate = formatted_date

                    return patient

        return None

    except Exception as e:
        print(f"Error converting HL7 to FHIR: {e}")
        return None


if __name__ == "__main__":
    import sys

    # Example usage
    print("FHIR Clinical Data Utilities")
    print("=" * 50)

    # Create example patient
    patient_data = {
        "id": "patient-001",
        "family_name": "Doe",
        "given_names": ["John"],
        "gender": "male",
        "birth_date": "1980-01-01"
    }

    patient = create_patient_resource(patient_data)
    print("\nCreated Patient Resource:")
    print(patient.json(indent=2))

    # Create example observation
    observation_data = {
        "id": "obs-001",
        "status": "final",
        "code": "8867-4",
        "code_display": "Heart rate",
        "code_system": "http://loinc.org",
        "patient_reference": "Patient/patient-001",
        "value_quantity": {
            "value": 72,
            "unit": "beats/minute",
            "system": "http://unitsofmeasure.org",
            "code": "/min"
        }
    }

    observation = create_observation_resource(observation_data)
    print("\nCreated Observation Resource:")
    print(observation.json(indent=2))
