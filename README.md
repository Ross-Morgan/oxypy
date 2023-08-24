# oxypy
![Tests](https://img.shields.io/github/actions/workflow/status/Ross-Morgan/oxypy/tests.yml)

Fully-featured ports of several essential structs from Rust into pure Python

Since true privacy is impossible, inner values of the classes are designed to be quasi-private.

---

## Methods

Some methods are deemed unnecessary due to the differences in the languages

Removed Methods:

- Copy and clone methods
- Ref and deref methods
- Unchecked methods
- Type-dependent methods

Reasons:

- Methods relating to references are useless due to lack of them in Python.
- Unchecked methods are unneccessary due to the lac of the unsafe system.
- Type dependent methods are practically impossible due to the dynamic type system.

---

## Examples

**Note:** *Type annotations are not always necessary, but are done here for brevity*

### Option

```python
from oxypy import Option

some: Option[int] = Option.some(10)
none: Option[int] = Option.none()
```

### Result

```python
ok: Result[int, str] = Result.ok(10)
err: Result[int, str] = Result.err("An error occured")
```

### Either

```python
from oxypy import Either

left: Either[int, float] = Either.left(42)
right: Either[int, float] = Either.right(3.14159265)
```
