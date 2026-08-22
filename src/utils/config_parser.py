import os
import tomllib

CONFIG_PATHS = {
    "local": "./config/local.toml",
    "develop": "./config/develop.toml",
}


def _load_dotenv(path: str = "./.env") -> None:
    if not os.path.isfile(path):
        return
    with open(path) as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip("'\"")
            os.environ.setdefault(key, value)


_load_dotenv()

caetra_env = os.environ.get("CAETRA_ENV", "local")
config_path = CONFIG_PATHS.get(caetra_env)
if config_path is None:
    raise ValueError(
        f"Invalid CAETRA_ENV '{caetra_env}', expected one of: {', '.join(CONFIG_PATHS)}"
    )

with open(config_path, "rb") as f:
    config = tomllib.load(f)
