from pathlib import Path
from typing import Optional

import yaml

from alwaysconf.conffield import ConfigField


class AnyConfig:
    data: Optional[dict] = None

    def __init__(self, name: Optional[str] = None, forced_path: Optional[Path] = None):
        if name is None:
            p = Path(__file__) if forced_path is None else forced_path
            name = f'{p.parent.name}/{p.name.split(".")[0]}'
        self._name = name
        self.__path = Path.home().joinpath(f'.config/{self._name}.yml') if forced_path is None else forced_path
        self.__register_fields()
        self.load()

    @classmethod
    def local(cls, name='config'):
        return cls(name, Path.cwd().joinpath(f'{name}.yml'))

    def load(self):
        if self.__path.exists():
            with self.__path.open('r', encoding='utf-8') as file:
                self.data = yaml.safe_load(file)

        if self.data is None:
            self.data = {}
            self.update()

        for name, field in self.__fields:
            field.value = self.data.get(name)

    def update(self):
        self.__path.parent.mkdir(exist_ok=True)  # Create .config dir if not exists
        self.__path.touch(exist_ok=True)  # Create some.yml file if not exixts

        for name, field in self.__fields:
            if field.value is not None:  # Field has some value
                self.data.update({name: field.value})  # Insert into dict

        with self.__path.open('w', encoding='utf-8') as file:
            file.write(yaml.safe_dump(self.data, allow_unicode=True))

    @property
    def __fields(self):
        return [(n, f) for n, f in self.__class__.__dict__.items() if isinstance(f, ConfigField)]

    def __register_fields(self):
        for name, field in self.__fields:
            field.register_parent(name, self)
