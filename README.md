# poc_soda

# Repositorio de soda-core:
Link a repositorio de: [soda-core](https://github.com/sodadata/soda-core)


# Tips Importantes:

### 1. Archivo de Configuración de Fuentes de Datos
En la carpeta de instalación de soda-core (~/.soda) se debe depositar el archivo ***configuration.yml*** con la configuración de las fuentes de datos a utilizar. Este archivo debe tener la siguiente estructura:

En caso de postgresql:
```yaml
data_source my_datasource_name:
  type: postgres
  host: db
  port: "5432"
  username: soda
  password: secret
  database: postgres
  schema: public
```

Para ver más opciónes de configuración de fuentes de datos, ver la documentación de soda-core en el siguiente [link](https://docs.soda.io/soda/connect-athena.html)

### 2. Otra opción de configuración de fuentes de datos:
En caso de que se desee utilizar un archivo de configuración de fuentes de datos diferente al ***configuration.yml***, se puede especificar el archivo de configuración con el siguiente comando:
```python
from soda.contracts.data_contract_translator import DataContractTranslator
from soda.scan import Scan

RUTA_DEL_ARCHIVO_DE_CONFIGURACION = "ruta/del/archivo/de/configuracion.yml"
RUTA_DEL_ARCHIVO_DE_CONTRATO_DE_DATOS = "ruta/del/archivo/de/contrato_de_datos.yml"

# Leer el archivo de contrato de datos
with open(dc_path) as infile:
    data_contract_yaml_str: str = infile.read()

# Traducir el archivo de contrato de datos a un objeto que pueda ser interpretado por soda-core
data_contract_parser = DataContractTranslator()
sodacl_yaml_str = data_contract_parser.translate_data_contract_yaml_str(data_contract_yaml_str)

# Crear un objeto de tipo Scan para escanear los datos
scan = Scan()
scan.set_data_source_name("hdi")
scan.add_configuration_yaml_file(file_path=RUTA_DEL_ARCHIVO_DE_CONFIGURACION)
scan.add_sodacl_yaml_str(sodacl_yaml_str)
scan.execute()

# Obtener los resultados del escaneo
scan.get_all_checks_text()
```

### 3. Ejemplos de contratos de datos
En este vinculo: [Ejemplos de contratos de datos](https://docs.soda.io/soda/data-contracts.html) se pueden encontrar ejemplos de contratos de datos para diferentes tipos de fuentes de datos.