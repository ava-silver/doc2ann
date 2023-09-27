# stdlib
from __future__ import annotations
from ast import (
    AST,
    Expr,
    FunctionDef,
    Name,
    Str,
    get_docstring,
    stmt,
)
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
import re
from types import GenericAlias
from typing import Literal

# 3p
from docstring_parser import Docstring, compose, parse
from refactor import Rule, Replace, Configuration


@dataclass
class Doc2AnnConfig(Configuration):
    preserve_non_square_brackets: bool = False
    preserve_list_literals: bool = False
    preserve_dict_literals: bool = False
    unparseable_types: UnparseableBehavior = "allow"
    keep_arg_description: bool = False
    unparser: str = "precise"


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
    config: Doc2AnnConfig

    def check_file(self, path: Path | None) -> bool:
        self.config = self.context.config  # type: ignore
        return super().check_file(path)

    def match(self, func: AST) -> Replace:
        assert isinstance(func, FunctionDef)
        assert (docstring := get_docstring(func))
        assert (name := func.name) not in SEEN_FUNCTIONS
        SEEN_FUNCTIONS.add(name)

        new_func = deepcopy(func)
        new_func.decorator_list = []

        doc = parse(docstring)
        if new_docstring := self.process_docstring(doc):
            new_func.body[0] = new_docstring
        else:
            new_func.body.pop(0)
        params = {arg.arg: arg.annotation for arg in func.args.args}
        for param_doc in doc.meta:
            if not hasattr(param_doc, "arg_name"):
                continue
            arg_name: str = param_doc.arg_name  # type: ignore
            if arg_name not in params or params[arg_name] is not None:
                # only add annotation to existing params without existing annotations
                continue
            arg_ann: str | None = param_doc.type_name  # type: ignore
            params[arg_name] = self.get_type(arg_ann)
        for arg in new_func.args.args:
            if new_ann := params.get(arg.arg):
                arg.annotation = new_ann
        new_func.returns = func.returns or self.get_type(
            (doc.returns and doc.returns.type_name) or get_return(docstring)
        )
        return Replace(func, new_func)

    def process_ann(self, annotation: str) -> str:
        annotation = annotation.strip()
        if (
            not self.config.preserve_list_literals
            and annotation.startswith("[")
            and annotation.endswith("]")
        ):
            annotation = f"list{annotation}"
        if not self.config.preserve_dict_literals:
            annotation = annotation.replace("{}", "dict")
        if not self.config.preserve_non_square_brackets:
            annotation = (
                annotation.replace("<", "[")
                .replace(">", "]")
                .replace("(", "[")
                .replace(")", "]")
            )

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
        unparseable = self.config.unparseable_types

        if unparseable == "allow":
            return Name(ann)
        elif unparseable == "drop":
            return None
        elif unparseable == "str":
            return Str(ann)

    def process_docstring(self, doc: Docstring) -> stmt | None:
        doc = deepcopy(doc)
        if not self.config.keep_arg_description:
            doc.meta = []
        for param in doc.meta:
            if hasattr(param, "type_name"):
                param.type_name = None  # type: ignore

        new_docstring = compose(doc)

        return Expr(Str(new_docstring)) if new_docstring else None
