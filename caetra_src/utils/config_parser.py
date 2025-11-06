import tomllib

def read(toml_path):
    print(toml_path)
    f = open(toml_path, "rb")
    return tomllib.load(f)


f = open("./config/develop.toml", "rb")
config = tomllib.load(f)


