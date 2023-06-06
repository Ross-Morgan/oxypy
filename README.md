# Magik

![Tests](https://github.com/Ross-Morgan/actions/workflows/tests.yml/badge.svg)
![Coverage]()

A fully-featured implementation of Rust's `Option<T>` and `Result<T, E>` in Python

Using some slightly cursed workarounds, the inner value is pseudo-private. It's difficult to access the inner value but you can.

---

## Methods

Some methods are deemed unnecessary due to the differences in the languages

Removed Methods:

- Copy and clone methods
- Ref and deref methods
- Unchecked methods
- Transpose methods

Methods relating to references are useless due to lack of them in Python.

Transpose methods are also impossible due to the weak, dynamic type system

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
