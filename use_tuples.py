from turtledemo.penrose import draw
from hypothesis.strategies import composite
from hypothesis import given, strategies as st
"""
1.元组的性质：tuples生成固定长度且每个位置类型可不同的结构。lists生成可变长度但所有元素类型相同的序列。
2.本身需要结合composite和lists使用，单独使用价值不高。待挖掘
"""

# 生成元素为整数、长度可变（但同质）的元组
variable_length_int_tuple = st.lists(st.integers()).map(tuple)


@composite
def dynamic_tuples(draw):
    # 首先决定元组长度
    n = draw(st.integers(min_value=1, max_value=5))
    # 然后根据长度n，依次绘制n个（可能是不同类型的）值，并组成元组
    drawn_elements = []
    for i in range(n):
        # 可以为不同索引选择不同的策略
        if i % 2 == 0:
            drawn_elements.append(draw(st.integers()))
        else:
            drawn_elements.append(draw(st.text()))
    return tuple(drawn_elements)

# 使用策略进行测试
@given(dynamic_tuples())
def test_dynamic_tuples(my_tuple):
    print(f"生成的元组: {my_tuple}")
    # 验证元组长度在1到5之间
    assert 1 <= len(my_tuple) <= 5
    # 验证每个元素类型
    for i, element in enumerate(my_tuple):
        if i % 2 == 0:
            assert isinstance(element, int)
        else:
            assert isinstance(element, str)