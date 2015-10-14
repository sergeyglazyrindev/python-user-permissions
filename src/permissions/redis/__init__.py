__all__ = ['GroupConfiguration', 'ConnectionHandler']

from .connection import ConnectionHandler
from .configuration import GroupConfiguration

from .managers import PermissionManager


class UsageOnRegistry(object):

    _use_on = None

    def __init__(self):
        self._use_on = {}

    def use_permissions_on(self, name):
        '''
        Registers legal way to use permissions for
        Args:
            :param name: permission alias or name
            :type name: str
        Returns: None
        '''
        self._use_on[name.lower()] = PermissionManager(name)

    def __getattr__(self, attr_name):
        '''
        returns PermissionManager for the way to use permission for
        Args:
            :param attr_name: Registered way (alias) to use permission for
            :type attr_name: str
        Returns: PermissionManager
        '''
        return self._use_on[attr_name.lower()]

use_on = UsageOnRegistry()
