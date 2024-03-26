
from soda.contracts.data_contract_translator import DataContractTranslator
from soda.scan import Scan
import logging
from dotenv import load_dotenv
import os
import yaml
import pandas as pd
import json

load_dotenv()

app_main_path=os.environ["APP_MAIN_PATH"]
datacontracts_path=os.environ["DATA_CONTRACTS_PATH"]
postgresql_conn_path=os.environ["POSTGRESQL_CONNECTION_YML_PATH"]

# Read the data contract file as a Python str
dc_path=f"{app_main_path}/{datacontracts_path}/02_sise_generales_tsuc.yml"
with open(dc_path) as infile:
    data_contract_yaml_str: str = infile.read()

print(data_contract_yaml_str)

# Translate the data contract standards into SodaCL
data_contract_parser = DataContractTranslator()
sodacl_yaml_str = data_contract_parser.translate_data_contract_yaml_str(data_contract_yaml_str)

# Log or save the SodaCL checks file to help with debugging  
logging.debug(sodacl_yaml_str)
print(sodacl_yaml_str)

# Execute the translated SodaCL checks in a scan
scan = Scan()
scan.set_data_source_name("hdi")
scan.add_configuration_yaml_file(file_path=postgresql_conn_path)
scan.add_sodacl_yaml_str(sodacl_yaml_str)
scan.execute()
scan.assert_no_checks_fail()
scan.get_checks_fail()[0].get_dict()

scan.build_scan_results()
results = scan.build_scan_results()
scan.get_all_checks_text()
scan.get_checks_fail()
