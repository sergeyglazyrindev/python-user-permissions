class GroupConfiguration(object):
    groups = {}

    @classmethod
    def configure_groups(cls, groups):
        for group_name, _data in groups.iteritems():
            group_name = group_name.lower()
            # that means that group is not configured yet
            if 'permissions' not in cls.groups.get(group_name, {}):
                cls.groups[group_name] = {'permissions': set(), 'id': _data['id']}
            cls.groups[group_name]['permissions'] |= set(map(str.lower, _data.get('permissions', set())))

    @classmethod
    def extend_permissions_for_group(cls, group_id_or_name, permissions):
        group_name = cls.get_group_name_by_id(group_id_or_name)
        # prevent not configured groups
        if 'permissions' not in cls.groups.get(group_name, {}):
            cls.groups[group_name]['permissions'] = set()
        cls.groups[group_name]['permissions'] |= map(str.lower, permissions or [])

    @classmethod
    def get_group_name_by_id(cls, group_id_or_name):
        group_id_or_name = str(group_id_or_name)
        if not group_id_or_name.isdigit():
            return group_id_or_name.lower()
        group_id_to_name = {cls.groups[group_name]['id']: group_name for group_name in cls.groups.keys()}
        return group_id_to_name[group_id_or_name].lower()

    @classmethod
    def get_group_id_by_name(cls, group_id_or_name):
        group_id_or_name = str(group_id_or_name)
        if group_id_or_name.isdigit():
            return group_id_or_name
        group_name_to_id = {group_name: cls.groups[group_name]['id'] for group_name in cls.groups.keys()}
        return str(group_name_to_id[group_id_or_name])

    @classmethod
    def get_permissions_for_group(cls, group_id_or_name):
        group_name = cls.get_group_name_by_id(group_id_or_name)
        return cls.groups.get(group_name, {}).get('permissions', set())
