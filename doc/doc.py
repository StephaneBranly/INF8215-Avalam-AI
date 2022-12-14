"""
Generates mermaid code for all classes in a module
"""

import os, sys


currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import inspect
from game import Agent
from avalam import ImprovedBoard
from heuristic.Heuristic import Heuristic

import re 

repo_path = "https://github.com/StephaneBranly/Avalam-AI"

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
    str += f"""click {class_.__name__} href "{repo_path}/blob/main/doc/{class_.__name__}.md" "Detail of the class {class_.__name__}\"\n"""
    return str

def generate_class_diagram(modules):
    stack = modules
    visited = []
    uml = "classDiagram\n"
    while stack:
        class_ = stack.pop()

        if class_.__name__ not in visited:
            visited.append(class_.__name__)
            uml += generate_class_uml(class_)
            class_documentation = generate_class_documentation(class_)
            create_class_documentation(class_documentation, class_.__name__)
            for subclass in class_.__subclasses__():
                uml += f"{class_.__name__} <|-- {subclass.__name__}\n"
                stack.append(subclass)
            for parentclass in class_.__bases__:
                if parentclass.__name__ != "object":
                    stack.append(parentclass)

    update_readme_class_diagram(uml)

def clean_doc_description(doc):
    str = re.sub(r'[^\S\r\n]+', ' ', doc)
    str = re.sub(r'\n\s', '\n', str)
    str = re.sub(r'(Arguments|Returns|Return|Example)\s?:', r'#### \1:', str)
    str = re.sub(r'(.*)\s?--\s?(.*)', r'* ```\1```: \2', str)
    return str.replace("\t", "\n")

def generate_class_documentation(class_):
    str = f"# {class_.__name__}\n"
    str += f"Back to [readme menu](../README.md)\n\n"
    if class_.__doc__:
        str += f"{class_.__doc__}\n"
    str += f"## Attributes\n"
    for attr in class_.__dict__:
        if attr.startswith("__"):
            continue
        if not inspect.isfunction(class_.__dict__[attr]):
            str += f"### ```{attr}```\n"
            if class_.__dict__[attr].__doc__:
                str += f"{clean_doc_description(class_.__dict__[attr].__doc__)}\n"
        else:
            args = inspect.getfullargspec(class_.__dict__[attr]).args[1:]
            str += f"### ```{attr}({','.join(args)})```\n"
            if class_.__dict__[attr].__doc__:
                str += f"{clean_doc_description(class_.__dict__[attr].__doc__)}\n"
        str += "\n----\n\n"
    return str

def update_readme_class_diagram(uml):
    f = open("README.md", "r")
    actual_content = f.read()
    actual_content = re.sub(r"```mermaid(\n|.)*```", f"```mermaid\n{uml}```", actual_content)
    f.close()
    f = open("README.md", "w")
    f.write(actual_content)
    f.close()

def create_class_documentation(class_md, classname):
    f = open(f"./doc/{classname}.md", "w")
    f.write(class_md)
    f.close()

if __name__ == "__main__":
    generate_class_diagram([Agent, Heuristic, ImprovedBoard])