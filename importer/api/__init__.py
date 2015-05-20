"""
Import OLX data into LORE.
"""

from glob import glob
from datetime import datetime
from shutil import rmtree
from tempfile import mkdtemp
from os.path import join

from xbundle import XBundle, DESCRIPTOR_TAGS
from lxml import etree
from archive import extract, ArchiveException

from learningobjects.api import create_course, create_lox


def import_course_from_file(filename, user_id):
    """
    Import OLX from .zip or tar.gz.

    Args:
        filename (unicode): Path to archive file (zip or .tar.gz)
    Raises:
        ValueError: Unable to extract or read archive contents.
    Returns: None
    """
    tempdir = mkdtemp()
    try:
        extract(path=filename, to_path=tempdir, method="safe")
    except ArchiveException:
        raise ValueError("Invalid OLX archive, unable to extract.")
    dirs = glob(join(tempdir, "*"))
    if len(dirs) != 1:
        raise ValueError("Invalid OLX archive, bad directory structure.")
    import_course_from_path(dirs[0], user_id)
    rmtree(tempdir)


def import_course_from_path(path, user_id):
    """
    Import course from an OLX directory.

    Args:
        path (unicode): path to extracted OLX tree
        user_id (int): pk of Django user doing the import
    """
    bundle = XBundle()
    bundle.import_from_directory(path)
    return import_course(bundle, user_id)


def import_course(bundle, user_id):
    """
    Import a course from an XBundle object.

    Args:
        bundle (xbundle.XBundle): Course as xbundle XML
        user_id (int): pk of Django user doing the import
    """
    src = bundle.course
    course = create_course(
        org=src.attrib["org"],
        course_number=src.attrib["course"],
        semester=src.attrib["semester"],
        user_id=user_id,
    )
    import_children(course, src, None)


def import_children(course, element, parent):
    """
    Create LearningObject instances for each element
    of an XML tree.

    Args:
        course (learningobjects.Course): Course
        element (lxml.etree): XML element within xbundle
        parent (learningobjects.LearningObject): parent LearningObject
    """
    lox = create_lox(
        course=course, parent=parent, lox_type=element.tag,
        title=element.attrib.get("display_name", "MISSING"),
        content_xml=etree.tostring(element),
    )
    for child in element.getchildren():
        if child.tag in DESCRIPTOR_TAGS:
            import_children(course, child, lox)