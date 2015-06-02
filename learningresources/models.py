"""
Learning resources data model
"""

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from role.api import roles_init_new_repo
from role.permissions import RepoPermission

class Course(models.Model):
    """
    A course on edX platform (MITx or residential).
    """
    repository = models.ForeignKey('Repository')
    org = models.TextField()
    course_number = models.TextField()
    semester = models.TextField()
    import_date = models.DateField(auto_now_add=True)
    imported_by = models.ForeignKey(User)


class LearningResource(models.Model):
    """
    The units that compose an edX course:
    chapter, sequential, vertical, problem, video, html, etc.
    """
    course = models.ForeignKey(Course)
    learning_resource_type = models.ForeignKey('LearningResourceType')
    uuid = models.TextField()
    title = models.TextField()
    description = models.TextField()
    content_xml = models.TextField()
    materialized_path = models.TextField()
    url_path = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True)
    copyright = models.TextField()
    xa_nr_views = models.IntegerField(default=0)
    xa_nr_attempts = models.IntegerField(default=0)
    xa_avg_grade = models.FloatField(default=0)
    xa_histogram_grade = models.FloatField(default=0)


class LearningResourceType(models.Model):
    """
    Learning resource type:
    chapter, sequential, vertical, problem, video, html, etc.
    """
    name = models.TextField()


class Repository(models.Model):
    """
    A collection of learning resources
    that come from (usually tightly-related) courses.
    """
    name = models.TextField()
    description = models.TextField()
    create_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User)

    class Meta:
        permissions = (
            RepoPermission.edit_repo,
            RepoPermission.use_repo,
            RepoPermission.view_repo,
        )

    def save(self, *args, **kwargs):
        is_create = False
        if not self.id:
            is_create = True
        super(Repository, self).save(*args, **kwargs)
        if is_create:
            roles_init_new_repo(self)
