import yaml

def load_config():
    with open("config/application.yml", "r") as file:
        return yaml.safe_load(file)

CONFIG = load_config()
DB_CONFIG = CONFIG["postgres"]
