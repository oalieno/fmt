# fmt

help you create **format string payload**

currently just for **amd64** (because for 32-bit you can use [pwntools - fmtstr](http://docs.pwntools.com/en/stable/fmtstr.html))

put address data after the format string to **avoid '\x00' cut of the string** (which pwntools fail to handle)

no dependency

## Install

```
pip install git+https://github.com/OAlienO/fmt.git
```

## Example

```python
from fmt import FMT

f = fmt()
f[0x601018] = 0x400747 # write address 0x601018 with data 0x400747
payload = f.payload(offset = 6, printed = 8)
```
