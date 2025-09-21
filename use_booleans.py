from hypothesis import given, strategies as st


@given(st.booleans())
def test_boolean_properties(boolean):
    """
    1.比较少接口直接使用True or False的表达，查用0,1之类的，方便拓展其他状态
    2.Ture or False的使用难度比较大，在之前的接口使用的时候，发现if，else的条件也不好写
    """
    # 测试布尔值只能是 True 或 False
    assert boolean in (True, False)

    # 测试布尔值的否定操作
    assert not (boolean and not boolean)  # 排中律：不可能同时为真和假
    assert boolean or not boolean  # 排中律：总是为真

    print(f"测试值: {boolean}")



