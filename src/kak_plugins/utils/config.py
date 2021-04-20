from typing import Any, Dict

config_path = "plugins.toml"


def read_config(loader: Any, config_path: str) -> Dict:
    """Read configuration options from a file
    args:
        - loader: a function that lets us load from a config file, like `toml.load`
            or `json.load`. Passing it here lets us use dependency injection for
            better testing and allows us to easily change the config format in the
            future
        - config_path: a filesystem path to the config file
    """
    with open(config_path, "r") as config_file:
        return loader.load(config_file)
