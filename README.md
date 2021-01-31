# alwaysconf
Config manager for busy developers

## Install 
From git
```shell
pip install git+https://github.com/kpostekk/alwaysconf.git
```

## Example
```python
from alwaysconf import *


class MyConfig(AnyConfig):
    val1 = ConfigField('special')
    val2 = ConfigField(True)

if __name__ == '__main__':
    conf = MyConfig.local()  # Will create config.yml
    print(conf.data)  # {'val1': 'special', 'val2': True}
    conf.val1 = 'magic'
    print(conf.data)  # {'val1': 'magic', 'val2': True}
```
