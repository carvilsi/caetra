
def mac_address_format(macstr):
    return ":".join(macstr[i:i+2] for i in range(0, len(macstr), 2))

