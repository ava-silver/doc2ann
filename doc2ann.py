from __future__ import annotations
from copy import deepcopy
import re
from types import GenericAlias
from docstring_parser import parse
from ast import AST, Expr, FunctionDef, Name, Str, fix_missing_locations, get_docstring
from refactor import Rule, Replace, run

OUTER_PAREN_REGEX = re.compile(r"\(((?:[^()]|\([^()]*\))*)\)")

CONVERT_CARET_TO_BRACKET = True


def get_type(ann: str | None) -> Name | Str | None:
    if not ann:
        return None
    try:
        if CONVERT_CARET_TO_BRACKET and ann:
            ann = ann.replace("<", "[").replace(">", "]")
            print(ann)
        type_ = eval(ann)
        if isinstance(type_, (type, GenericAlias)):
            return Name(ann)
    except Exception:
        pass
    return Str(ann)


def get_return(doc: str):
    parts = doc.split("Return:")
    if len(parts) > 1:
        if matches := OUTER_PAREN_REGEX.findall(parts[1]):
            return matches[-1]
        elif parts := parts[1].split(":"):
            return parts[0].lstrip()


seen_already = set()


class FixDocstring(Rule):
    def match(self, func: AST) -> Replace:
        assert isinstance(func, FunctionDef)
        assert (docstring := get_docstring(func))
        assert (name := func.name) not in seen_already
        seen_already.add(name)

        new_func = deepcopy(func)
        fix_missing_locations(new_func)

        doc = parse(docstring)
        print(new_func.body, doc.short_description)
        new_func.body[0] = Expr(Str(doc.short_description))

        params = {arg.arg: arg.annotation for arg in func.args.args}
        for param_doc in doc.meta:
            arg_name: str = param_doc.arg_name  # type: ignore
            if arg_name not in params or params[arg_name] is not None:
                # only add annotation to existing params without existing annotations
                continue
            arg_ann: str | None = param_doc.type_name  # type: ignore
            params[arg_name] = get_type(arg_ann)
        for arg in new_func.args.args:
            if new_ann := params.get(arg.arg):
                arg.annotation = new_ann
        print(f"{doc.many_returns=}")
        new_func.returns = get_type(
            (doc.returns and doc.returns.type_name) or get_return(docstring)
        )
        return Replace(func, new_func)


if __name__ == "__main__":
    run(rules=[FixDocstring])
