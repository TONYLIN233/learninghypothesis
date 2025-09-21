from hypothesis import given, strategies as st, note,assume

@given(st.integers(min_value=1, max_value=100))
def test_integers_in_range(n):
    """
    1.min_value=1, max_value=100依照这个范围随机取数执行100次，
    2.一定要使用 min_value，max_value确定发范围不然会造成无线循环的问题
    3.结合assume使用，过滤掉一些特殊值，如示例test_division_by_non_zero
    4.使用note作为执行自动化用例失败的时候调试用
    5.使用控制台命令执行用例 pytest use_integers.py -s
    """
    note(f"n is: {n}")  # 特别记录 n 的值，失败时显示
    print(f"打印出整数值{n}")
    assert 1 <= n <= 100

@given(st.integers())
def test_division_by_non_zero(n):
    assume(n != 0)  # 假设n不为0，过滤掉n=0的情况
    #
    # 现在可以安全地进行除以n的测试
    assert (10 / n) is not None

"""过滤的几种写法"""
@given(st.integers())
def test_filter_multiple_values(n):
    # 假设 n 不在 [0, 1, 2, 3, 4, 10] 这个列表中，过滤掉这些值
    assume(n not in [0, 1, 2, 3, 4, 10])
    # 现在可以安全地进行除以n的测试
    assert n != [0, 1, 2, 3, 4, 10]
@given(st.integers())
def test_filter_multiple_values(n):
    multiple_values = [0, 1, 2, 3, 4, 10]
    # 假设 n 不在 [0, 1, 2, 3, 4, 10] 这个列表中，过滤掉这些值
    assume(n not in multiple_values)
    # 现在可以安全地进行除以n的测试
    assert n != [0, 1, 2, 3, 4, 10]


values_to_filter = [0, 1, 2, 3, 4, 10]
@given(st.integers().filter(lambda x: x not in values_to_filter))#设置有效值，这个用法不适合设置比较严格的条件
def test_with_filter_strategy(n):
    # 参数 n 已经不会是 0, 1, 2, 3, 4, 10 了
    assert n != [0, 1, 2, 3, 4, 10]