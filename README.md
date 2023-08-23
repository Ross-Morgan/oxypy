# oxypy
![Tests](https://img.shields.io/github/actions/workflow/status/Ross-Morgan/oxypy/tests.yml)

A fully-featured implementation of Rust's `Option<T>` and `Result<T, E>` in Python

Inner values are designed to be quasi-private, since true privacy is impossible without building the package in C or Rust, and I didn't want to extras of doing that.

The source code is cursed yet expandable, well-documented and somehow beautiful

---

## Methods

Some methods are deemed unnecessary due to the differences in the languages

Removed Methods:

- Copy and clone methods
- Ref and deref methods
- Unchecked methods
- Transpose methods

Reasons:
- Methods relating to references are useless due to lack of them in Python.
- Unchecked methods are unneccessary due to the inherent inability to be unsafe.
- Transpose methods are also impossible due to the dynamic type system.

---

## Use

|Rust               |Python            |
|-------------------|------------------|
| `Option::Some(v)` | `Option.some(v)` |
| `Option::None`    | `Option.none()`  |
| `Result::Ok(v)`   | `Result.ok(v)`   |
| `Result::Err(v)`  | `Result.err(v)`  |

---

## Examples

**Note:** *Type annotations are not always necessary, but are done here for brevity*

`Option[T]` and `Result[T, E]` can be imported directly from the `oxypy` library

```python
from oxypy import Option, Result

some: Option[int] = Option.some(10)
none: Option[int] = Option.none()

ok: Result[int, str] = Result.ok(10)
err: Result[int, str] = Result.err("An error occured")
```
