__all__ = ['GroupConfiguration', 'ConnectionHandler']

from .connection import ConnectionHandler
from .configuration import GroupConfiguration

from .managers import PermissionManager


class UsageOnRegistry(object):

    _use_on = None

    def __init__(self):
        self._use_on = {}

    def use_permissions_on(self, name):
        self._use_on[name.lower()] = PermissionManager(name)

    def __getattr__(self, attr_name):
        return self._use_on[attr_name.lower()]

use_on = UsageOnRegistry()
