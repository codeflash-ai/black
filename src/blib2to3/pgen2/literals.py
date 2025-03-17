# Copyright 2004-2005 Elemental Security, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""Safely evaluate Python string literals without using eval()."""

import re

simple_escapes: dict[str, str] = {
    "a": "\a",
    "b": "\b",
    "f": "\f",
    "n": "\n",
    "r": "\r",
    "t": "\t",
    "v": "\v",
    "'": "'",
    '"': '"',
    "\\": "\\",
}


def escape(m: re.Match[str]) -> str:
    tail = m.group(1)
    esc = simple_escapes.get(tail)
    if esc is not None:
        return esc
    if tail.startswith("x"):
        hexes = tail[1:]
        if len(hexes) != 2:
            raise ValueError("invalid hex string escape ('\\%s')" % tail)
        try:
            return chr(int(hexes, 16))
        except ValueError:
            raise ValueError("invalid hex string escape ('\\%s')" % tail) from None
    else:
        try:
            return chr(int(tail, 8))
        except ValueError:
            raise ValueError("invalid octal string escape ('\\%s')" % tail) from None


def evalString(s: str) -> str:
    assert s.startswith("'") or s.startswith('"'), repr(s[:1])
    q = s[0]
    if s[:3] == q * 3:
        q = q * 3
    assert s.endswith(q), repr(s[-len(q) :])
    assert len(s) >= 2 * len(q)
    s = s[len(q) : -len(q)]
    return re.sub(r"\\(\'|\"|\\|[abfnrtv]|x.{0,2}|[0-7]{1,3})", escape, s)


def test() -> None:
    for i in range(256):
        c = chr(i)
        s = repr(c)
        e = evalString(s)
        if e != c:
            print(i, c, s, e)


if __name__ == "__main__":
    test()
