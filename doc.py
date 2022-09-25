"""
Generates mermaid code for all classes in a module
"""

import inspect
from game import Agent
import re 

def generate_class_uml(class_):
    str = f"class {class_.__name__} {{\n"
    for attr in class_.__dict__:
        if attr.startswith("__"):
            continue
        if not inspect.isfunction(class_.__dict__[attr]):
            str += f" {attr}\n"
        else:
            args = inspect.getfullargspec(class_.__dict__[attr]).args[1:]
            str += f"  +{attr}({','.join(args)}) \n"
    str += "}\n"

    return str

stack = [Agent]

uml = "classDiagram\n"
while stack:
    class_ = stack.pop()
    uml += generate_class_uml(class_)
    for subclass in class_.__subclasses__():
        uml += f"{class_.__name__} <|-- {subclass.__name__}\n"
        stack.append(subclass)

f = open("README.md", "r")
actual_content = f.read()
actual_content = re.sub(r"```mermaid(\n|.)*```", f"```mermaid\n{uml}```", actual_content)
f.close()
f = open("README.md", "w")
f.write(actual_content)
f.close()

