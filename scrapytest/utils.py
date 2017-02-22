# -*- coding: utf-8 -*-
"""
    utils.py

    Copyright 2017 CodeRatchet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
"""

from copy import copy


def find_first(dictionary, condition):
    """ utility for finding the first occurrence of a passing condition for a key and value pair in a dict """
    for key, value in dictionary.items():
        if condition(key, value):
            return key, value
    return None


class MergingProxyDictionary(dict):
    """
    A MergingProxyDictionary allows for the merging of dictionaries without copying their values. for this reason,
    mutation of the contained dictionaries is not allowed directly through this class's interface. changing the
    referenced dictionaries outside this class will be reflected when accessing the keys through this interface. The
    dictionary will resolve keys with left to right priority on dictionaries provided in the __init__ function.
    """

    def __init__(self, initial_values=None, *args):
        """
        :param list[dict] args: the dictionaries to proxy against. key and value resolution is done in the order
        provided to this init function (left to right).
        """
        self._others = None
        if len(args) > 0:
            for arg in args:
                if isinstance(arg, MergingProxyDictionary):
                    self._append_others(arg)
                else:
                    self._append_others(MergingProxyDictionary(initial_values=arg))
        if initial_values is None:
            super(MergingProxyDictionary, self).__init__()
        else:
            super(MergingProxyDictionary, self).__init__(initial_values)

    def own_items(self):
        return super(MergingProxyDictionary, self).items()

    def own_keys(self):
        return super(MergingProxyDictionary, self).keys()

    def own_values(self):
        return super(MergingProxyDictionary, self).values()

    def _append_others(self, item):
        if self._others:
            return self._others.append(item)
        else:
            self._others = [item]
            return self._others

    def __getitem__(self, item):
        try:
            return super(MergingProxyDictionary, self).__getitem__(item)
        except KeyError as error:
            if self._others:
                for other in self._others:
                    try:
                        return other[item]
                    except KeyError:
                        pass
            raise error

    def __contains__(self, item):
        in_me = super(MergingProxyDictionary, self).__contains__(item)
        if not in_me and self._others:
            return any(find_first(other, lambda key, _: item == key) for other in self._others)
        return in_me

    def __copy__(self):
        _copy = {}
        if self._others:
            for other in reversed(self._others):
                _copy.update(copy(other))
        _copy.update(super(MergingProxyDictionary, self).copy())
        return _copy

    def copy(self):
        return copy(self)

    def __len__(self):
        return sum(1 for _ in self.keys())

    def __str__(self):
        return str(self.copy())

    def __repr__(self):
        return repr(self.copy())

    def get(self, key, default=None):
        try:
            return super(MergingProxyDictionary, self).__getitem__(key)
        except KeyError:
            if self._others:
                for other in self._others:
                    try:
                        return other[key]
                    except KeyError:
                        pass
        return default

    # noinspection PyMethodOverriding
    def values(self):
        return self.copy().values()

    def keys(self):
        s = set(super(MergingProxyDictionary, self).keys())
        if self._others:
            [s.update(other.keys()) for other in self._others]
        return s
        # return self.copy().keys()

    def items(self):
        return self.copy().items()

    def is_own_key(self, key):
        return key in super(MergingProxyDictionary, self).keys()


class ImmutableMergingDictionary(MergingProxyDictionary):
    """ 'Immutable'. raises AccessError on an attempt to mutate, otherwise the same as |MergingProxyDictionary| """

    def __delitem__(self, key):
        """ :raises AccessError: when attempting to call this function. """
        raise Exception(self.__class__)

    def __setitem__(self, key, value):
        """ :raises AccessError: when attempting to call this function. """
        raise Exception(self.__class__)

    def update(self, other=None, **kwargs):
        """ :raises AccessError: when attempting to call this function. """
        raise Exception(self.__class__)

    def popitem(self):
        """ :raises AccessError: when attempting to call this function. """
        raise Exception(self.__class__)

    def setdefault(self, key, default=None):
        """ :raises AccessError: when attempting to call this function. """
        raise Exception(self.__class__)

    def pop(self, key, default=None):
        """ :raises AccessError: when attempting to call this function. """
        raise Exception(self.__class__)

    def clear(self):
        """ :raises AccessError: when attempting to call this function. """
        raise Exception(self.__class__)


def merge_dict(source, destination):
    """
    merges dictionaries with priority given to the key values of destination

    >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
    >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
    >>> merge_dict(b, a) == { 'first' : { 'all_rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
    True
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge_dict(value, node)
        else:
            destination[key] = value

    return destination
