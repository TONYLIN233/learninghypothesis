from hypothesis import given, strategies as st, note
import pytest

@given(st.integers(min_value=1, max_value=100))
def test_integers_in_range(n):
    """
    1.min_value=1, max_value=100依照这个范围随机取数执行100次，
    2.一定要使用 min_value，max_value确定发范围不然会造成无线循环的问题，
    3.使用note作为执行自动化用例失败的时候调试用
    4.使用控制台命令执行用例 pytest use_integers.py -s
    """
    note(f"n is: {n}")  # 特别记录 n 的值，失败时显示
    print(f"打印出整数值{n}")
    assert 1 <= n <= 100
