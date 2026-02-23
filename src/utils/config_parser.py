import tomllib

# TODO: Add a config checker for mandatory variables
f = open("./config/local.toml", "rb")
config = tomllib.load(f)
