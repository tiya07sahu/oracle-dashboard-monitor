import oracledb
import json
import os

# Automatically use Thin mode (no Oracle Instant Client required)
oracledb.init_oracle_client = lambda *args, **kwargs: None  # Safeguard if called elsewhere

def load_db_config():
    config_path = os.path.join(os.path.dirname(__file__), "cred_new.json")
    try:
        with open(config_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise RuntimeError("cred_new.json file not found.")
    except json.JSONDecodeError:
        raise RuntimeError("Invalid JSON format in cred_new.json.")

def get_oracle_connection(db_name):
    """
    Get Oracle database connection for specified database.
    
    Args:
       
        db_name (str): Database name (rundb1, rundb2,etc.)
    
    Returns:
        oracledb.Connection: Oracle database connection object
    """
    config = load_db_config()
    if db_name not in config:
        raise ValueError(f"Database '{db_name}' not found .")

    creds = config[db_name]
    try:
        connection = oracledb.connect(
            user=creds["user"],
            password=creds["password"],
            dsn=creds["dsn"],
            config_dir=None  # Ensures thin mode
        )
        return connection
    except oracledb.DatabaseError as e:
        raise RuntimeError(f"Oracle DB connection failed for {db_name}: {e}")