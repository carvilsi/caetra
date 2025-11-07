import os
from jinja2 import Environment, FileSystemLoader

# loading the environment
env = Environment(loader = FileSystemLoader("templates"))

# loading the template
template = env.get_template("ctr_bpf_py.jinja")

# rendering the template and storing the resultant text in variable output
output = template.render(shield_name = "test", kprobe_event = "foo")

# printing the output on screen
print(output)

if not os.path.exists("test"):
    os.makedirs("test")

with open("test/test.py", "w", encoding="utf-8") as f:
    f.write(output)
