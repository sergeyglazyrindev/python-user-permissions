class GroupConfiguration(object):
    '''
    This variable has following structure:
    ``{
        'group_name': {
            'id':  number,
            'permissions': ['users.add', 'users.del', 'etc']
        }
    }``
    '''
    _groups = None

    def __init__(self):
        self._groups = {}

    def configure_groups(self, groups):
        '''
        This method configures class variable _groups.
        Please look for documentation for :data:GroupConfiguration._groups
        You may call few times this method to adjust permissnions for group.
        Args:
            :param groups: dict
            :type groups: dict
        Returns: None
        '''

        for group_name, _data in groups.iteritems():
            group_name = group_name.lower()
            # that means that group is not configured yet
            if 'permissions' not in self._groups.get(group_name, {}):
                self._groups[group_name] = {'permissions': set(), 'id': _data['id']}
            self._groups[group_name]['permissions'] |= set(map(str.lower, _data.get('permissions', set())))

    def extend_permissions_for_group(self, group_id_or_name, permissions):
        '''
        Small helper to simplify extending group permissions
        Args:
            :param group_id_or_name: Name or id of the group
            :type group_id_or_name: int|str
            :param permissions: list of permissions
            :type permissions: list|tuple|set
        Returns: None
        '''
        group_name = self.get_group_name_by_id(group_id_or_name)
        # prevent not configured groups
        if 'permissions' not in self.groups.get(group_name, {}):
            self.groups[group_name]['permissions'] = set()
        self.groups[group_name]['permissions'] |= map(str.lower, permissions or [])

    def get_group_name_by_id(self, group_id_or_name):
        '''
        Small helper which does group introspection and finds out group name by id
        Args:
            :param group_id_or_name: Name or id of the group
            :type group_id_or_name: int|str
        Returns: str
        '''
        group_id_or_name = str(group_id_or_name)
        if not group_id_or_name.isdigit():
            return group_id_or_name.lower()
        group_id_to_name = {self.groups[group_name]['id']: group_name for group_name in self.groups.keys()}
        return group_id_to_name[group_id_or_name].lower()

    def get_group_id_by_name(self, group_id_or_name):
        '''
        Small helper which does group introspection and finds out group id by name
        Args:
            :param group_id_or_name: Name or id of the group
            :type group_id_or_name: int|str
        Returns: int
        '''
        group_id_or_name = str(group_id_or_name)
        if group_id_or_name.isdigit():
            return group_id_or_name
        group_name_to_id = {group_name: self.groups[group_name]['id'] for group_name in self.groups.keys()}
        return str(group_name_to_id[group_id_or_name])

    def get_permissions_for_group(self, group_id_or_name):
        '''
        Small helper which returns permission list for the given group
        Args:
            :param group_id_or_name: Name or id of the group
            :type group_id_or_name: int|str
        Returns: set
        '''
        group_name = self.get_group_name_by_id(group_id_or_name)
        return self.groups.get(group_name, {}).get('permissions', set())

group_config = GroupConfiguration()
