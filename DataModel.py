import pandas as pd

# Define the data schema
miabis_schema = {
    'biobank_id': 'int',
    'biobank_name': 'str',
    'biobank_acronym': 'str',
    'biobank_description': 'str',
    'biobank_url': 'str',
    'country': 'str',
    'juristic_person': 'str',
    'biobank_contact': 'str',
    'biobank_contact_email': 'str',
    'biobank_contact_phone': 'str',
    'biobank_contact_address': 'str',
    'biobank_contact_zip': 'str',
    'biobank_contact_city': 'str',
    'biobank_contact_country': 'str',
    'biobank_contact_state': 'str',
    'biobank_contact_fax': 'str',
    'biobank_contact_web': 'str',
    'biobank_contact_notes': 'str'
}

sprec_schema = {
    'sample_id': 'int',
    'sample_type': 'str',
    'sprec_code': 'str',
    'collection_type': 'str',
    'pre_ct': 'str',
    'post_ct': 'str',
    'storage_temp': 'str',
    'biobank_id': 'int'  # Foreign key to MIABIS
}

omop_person_schema = {
    'person_id': 'int',
    'gender_concept_id': 'int',
    'year_of_birth': 'int',
    'month_of_birth': 'int',
    'day_of_birth': 'int',
    'birth_datetime': 'str',
    'race_concept_id': 'int',
    'ethnicity_concept_id': 'int',
    'location_id': 'int',
    'provider_id': 'int',
    'care_site_id': 'int',
    'person_source_value': 'str',
    'gender_source_value': 'str',
    'gender_source_concept_id': 'int',
    'race_source_value': 'str',
    'race_source_concept_id': 'int',
    'ethnicity_source_value': 'str',
    'ethnicity_source_concept_id': 'int'
}

condition_occurrence_schema = {
    'condition_occurrence_id': 'int',
    'person_id': 'int',  # Foreign key to OMOP Person
    'condition_concept_id': 'int',
    'condition_start_date': 'str',
    'condition_start_datetime': 'str',
    'condition_end_date': 'str',
    'condition_end_datetime': 'str',
    'condition_type_concept_id': 'int',
    'stop_reason': 'str',
    'provider_id': 'int',
    'visit_occurrence_id': 'int',
    'condition_source_value': 'str',
    'condition_source_concept_id': 'int',
    'condition_status_source_value': 'str',
    'condition_status_concept_id': 'int'
}

procedure_occurrence_schema = {
    'procedure_occurrence_id': 'int',
    'person_id': 'int',  # Foreign key to OMOP Person
    'procedure_concept_id': 'int',
    'procedure_date': 'str',
    'procedure_datetime': 'str',
    'procedure_type_concept_id': 'int',
    'modifier_concept_id': 'int',
    'quantity': 'int',
    'provider_id': 'int',
    'visit_occurrence_id': 'int',
    'procedure_source_value': 'str',
    'procedure_source_concept_id': 'int',
    'qualifier_source_value': 'str'
}

# Example of creating DataFrames with the defined schema
miabis_df = pd.DataFrame(columns=miabis_schema.keys()).astype(miabis_schema)
sprec_df = pd.DataFrame(columns=sprec_schema.keys()).astype(sprec_schema)
omop_person_df = pd.DataFrame(columns=omop_person_schema.keys()).astype(omop_person_schema)
condition_occurrence_df = pd.DataFrame(columns=condition_occurrence_schema.keys()).astype(condition_occurrence_schema)
procedure_occurrence_df = pd.DataFrame(columns=procedure_occurrence_schema.keys()).astype(procedure_occurrence_schema)