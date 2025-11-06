import tomllib

# def config():
    # try:
f = open("./config/develop.toml", "rb")
config = tomllib.load(f)
    # except:
        # print("config file not found")


