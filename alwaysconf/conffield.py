class ConfigField:
    __key = None
    __parent = None
    value = None

    def __init__(self, default=None):
        if default is not None:
            self.value = default

    def register_parent(self, name: str, parent):
        """

        :param str name:
        :param alwaysconf.AnyConfig parent:
        :return:
        """
        self.__key = name
        self.__parent = parent

    def __set__(self, instance, value):
        self.value = value
        self.__parent.update()

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f'<{self.__key} is has val {self}>'
