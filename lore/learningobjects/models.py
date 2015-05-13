from django.db import models


class Course(models.Model):
    repository = models.ForeignKey(Repository)
    org = models.TextField()
    course_number = models.IntegerField()
    semester = models.TextField()
    import_date = models.DateField()
    imported_by = models.TextField()

class LearningObject(models.Model):
    course = models.ForeignKey(Course)
    learning_object_type = models.ForeignKey(LearningObjectType)
    uuid = models.TextField()
    title = models.TextField()
    description = models.TextField()
    content_xml = models.TextField()
    path_xml = models.TextField()
    mpath = models.TextField()
    url_path = models.TextField()
    parent_id = models.ForeignKey("self")
    copyright = models.TextField()
    xa_nr_views = models.TextField()
    xa_nr_attempts = models.IntegerField()
    xa_avg_grade = models.FloatField()
    xa_histogram_grade = models.FloatField()

class LearningObjectType(models.Model):
    learning_object = models.ForeignKey(LearningObject)
    name = models.TextField()
    
class Repository(models.Model):
    name = models.TextField()
    description = models.TextField()
    create_date = models.DateField()
    created_by = models.TextField()