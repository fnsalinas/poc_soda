# Manual de configuración de Contratos de Datos

**Creado por**: Fabio Salinas  
**Fecha de Creación**: 2024-07-31  
**Contacto**: fabio.salinas@hdi.com.co  

----------

## Pasos

### Clonado de repositorio

1. Clonar el repositorio desde github:
    ```bash
    git clone https://github.com/fnsalinas/poc_soda.git;
    ```  
2. Navegar hasta la carpeta del repositorio clonado
    ```bash
    cd poc_soda;
    ```  

### Creación de ambiente virtual

1. Instalar virtualenv
    ```bash
    pip install virtualenv
    ```  
2. Crear ambiente virtual con el nombre **soda**
    ```bash
    python -m venv soda
    ```  
3. Activar el ambiente virtual
    ```bash
    source env/bin/activate
    ```  

### Instalación de paquetes

Los paquetes a instalar son:
    - requests
    - pandas
    - psycopg2-binary
    - soda-core==3.2.1
    - soda-core-contracts==3.2.1
    - soda-core-postgres==3.2.1
    - python-dotenv
    - pyyaml
    - soda-core-redshift
   
1. Crear el archivo de requirements:
    ```bash
    cat >requirements_prod.txt <<EOL
    requests==2.31.0
    pandas==1.5.3
    psycopg2-binary==2.9.9
    soda-core==3.2.1
    soda-core-contracts==3.2.1
    soda-core-postgres==3.2.1
    python-dotenv==1.0.1
    pyyaml==6.0.1
    soda-core-redshift==3.2.1
    EOL
    ```
2. Instalar paquetes
    ```bash
    pip install -r requirements_prod.txt
    ```

### Crear archivo de conexiones

1. Crear el archivo de secretos de redshift, verificar que la ruta /mnt/N1662770/PRIVATE exista o reemplazarla por una existente que no se encuentra accesible desde un repositorio de git.
    ```bash
    cat >/mnt/N1662770/PRIVATE/soda_secret.yml <<EOL
    data_source adp:
      type: redshift
      host: HOST DE LA CONEXIÓN A REDSHIFT
      port: PUERTO DE LA CONEXIÓN A REDSHIFT
      username: NOMBRE DE USUARIO
      password: CONTRASEÑA
      database: BASE DE DATOS
      schema: ESQUEMA DE DATOS
    EOL
    ```

### Crear variables de entorno

1. Crear archivo .env y cargar variables de entorno
    ```bash
    cat >.env <<EOL
    APP_MAIN_PATH=/mnt/N1662770/poc_soda
    DATA_CONTRACTS_PATH=contracts
    POSTGRESQL_CONNECTION_YML_PATH=/mnt/N1662770/PRIVATE/soda_secret.yml
    EOL
    ```
    
    - Se debe cambiar /mnt/N1662770/poc_soda por la ruta de la instalación de la aplicación
    - Se debe cambiar /mnt/N1662770/PRIVATE/soda_secret.yml por la ruta donde se guarda el archivo de conexiones.

### Script de python

1. Importar pajquetes
    ```python
    from soda.contracts.data_contract_translator import DataContractTranslator
    from soda.scan import Scan
    import logging
    from dotenv import load_dotenv
    import os
    import yaml
    import pandas as pd
    import json
    ```
2. Cargar variables de entorno
    ```python
    load_dotenv()
    app_main_path=os.environ["APP_MAIN_PATH"]
    datacontracts_path=os.environ["DATA_CONTRACTS_PATH"]
    postgresql_conn_path=os.environ["POSTGRESQL_CONNECTION_YML_PATH"]
    ```
3. Proceso completo para obtener resultados del contrato de datos
    ```python
    # Cargar contrato de datos en string Importante cambiar la ruta de dc_path hacia el contrato de datos correcto
    dc_path=f"{app_main_path}/{datacontracts_path}/03_vw_dim_lob.yml"
    with open(dc_path) as infile:
        data_contract_yaml_str: str = infile.read()

    # Traduce e interpreta el string del contrato de datos en el formato estandar de SodaCL
    data_contract_parser = DataContractTranslator()
    sodacl_yaml_str = data_contract_parser.translate_data_contract_yaml_str(data_contract_yaml_str)

    # Ejecuta el contrato de datos en la conexión definida previemante en el postgresql_conn_path
    scan = Scan()
    scan.set_data_source_name("adp") # Importante cambiar el datasource_name a uno que exista en el postgresql_conn_path
    scan.add_configuration_yaml_file(file_path=postgresql_conn_path)
    scan.add_sodacl_yaml_str(sodacl_yaml_str)

    # Ejecuta el escaneo definido en el contrato de datos
    scan.execute()

    # Guarda los resultados completos del escaneo en un diccionario
    scan_results = scan.build_scan_results()

    # Guarda una lista con los fallos resultadfo del escaneo
    fail_list = scan.get_checks_fail()

    # Guarda en formato de texto los resultados de la ejecución del contrato de datos
    scan_results_string = scan.get_all_checks_text()
    
    ```



