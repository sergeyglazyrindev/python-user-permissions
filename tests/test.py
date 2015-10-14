from unittest import TestCase

from src.permissions.redis import group_config, use_on, ConnectionHandler

group_config.configure_groups({
    'admin': {
        'id': 1,
        'permissions': ['test', 'test1', 'test2']
    },
    'reader': {
        'id': 2,
        'permissions': ['readtest', 'readtest1', 'readtest2']
    },
    'guest_writer': {
        'id': 3,
        'permissions': ['guestwriter1', 'guestwriter2', 'guestwriter3']
    }
})

use_on.use_permissions_on('test_entity')

permission_manager = use_on.test_entity

test_on_id = 19
test_user_id = 20


class TestPackage(TestCase):

    def tearDown(self):
        ConnectionHandler._redis().flushall()

    def test(self):

        on_kwargs = {'on_id': test_on_id}
        self.assertEqual(
            list(permission_manager.get_users_by_group('admin', **on_kwargs)),
            []
        )

        permission_manager.add_user_to_group(test_user_id, 'admin', **on_kwargs)

        self.assertEqual(
            list(permission_manager.get_users_by_group('admin', **on_kwargs)),
            [20, ]
        )

        permission_manager.remove_user_from_groups(test_user_id, 'admin', **on_kwargs)

        self.assertEqual(
            list(permission_manager.get_users_by_group('admin', **on_kwargs)),
            []
        )

        permission_manager.add_user_to_group(test_user_id, 'admin', **on_kwargs)

        self.assertEqual(
            list(permission_manager.user_groups(test_user_id, **on_kwargs)),
            [1, ]
        )

        self.assertTrue(permission_manager.user_has_permissions(test_user_id, ['test', ], **on_kwargs))

        self.assertTrue(not permission_manager.user_has_permissions(
            test_user_id,
            ['test', 'guestwriter1'],
            **on_kwargs
        ))

        permission_manager.add_user_to_group(test_user_id, 'guest_writer', **on_kwargs)

        self.assertTrue(permission_manager.user_has_permissions(test_user_id, ['test', 'guestwriter1'], **on_kwargs))
