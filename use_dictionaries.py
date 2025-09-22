from hypothesis import given, strategies as st
"""
1.本人常采用lists.map(lambda lst: [{"key": k, "value": v} for d in lst for k, v in d.items()]),直接使用lists转为字典。
2.dict_class: 默认值type = dict,有以下几种：defaultdict，OrderedDict，ChainMap，Counter，UserDict；感觉没有什么用，
3.min_size,max_size 取值范围
4.键的唯一性: 字典自动保证键的唯一性，即使键策略可能生成重复值
5.键的可哈希性: 键策略必须生成可哈希的对象
6.默认行为: 默认情况下可以生成空字典，使用 min_size=1来避免空字典
"""
# 生成字符串键和整数值的字典
@given(st.dictionaries(st.text(), st.integers()))
def test_string_key_int_value_dicts(d):
    print(f"字典: {d}")
    assert isinstance(d, dict)
    for k, v in d.items():
        assert isinstance(k, str)
        assert isinstance(v, int)

# 生成包含 1-5 个键值对的字典
@given(st.dictionaries(st.text(), st.integers(), min_size=1, max_size=5))
def test_bounded_size_dicts(d):
    print(f"有限大小字典: {d}")
    assert 1 <= len(d) <= 5

# 生成字符串键和整数列表值的字典
@given(st.dictionaries(st.text(), st.lists(st.integers())))
def test_dicts_with_list_values(d):
    print(f"字典: {d}")
    for k, v in d.items():
        assert isinstance(k, str)
        assert isinstance(v, list)
        assert all(isinstance(x, int) for x in v)

# 生成整数键和字符串值的字典
@given(st.dictionaries(st.integers(), st.text()))
def test_integer_key_dicts(d):
    print(f"整数键字典: {d}")
    for k, v in d.items():
        assert isinstance(k, int)
        assert isinstance(v, str)


# 生成具有唯一键的字典（默认行为）
@given(st.dictionaries(st.text(min_size=1), st.integers()))
def test_dicts_with_unique_keys(d):
    print(f"唯一键字典: {d}")
    # 字典自动保证键的唯一性
    keys = list(d.keys())
    assert len(keys) == len(set(keys))  # 所有键都是唯一的