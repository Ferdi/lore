"""
Test the APIs views to make sure they work.
"""

from __future__ import unicode_literals

from django.test.testcases import TestCase

from role.permissions import GroupTypes


class TestRolePermission(TestCase):
    """
    Test for the permissions
    """
    def test_group_types(self):
        """
        Checks repo group types
        """
        self.assertEqual(
            GroupTypes.repo_administrator,
            '{}_repo_administrators'
        )
        self.assertEqual(
            GroupTypes.repo_curator,
            '{}_repo_curators'
        )
        self.assertEqual(
            GroupTypes.repo_author,
            '{}_repo_authors'
        )
