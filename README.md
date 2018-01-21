# FMT

help you create **format string payload**

currently just for **amd64** (because for 32-bit you can use [pwntools - fmtstr](http://docs.pwntools.com/en/stable/fmtstr.html))

put address data after the format string to **avoid '\x00' cut of the string** (which pwntools fail to handle)

no dependency

## Install

git clone it down and import it

```
git clone https://github.com/OAlienO/FMT.git
cp FMT/FMT.py your_path/
```

currently not on PYPI

## Example

```python
from FMT import FMT

F = FMT()
F[0x601018] = 0x400747 # write address 0x601018 with data 0x400747
payload = F.payload(offset = 6, printed = 8)
```
