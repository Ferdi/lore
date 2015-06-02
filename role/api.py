"""
Functions for handling roles
"""

from __future__ import unicode_literals

from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm

from role.permissions import RepoPermission, GroupTypes


def roles_init_new_repo(repo):
    """
    Create new groups for the repo
    """
    administrator_group = Group.objects.get_or_create(
        name=GroupTypes.repo_administrator.format(repo.name)
    )[0]
    curator_group = Group.objects.get_or_create(
        name=GroupTypes.repo_curator.format(repo.name)
    )[0]
    author_group = Group.objects.get_or_create(
        name=GroupTypes.repo_author.format(repo.name)
    )[0]

    # administrator permissions
    for permission in RepoPermission.administrator_permissions():
        assign_perm(permission, administrator_group, repo)
    # curator permissions
    for permission in RepoPermission.curator_permissions():
        assign_perm(permission, curator_group, repo)
    # author permissions
    for permission in RepoPermission.author_permissions():
        assign_perm(permission, author_group, repo)

    return True

def assign_user_to_repo_group(user, repo, group_type=GroupTypes.repo_administrator):
    """
    Assigns an user to a repo specific group type
    """
    repo_group = Group.objects.get(name=group_type.format(repo.name))
    user.groups.add(repo_group)
    user.save()
    return True
