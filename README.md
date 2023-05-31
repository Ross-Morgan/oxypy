# Magik

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
