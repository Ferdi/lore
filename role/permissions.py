"""
Definition of custom permissions
"""

from __future__ import unicode_literals


class GroupTypes(object):  # pylint: disable=too-few-public-methods
    """
    Definition of generic group names
    """
    repo_administrator = '{}_repo_administrators'
    repo_curator = '{}_repo_curators'
    repo_author = '{}_repo_authors'


class RepoPermission(object):
    """
    Permissions for the repo objects
    Django permissions are defined as a tuple of (name, description)
    """
    edit_repo = ('edit_repo', 'Permission to edit/delete repo')
    use_repo = ('use_repo', 'Permission to use the repo')
    view_repo = ('view_repo', 'Permission to view-only the repo')

    @classmethod
    def administrator_permissions(cls):
        """
        Administrator permissions
        """
        return [
            cls.edit_repo[0],
            cls.use_repo[0],
            cls.view_repo[0],
        ]

    @classmethod
    def curator_permissions(cls):
        """
        Curator permissions
        """
        return [
            cls.use_repo[0],
            cls.view_repo[0],
        ]

    @classmethod
    def author_permissions(cls):
        """
        Author permissions
        """
        return [
            cls.view_repo[0],
        ]
