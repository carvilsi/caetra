import click

@click.command()
@click.option("--shield_name", prompt="Shield name",
              help="New caetra shield name.")
# TODO: would it be nice to check if the kprobe_event exists
@click.option("--kprobe_event", prompt="Kprobe event",
              help="Kprobe event.")
@click.option("--c_function_name", prompt="Function name",
              help="Name function for c code.")

def caetra_shield_gen(shield_name, kprobe_event, c_function_name):
    """caetra bpf shield generator."""

    # we do not want spaces on Shields name
    shield_name = shield_name.replace(" ", "_") 

    print(shield_name)
    print(kprobe_event)
    print(c_function_name)


if __name__ == "__main__":
    caetra_shield_gen()
