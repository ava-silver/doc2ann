# stdlib
from __future__ import annotations
from ast import AST, Expr, FunctionDef, Name, Str, fix_missing_locations, get_docstring
from copy import deepcopy
import re
from types import GenericAlias
from typing import Literal

# 3p
from docstring_parser import parse
from refactor import Rule, Replace


UnparseableBehavior = Literal["allow", "drop", "str"]

OUTER_PAREN_REGEX = re.compile(r"\(((?:[^()]|\([^()]*\))*)\)")


def get_return(doc: str):
    parts = doc.split("Return:")
    if len(parts) > 1:
        if matches := OUTER_PAREN_REGEX.findall(parts[1]):
            return matches[-1]
        elif parts := parts[1].split(":"):
            return parts[0].lstrip()


SEEN_FUNCTIONS = set()


class FixDocstring(Rule):
    def match(self, func: AST) -> Replace:
        assert isinstance(func, FunctionDef)
        assert (docstring := get_docstring(func))
        assert (name := func.name) not in SEEN_FUNCTIONS
        SEEN_FUNCTIONS.add(name)

        new_func = deepcopy(func)
        fix_missing_locations(new_func)

        doc = parse(docstring)
        new_func.body[0] = Expr(Str(doc.short_description))

        params = {arg.arg: arg.annotation for arg in func.args.args}
        for param_doc in doc.meta:
            arg_name: str = param_doc.arg_name  # type: ignore
            if arg_name not in params or params[arg_name] is not None:
                # only add annotation to existing params without existing annotations
                continue
            arg_ann: str | None = param_doc.type_name  # type: ignore
            params[arg_name] = self.get_type(arg_ann)
        for arg in new_func.args.args:
            if new_ann := params.get(arg.arg):
                arg.annotation = new_ann
        new_func.returns = self.get_type(
            (doc.returns and doc.returns.type_name) or get_return(docstring)
        )
        return Replace(func, new_func)

    def process_ann(self, annotation: str) -> str:
        if self.context.config.convert_caret_to_bracket:  # type: ignore
            annotation = annotation.replace("<", "[").replace(">", "]")
        return annotation

    def get_type(self, ann: str | None) -> Name | Str | None:
        if not ann:
            return None
        try:
            if ann:
                ann = self.process_ann(ann)
            type_ = eval(ann)
            if isinstance(type_, (type, GenericAlias)):
                return Name(ann)
        except Exception:
            pass
        unparseable_types: UnparseableBehavior = self.context.config.unparseable_types  # type: ignore
        match unparseable_types:
            case "allow":
                return Name(ann)
            case "drop":
                return None
            case "str":
                return Str(ann)
