
USER_PASSWORD = 'abcdeF3#'


def dict_factory(factory_cls, **kwargs):
    return factory_cls.stub(**kwargs).__dict__


def extra_kwargs_factory(fields, **options):
    return {k: options for k in fields}


def enum_choices_factory(enum_cls):
    return tuple([(member.value, member.value) for name, member in enum_cls.__members__.items()])
