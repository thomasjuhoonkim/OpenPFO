# system
import tomllib


def get_config():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
        return config
