from __future__ import annotations
from pprint import pprint
from types import FunctionType, MethodType
from typing import Union
from docstring_parser import parse
from importlib.util import spec_from_file_location, module_from_spec
from inspect import getmembers as _get_members, isclass, isfunction, ismethod, signature, _empty as empty
from ast import AST, Constant, Name, FunctionDef
from refactor import Rule, Replace, run


### GET INFO CODE

def get_members(obj):
    return [
        value
        for name, value in _get_members(obj)
        if name != "__builtins__" and not name.startswith("__")
    ]


def init_module(file):
    spec = spec_from_file_location("module_name", file)
    if not spec:
        raise ValueError("no spec found")
    module = module_from_spec(spec)
    if not spec.loader:
        raise ValueError("no spec loader found")
    spec.loader.exec_module(module)
    return module

def get_type(ann: str) -> type | str | None:
    if not ann:
        return None
    try:
        type_ = eval(ann)
        if isinstance(type_, type):
            return type_
        
    except Exception as e:
        return ann
    
ReplaceDict = dict[str, tuple[str, dict[str, Union[type, str]]]]

def update_function(func: FunctionType | MethodType, type_map: ReplaceDict):
    if not func.__doc__:
        return
    doc = parse(func.__doc__)
    params = signature(func).parameters
    type_map[func.__qualname__] = (doc.short_description or "", {})
    arg_types = type_map[func.__qualname__][1]
    for param_doc in doc.meta:
        arg_name: str = param_doc.arg_name # type: ignore
        if arg_name not in params or params[arg_name].annotation is not empty:
            # only add annotation to existing params without existing annotations
            continue
        type_ = get_type(param_doc.type_name) # type: ignore
        if type_:
            arg_types[arg_name] = type_


def get_info(obj) -> ReplaceDict:
    type_map = {}
    members = get_members(obj)
    for member in members:
        if isfunction(member) or ismethod(member):
            update_function(member, type_map)
        elif isclass(member):
            type_map.update(get_info(member))
    return type_map


### REPLACEMENTS CODE

file = "./hi.py"
module = init_module(file)
replacements = get_info(module)

class FixDocstring(Rule):

    # And each rule implements a "match()" method, which would
    # receive every node in the tree in a breadth-first order.
    def match(self, node: AST) -> Replace:
        # This is where things get interesting. Instead of just writing
        # filters with if statements, you can use the following assert
        # based approach (a contract of transformation).

        assert isinstance(node, FunctionDef)
        assert node.id == "placeholder"

        # And this is where we choose what action we are taking for the
        # given node (which we have verified with our contract). There
        # are multiple transformation actions, but in this case what we
        # need is something that replaces a node with another one.
        replacement = Constant(42)
        return Replace(node, replacement)




# if __name__ == "__main__":
    # run(rules=[FixDocstring])

