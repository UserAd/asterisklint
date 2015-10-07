# vim: set ts=8 sw=4 sts=4 et ai:
from .defines import ErrorDef, WarningDef
from .file import W_WSH_BOL


if 'we_dont_want_two_linefeeds_between_classdefs':  # for flake8
    class I_NOTIMPL_TEMPLATES(ErrorDef):
        message = 'asterisklint does not implement template use yet'

    class W_WSH_OBJSET(WarningDef):
        message = 'expected " => " horizontal whitespace around arrow operator'

    class W_WSH_VARSET(WarningDef):
        message = 'expected no horizontal whitespace around equals operator'


class EmptyLine(object):
    def __init__(self, comment, where):
        self.comment = comment
        self.where = where


class Context(object):
    @classmethod
    def from_context(cls, context):
        """
        Use this on subclasses of Context.
        """
        assert not context._varsets
        return cls(name=context.name, templates=context._templates,
                   comment=context.comment, bolspace='',
                   where=context.where)

    def __init__(self, name, templates='', comment=False, bolspace='',
                 where=None):
        if bolspace:
            W_WSH_BOL(where)

        self.name = name
        self.comment = comment
        self.where = where
        self._templates = templates
        self._varsets = []

        if templates:
            I_NOTIMPL_TEMPLATES(where)

    def add(self, varset):
        self._varsets.append(varset)

    def __bool__(self):
        # Must(!) define this, now that we use __len__.
        return True

    def __len__(self):
        return len(self._varsets)

    def __getitem__(self, key):
        assert isinstance(key, int)
        return self._varsets[key]

    def __repr__(self):
        return '[{}]({}) => ({} elements)'.format(
            self.name, self._templates, len(self._varsets))


class Varset(object):
    def __init__(self, variable, value, separator, comment, where):
        clean_separator = separator.strip()
        if clean_separator == '=>':
            if separator != ' => ':
                W_WSH_OBJSET(where)
            self.arrow = True
        elif clean_separator == '=':
            if separator != '=':
                W_WSH_VARSET(where)
            self.arrow = False

        if variable.startswith(tuple(' \t')):
            # QUICK HACK: only allow leading WS for 'same'..
            variable = variable.lstrip(' \t')
            if variable != 'same':
                W_WSH_BOL(where)

        self.variable = variable
        self.value = value
        self.comment = comment
        self.where = where