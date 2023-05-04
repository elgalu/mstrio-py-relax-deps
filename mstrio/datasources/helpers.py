from enum import auto
from mstrio.utils.enum_helper import AutoName, AutoCapitalizedName


class DBType(AutoName):
    """Enumeration representing database type."""

    RESERVED = auto()
    ACCESS = auto()
    ALTIBASE = auto()
    AMAZON_ATHENA = auto()
    AMAZON_AURORA = auto()
    AMAZON_DOCUMENT_DB = auto()
    AMAZON_DYNAMO_DB = auto()
    AMAZON_REDSHIFT = auto()
    ARCADIA_PLATFORM = auto()
    ASTER = auto()
    AZURE_COSMOS = auto()
    BIG_DATA_ENGINE = auto()
    CASSANDRA = auto()
    CIRRO = auto()
    CLOUD_ELEMENT = auto()
    CLOUD_GATEWAY = auto()
    CLOUD_GATEWAY_AWS_S3 = auto()
    CLOUD_GATEWAY_AZURE_ADLS_2 = auto()
    CLOUD_GATEWAY_GOOGLE_CLOUD_STORAGE = auto()
    COMPOSITE = auto()
    CONCUR = auto()
    CONNECTION_CLOUD = auto()
    DATABRICKS = auto()
    DATA_DIRECT_CLOUD = auto()
    DATALLEGRO = auto()
    DB2 = auto()
    DENODO = auto()
    DREMIO = auto()
    DRILL = auto()
    DROPBOX = auto()
    DRUID = auto()
    ELASTICSEARCH = auto()
    ELOQUA = auto()
    ENTERPRISE_DB = auto()
    ESS_BASE = auto()
    EXA_SOLUTION = auto()
    EXCEL = auto()
    FACEBOOK = auto()
    FINANCIALFORCE = auto()
    GBASE_8A = auto()
    GENERIC = auto()
    GENERIC_DATA_CONNECTOR = auto()
    GITHUB = auto()
    GOOGLE_ANALYTICS = auto()
    GOOGLE_BIG_QUERY = auto()
    GOOGLE_BIG_QUERY_FF_SQL = auto()
    GOOGLE_CLOUD_SPANNER = auto()
    GOOGLE_DRIVE = auto()
    HIVE = auto()
    HIVE_THRIFT = auto()
    HUBSPOT = auto()
    IBM_IPS = auto()
    IMPALA = auto()
    INFORMATICA = auto()
    INFORMIX = auto()
    JIRA = auto()
    KAFKA = auto()
    KOGNITIOWX2 = auto()
    KYVOS_MDX = auto()
    MAPD = auto()
    MARKETO = auto()
    MARK_LOGIC = auto()
    MEM_SQL = auto()
    METAMATRIX = auto()
    MICROSOFT_AS = auto()
    MICROSOFT_DYNAMICS_CRM = auto()
    MICROSOFT_DYNAMICS_ERP = auto()
    MICROSOFT_DYNAMICS_365 = auto()
    MONGO_BI = auto()
    MONGO_DB = auto()
    MY_SQL = auto()
    NEO4J = auto()
    NEOVIEW = auto()
    NETEZZA = auto()
    ODATA = auto()
    OPEN_ACCESS = auto()
    ORACLE = auto()
    ORACLE_CX_SALES = auto()
    ORACLE_CX_SERVICE = auto()
    ORACLE_ELOQUA = auto()
    PALANTIR_FOUNDRY = auto()
    PAR_ACCEL = auto()
    PAR_STREAM = auto()
    PAYPAL = auto()
    PHOENIX = auto()
    PIG = auto()
    PIVOTAL_HAWQ = auto()
    POSTGRE_SQL = auto()
    PRESTO = auto()
    PYTHON = auto()
    RED_BRICK = auto()
    SALESFORCE = auto()
    SAND = auto()
    SAP = auto()
    SAP_BW4_HANA = auto()
    SAP_BW_ODATA = auto()
    SAP_ECC_ODATA = auto()
    SAP_HANA = auto()
    SAP_HANA_MDX = auto()
    SAP_S4_HANA = auto()
    SEARCH_ENGINE = auto()
    SERVICEMAX = auto()
    SERVICENOW = auto()
    SHOPIFY = auto()
    SNOW_FLAKE = auto()
    SPARK_CONFIG = auto()
    SPARK_SQL = auto()
    SPLUNK = auto()
    SQL_SERVER = auto()
    SQUARE = auto()
    STARBURST = auto()
    SUGAR_CRM = auto()
    SYBASE = auto()
    SYBASE_IQ = auto()
    SYBASE_SQL_ANY = auto()
    TANDEM = auto()
    TEAMCITY = auto()
    TERADATA = auto()
    TM1 = auto()
    TRINO = auto()
    TWITTER = auto()
    UNKNOWN = auto()
    URL_AUTH = auto()
    VECTORWISE = auto()
    VERTICA = auto()
    XQUERY = auto()
    YELLOWBRICK = auto()


class GatewayType(AutoCapitalizedName):
    """Enumeration representing gateway type."""

    CLOUD = auto()
    COMMUNITY = auto()
    NATIVE = auto()
    RELATIONAL = auto()
