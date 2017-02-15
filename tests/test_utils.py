import pytest
from copy import copy

from scrapytest.utils import MergingProxyDictionary, ImmutableMergingDictionary, find_first


def test_find_first_returns_none_on_condition_not_found():
    assert find_first({'foo': 'bar', 'baz': 'spam'}, lambda x, y: False) is None


def test_merging_dictionary_can_exist():
    dictionary = MergingProxyDictionary({})
    assert len(dictionary) == 0


def test_merging_dictionary_can_access_all_keys():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'})
    assert 'foo' in dictionary
    assert 'bar' in dictionary


def test_can_copy_merging_dictionary():
    dictionary = MergingProxyDictionary({'foo': 'bar'}, {'baz': 'ham'}, MergingProxyDictionary({'spam': 'glam'}))
    copy1 = copy(dictionary)
    assert 'foo' in copy1
    assert 'baz' in copy1
    assert 'spam' in copy1
    assert copy1 is not dictionary


def test_merging_dictionary_can_retrieve_values():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'})
    assert dictionary['foo'] == 'spam'
    assert dictionary['bar'] == 'ham'


def test_merging_dictionary_reports_correct_length():
    dictionary = MergingProxyDictionary()
    assert len(dictionary) == 0
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'})
    assert len(dictionary) == 2
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'foo': 'ham'})
    assert len(dictionary) == 1


def test_merging_dictionary_overrides_later_dictionaries_values():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'foo': 'ham'})
    assert dictionary['foo'] == 'spam'
    assert len(dictionary) == 1


def test_mutating_dictionaries_outside_affects_item_retrieval():
    other_dictionary = MergingProxyDictionary({})
    dictionary = MergingProxyDictionary({}, other_dictionary)
    assert len(dictionary) == 0
    other_dictionary['foo'] = 'bar'
    dictionary['ham'] = 'spam'
    assert len(dictionary) == 2
    assert 'foo' in dictionary
    assert 'ham' in dictionary


def test_merging_dictionary_can_return_values():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thank you mam'})
    values = dictionary.values()
    assert len(values) == 2
    assert 'spam' in values
    assert 'ham' in values
    assert 'thank you mam' not in values


def test_merging_dictionary_can_return_keys():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thank you mam'})
    keys = dictionary.keys()
    assert len(keys) == 2
    assert 'foo' in keys
    assert 'bar' in keys


def test_key_not_found_raises_key_error():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'})
    with pytest.raises(KeyError):
        # noinspection PyStatementEffect
        dictionary['not there']


def test_can_determine_whether_key_is_own():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'})
    assert dictionary.is_own_key('foo')
    assert not dictionary.is_own_key('bar')


def test_merging_dictionary_can_see_items():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thank you mam'})
    items = dictionary.items()
    assert len(items) == 2


def test_get_returns_default_on_no_key():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thank you mam'})
    assert dictionary.get('foo', 'bam') == 'spam'
    assert dictionary.get('bar', 'bam') == 'ham'
    assert dictionary.get('baz', 'bam') == 'bam'


def test_str_method_functioning():
    assert "'foo': 'bar'" in str(MergingProxyDictionary({'foo': 'bar'}, {'baz': 'spam'}))
    assert "'baz': 'spam'" in str(MergingProxyDictionary({'foo': 'bar'}, {'baz': 'spam'}))


def test_repr_method_functioning():
    assert "'foo': 'bar'" in repr(MergingProxyDictionary({'foo': 'bar'}, {'baz': 'spam'}))
    assert "'baz': 'spam'" in repr(MergingProxyDictionary({'foo': 'bar'}, {'baz': 'spam'}))


def test_can_set_item():
    dictionary = MergingProxyDictionary()
    dictionary['foo'] = 'bar'


def test_can_pop_item():
    dictionary = MergingProxyDictionary({'foo': 'bar'})
    pop = dictionary.popitem()
    assert pop == ('foo', 'bar')
    assert len(dictionary) == 0


def test_can_pop():
    dictionary = MergingProxyDictionary({'foo': 'bar'})
    pop = dictionary.pop('foo')
    assert pop == 'bar'
    assert len(dictionary) == 0
    pop = dictionary.pop('foo', 'spam')
    assert pop == 'spam'
    assert len(dictionary) == 0


def test_merging_dictionary_can_update():
    dictionary = MergingProxyDictionary({'foo': 'bar'})
    dictionary.update({'foo': 'baz', 'ham': 'spam'})
    assert dictionary['foo'] == 'baz'
    assert dictionary['ham'] == 'spam'


# noinspection PyStatementEffect
def test_merging_dictionary_can_clear_own_values_only():
    dictionary = MergingProxyDictionary({'baz': 'bar'}, {'spam': 'ham'})
    assert len(dictionary) == 2
    dictionary.clear()
    assert len(dictionary) == 1
    with pytest.raises(KeyError):
        dictionary['baz']
    assert dictionary['spam'] == 'ham'


def test_merging_dictionary_can_set_default():
    dictionary = MergingProxyDictionary({'foo': 'bar'})
    value = dictionary.setdefault('foo', 'baz')
    assert len(dictionary) == 1
    assert value == 'bar'
    value = dictionary.setdefault('ham', 'spam')
    assert len(dictionary) == 2
    assert value == 'spam'


def test_merging_dictionary_raises_exception_when_setting_item():
    dictionary = ImmutableMergingDictionary()
    with pytest.raises(Exception):
        dictionary['foo'] = 'bar'


def test_merging_dictionary_raises_exception_when_deleting_items():
    dictionary = ImmutableMergingDictionary({'foo': 'bar'})
    with pytest.raises(Exception):
        del dictionary['foo']


def test_pop_item_raises_exception():
    dictionary = ImmutableMergingDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thank you mam'})
    with pytest.raises(Exception):
        dictionary.popitem()


def test_set_default_raises_exception():
    dictionary = ImmutableMergingDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thank you mam'})
    with pytest.raises(Exception):
        dictionary.setdefault('doesnt', 'matter')


def test_pop_raises_exception():
    dictionary = ImmutableMergingDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thank you mam'})
    with pytest.raises(Exception):
        dictionary.pop('doesnt', 'matter')


def test_clear_raises_exception():
    dictionary = ImmutableMergingDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thank you mam'})
    with pytest.raises(Exception):
        dictionary.clear()


def test_update_raises_exception():
    dictionary = ImmutableMergingDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thank you mam'})
    with pytest.raises(Exception):
        dictionary.update({'foo': 'no'})


def test_merging_dictionary_does_not_skip_items():
    dictionary = MergingProxyDictionary({'foo': 'bar'}, MergingProxyDictionary({'baz': 'spam'}),
                                        MergingProxyDictionary({'bar': 'ham'}))
    assert ('foo', 'bar') in dictionary.items()
    assert ('baz', 'spam') in dictionary.items()
    assert ('bar', 'ham') in dictionary.items()


def test_merging_dictionary_can_access_own_items():
    dictionary = MergingProxyDictionary({'foo': 'bar'}, {'baz': 'spam'})
    assert dictionary.own_items() == {'foo': 'bar'}.items()


def test_merging_dictionary_can_access_own_keys():
    dictionary = MergingProxyDictionary({'foo': 'bar'}, {'baz': 'spam'})
    assert dictionary.own_keys() == {'foo': 'bar'}.keys()


def test_merging_dictionary_can_access_own_values():
    dictionary = MergingProxyDictionary({'foo': 'bar'}, {'baz': 'spam'})
    values = dictionary.own_values()
    assert len(values) == 1
    assert list(values)[0] == list({'foo': 'bar'}.values())[0]
