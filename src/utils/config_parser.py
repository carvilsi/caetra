import tomllib

# TODO: Add a config checker for mandatory variables
f = open("./config/develop.toml", "rb")
config = tomllib.load(f)
