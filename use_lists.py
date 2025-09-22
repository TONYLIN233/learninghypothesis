from hypothesis import given, strategies as st
from dataclasses import dataclass
"""
1.elements:所有入参基本可以都可以，常用st.integers(), st.text(), st.floats,st.booleans()
2.min_size,max_size 取值范围，int型
3.unique_by: 用于确定元素唯一性的函数，通过函数对生成数据的某一个部分进行唯一处理，应用场景更广泛，要求代码熟练度高。
4.unique: 默认bool = False,是否要求列表中的所有元素唯一,推荐带入True，性能要求高可能导致用例执行缓慢。
5.示例中有详细对unique_by和unique对比及说明
6.默认情况下可以生成空列表，使用 min_size=1来避免空列表,接口接受空list的时，一般会有特殊返回值。空list最好作为单独的测试情况
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

# 生成唯一整数的列表
@given(st.lists(st.integers(), unique=True))
def test_unique_integer_lists(lst):
    print(f"唯一元素列表: {lst}")
    assert len(lst) == len(set(lst))  # 验证元素唯一性

"""下面是unique_by的一些示例"""
# 基于元素的绝对值判断唯一性
@given(st.lists(st.integers(), unique_by=abs))
def test_unique_by_abs(lst):
    print(f"绝对值唯一列表: {lst}")
    abs_values = [abs(x) for x in lst]
    assert len(abs_values) == len(set(abs_values))



@dataclass
class User:
    username: str
    age: int

# 生成具有唯一用户名的用户列表
user_strategy = st.lists(
    st.builds(
        User,
        username=st.text(min_size=3, max_size=20),
        age=st.integers(min_value=0, max_value=120)
    ),
    min_size=1,
    max_size=10,
    unique_by=lambda user: user.username  # 确保用户名唯一
)

@given(user_strategy)
def test_unique_usernames(users):
    # 验证所有用户名都是唯一的
    usernames = [user.username for user in users]
    assert len(usernames) == len(set(usernames))
    print(f"测试通过: {[user.username for user in users]}")



# 生成字典，其中值的某个属性是唯一的
unique_dict_strategy = st.lists(
    st.tuples(
        st.text(min_size=1, max_size=10),  # 键的策略
        st.integers(min_value=1, max_value=100)  # 值的策略
    ),
    min_size=1,
    max_size=5,
    unique_by=lambda x: x[1]  # 指定根据元组的第二个元素（即值）进行唯一性检查
).map(dict)  # 将生成的键值对列表转换为字典

@given(unique_dict_strategy)
def test_unique_values_in_dict(test_dict):
    # 验证字典中的所有值都是唯一的
    values = list(test_dict.values())
    assert len(values) == len(set(values)), f"发现重复值: {test_dict}"
    print(f"字典: {test_dict}")



case_insensitive_strategy = st.lists(
    st.text(min_size=1, max_size=10),
    min_size=1,
    max_size=8,
    unique_by=lambda s: s.lower()  # 不区分大小写的唯一性
)

@given(case_insensitive_strategy)
def test_case_insensitive_unique(strings):
    # 验证小写版本都是唯一的
    lower_strings = [s.lower() for s in strings]
    assert len(lower_strings) == len(set(lower_strings))
    print(f"字符串: {strings}")
    print(f"小写形式: {lower_strings}")

"""
# unique=True 相当于 unique_by=lambda x: x
# 但 unique_by 更灵活，可以处理复杂的情况
"""
# 这样是等价的:
st.lists(st.integers(), unique=True)
st.lists(st.integers(), unique_by=lambda x: x)

# 但这样更强大:
st.lists(st.integers(), unique_by=lambda x: x % 10)  # 最后一位数字唯一