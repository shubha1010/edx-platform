"""
An implementation of a RequestCache. This cache is reset at the beginning
and end of every request.
"""

import crum
import threading


class _RequestCache(threading.local):
    """
    A thread-local for storing the per-request cache.
    """
    def __init__(self):
        super(_RequestCache, self).__init__()
        self.data = {}


REQUEST_CACHE = _RequestCache()


class RequestCache(object):
    @classmethod
    def get_request_cache(cls, name=None):
        """
        This method is deprecated. Please use :func:`request_cache.get_cache`.
        """
        if name is None:
            return REQUEST_CACHE
        else:
            return REQUEST_CACHE.data.setdefault(name, {})

    @classmethod
    def get_current_request(cls):
        """
        This method is deprecated. Please use :func:`request_cache.get_request`.
        """
        return crum.get_current_request()

    @classmethod
    def clear_request_cache(cls):
        """
        Empty the request cache.
        """
        REQUEST_CACHE.data = {}

    def process_request(self, request):
        self.clear_request_cache()
        return None

    def process_response(self, request, response):
        self.clear_request_cache()
        return response

    def process_exception(self, request, exception):  # pylint: disable=unused-argument
        """
        Clear the RequestCache after a failed request.
        """
        self.clear_request_cache()
        return None


def request_cached(wrapped):
    """
    Wraps a function and automatically handles caching its return value, as well as
    returning that cached value for subsequent calls to the same function, with the
    same parameters, within a given request.

    Caveats:
        - we convert positional arguments to their string equivalent and use them in the cache key, so if something
          can't be converted to a string, things might blow up
        - our cache key depends on the positional args (so , holistically, cache efficiency is tied to cardinality)
        - we use the default request cache, not a named request cache
        - the cache key is prefixed with the name of the wrapped function, so theoretically, an identically named
          function elsewhere in the code with the same parameters could overwrite cached values
    """
    def wrapper(*args, **kwargs):
        """
        Wrapper function to decorate with.
        """

        # Build our cache key based on the name of the function we're wrapping
        # and the parameters passed in to it.  This could get a little dicey
        # but the intention is that the only functions being decorated with this
        # are akin to pure functions, where you're passing in simple values and
        # getting something out, and don't require full objects that you modify,
        # or anything like that.
        converted_params = map(str, args)
        cache_keys = [wrapped.func_name] + converted_params
        cache_key = '.'.join(cache_keys)

        # Check to see if we have a result in cache.  If not, invoke our wrapped
        # function.  If the result of that function call isn't None, then cache it.
        # Regardless, return the result to the caller.
        rcache = RequestCache.get_request_cache()

        cached_result = rcache.data.get(cache_key)
        if cached_result:
            return cached_result
        else:
            result = wrapped(*args, **kwargs)
            if result:
                rcache.data[cache_key] = result

            return result

    return wrapper
