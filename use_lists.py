from hypothesis import given, strategies as st
"""
1.elements:基本可以
"""
# 生成整数列表
@given(st.lists(st.integers()))
def test_integer_lists(lst):
    print(f"整数列表: {lst}")
    assert isinstance(lst, list)
    assert all(isinstance(x, int) for x in lst)

# 生成包含 1-5 个整数的列表
@given(st.lists(st.integers(), min_size=1, max_size=5))
def test_bounded_size_lists(lst):
    print(f"有限大小列表: {lst}")
    assert 1 <= len(lst) <= 5