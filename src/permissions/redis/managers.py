from .configuration import GroupConfiguration
from .connection import ConnectionHandler


class PermissionManager(object):

    on = None

    def __init__(self, on):
        self.on = on

    def __on_str(self, on_id):
        return '{}_{}'.format(self.on, on_id)

    def get_users_by_group(self, on_id, *args, **kwargs):
        return GroupUserManager.get_users_by_group(self.__on_str(on_id), *args, **kwargs)

    def add_user_to_group(self, on_id, *args):
        return UserManager.add_user_to_group(self.__on_str(on_id), *args)

    def remove_user_from_groups(self, on_id, *args):
        return UserManager.remove_user_from_groups(self.__on_str(on_id), *args)

    def user_groups(self, on_id, *args):
        return UserManager.user_groups(self.__on_str(on_id), *args)

    def user_has_permissions(self, on_id, *args):
        return UserManager.has_permissions(self.__on_str(on_id), *args)


class GroupUserManager(ConnectionHandler):
    BASE_KEY = 'g_u_{}{}'

    @classmethod
    def get_key(cls, group_id, on_str):
        on_str = '_{}'.format(on_str)
        return cls.BASE_KEY.format(str(group_id), on_str)

    @classmethod
    def get_users_by_group(cls, on, group_id_or_group_name, num=None):
        group_id = GroupConfiguration.get_group_id_by_name(group_id_or_group_name)
        group_key = cls.get_key(group_id, on)
        return map(int, cls._redis.smembers(group_key)[:num])


class UserManager(ConnectionHandler):
    BASE_KEY = 'u_g_{}{}'

    @classmethod
    def get_key(cls, user_id, on_str):
        on_str = '_{}'.format(on_str)
        return cls.BASE_KEY.format(str(user_id), on_str)

    @classmethod
    def add_to_group(cls, on, user_id, groups):
        if isinstance(groups, (int, str)):
            groups = [str(groups), ]
        redis_key = cls.get_key(user_id, on)
        pipeline = cls._redis.pipeline()
        pipeline.sadd(redis_key, *groups)
        for group in groups:
            group_key = GroupUserManager.get_key(group, on)
            pipeline.sadd(group_key, user_id)
        pipeline.execute()

    @classmethod
    def remove_from_group(cls, on, user_id, groups):
        if isinstance(groups, (int, str)):
            groups = [str(groups), ]
        redis_key = cls.get_key(user_id, on)
        pipeline = cls._redis.pipeline()
        pipeline.srem(redis_key, *groups)
        for group in groups:
            group_key = GroupUserManager.get_key(group, on)
            pipeline.srem(group_key, user_id)
        pipeline.execute()

    @classmethod
    def has_permissions(cls, on, user_id, permissions):
        u_groups = cls.user_groups(on, user_id)
        for group in u_groups:
            permissions -= GroupConfiguration.get_permissions_for_group(group)
            if not permissions:
                return True
        return not len(permissions)

    @classmethod
    def user_groups(cls, on, user_id):
        redis_key = cls.get_key(user_id, on)
        return map(int, cls._redis.smembers(redis_key))
