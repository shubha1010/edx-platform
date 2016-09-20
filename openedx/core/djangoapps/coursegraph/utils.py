"""
Helpers for the CourseGraph app
"""
from django.core.cache import cache
from django.utils import timezone


class TimeRecordingCacheBase(object):
    """
    A base class for caching the current time for some key.
    """
    # cache_prefix should be defined in children classes
    cache_prefix = None
    _cache = cache

    def _key(self, course_key):
        """
        Make a cache key from the prefix and a course_key
        :param course_key: CourseKey object
        :return: a cache key
        """
        return self.cache_prefix + unicode(course_key)

    def get(self, course_key):
        return self._cache.get(self._key(course_key))

    def set(self, course_key):
        return self._cache.set(self._key(course_key), timezone.now())


class CourseLastPublishedCache(TimeRecordingCacheBase):
    """
    Used to record the last time that a course had a publish event run on it.
    """
    cache_prefix = u'course_last_published'


class CommandLastRunCache(TimeRecordingCacheBase):
    """
    Used to record the last time that the dump_to_neo4j command was run on a
    course.
    """
    cache_prefix = u'dump_to_neo4j_command_last_run'
