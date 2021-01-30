import uuid
from pathlib import Path
from typing import Optional

from alwaysconf.conffield import ConfigField

import yaml


class AnyConfig:
    data = {}

    def __init__(self, name: Optional[str] = None):
        if name is None:
            p = Path(__file__)
            name = f'{p.parent.name}/{p.name.split(".")[0]}'
        self._name = name
        self.__register_fields()
        self.load()

    @property
    def path(self):
        return Path().home().joinpath(f'.config/{self._name}.yml')

    def load(self):
        if self.path.exists():
            with self.path.open('r', encoding='utf-8') as file:
                self.data = yaml.safe_load(file)

        if self.data is None:
            self.data = {}
            self.update()

    def update(self):
        self.path.parent.mkdir(exist_ok=True)  # Create .config dir if not exists
        self.path.touch(exist_ok=True)  # Create some.yml file if not exixts

        for name, field in self.__fields:
            if field.value is not None:
                self.data.update({name: field.value})

        with self.path.open('w', encoding='utf-8') as file:
            file.write(yaml.safe_dump(self.data, allow_unicode=True))

    @property
    def __fields(self):
        return [(n, f) for n, f in self.__class__.__dict__.items() if isinstance(f, ConfigField)]

    def __register_fields(self):
        for name, field in self.__fields:
            field.register_parent(name, self)


if __name__ == '__main__':
    class MyConfig(AnyConfig):
        myval = ConfigField(default='my default')

    ac = MyConfig()
    ac.myval = True
    print(ac.data)
