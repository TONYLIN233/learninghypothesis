import uuid
from datetime import datetime, timezone, timedelta, time
from fractions import Fraction

from hypothesis import given, strategies as st
from datetime import date
"""
1.email()-生成邮箱
2.uuid()-生成uuid
3.ip_addresses()-生成IP地址
4.dates()- 生成日期对象
5.datetimes()- 生成日期时间对象
6.times()- 生成时间对象
7.timedeltas()- 生成时间间隔对象
8.decimals()- 生成十进制小数对象
9.fractions()- 生成分数对象
"""

#email
# 示例1：完全随机生成
# email_strategy = st.emails()

# 示例2：自定义用户名和域名
# email_custom = st.emails(
#     username=st.text(min_size=3, max_size=15, alphabet="abcdefghijklmnopqrstuvwxyz0123456789_-."),
#     domain=st.sampled_from(["example.com", "test.org", "my-domain.net"])
# )

# # 示例3：使用内置常见域名列表提高真实度
# common_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com"]
# email_with_common_domains = st.emails(domain=st.sampled_from(common_domains))
#
# # uuid
# # 示例1：生成随机的UUIDv4（最常用）
# uuid_strategy = st.uuids()
#
# # 示例2：生成基于版本和命名空间的UUID
# uuid_v5 = st.uuids(version=5, namespace=uuid.NAMESPACE_DNS, name="example.com")
#
# # 示例3：生成特定版本的UUID
# uuid_v1 = st.uuids(version=1)  # 基于时间戳和MAC地址
#
# # IP Addresses
# # 示例1：生成随机IPv4或IPv6地址
# ip_strategy = st.ip_addresses()
#
# # 示例2：仅生成IPv4地址
# ipv4_only = st.ip_addresses(version="v4")
#
# # 示例3：生成特定网络内的IP（如私有网络）
# ip_in_private_network = st.ip_addresses(version="v4", network="192.168.0.0/16")

# 示例4：生成指定范围内的IP
# ip_in_range = st.ip_addresses(version="v4", min_value="10.0.0.1", max_value="10.0.0.100")



# dates
# 基本用法
@given(st.dates())
def test_dates_basic(d):
    print(f"生成的日期: {d}")
    assert isinstance(d, date)
    assert date(1, 1, 1) <= d <= date(9999, 12, 31)#这也是dates的最小-最大的范围

# 限制日期范围
@given(st.dates(min_value=date(2020, 1, 1), max_value=date(2020, 12, 31)))
def test_dates_2020(d):
    print(f"2020年的日期: {d}")
    assert date(2020, 1, 1) <= d <= date(2020, 12, 31)
    assert d.year == 2020


# datetimes
# 基本用法
@given(st.datetimes())
def test_datetimes_basic(dt):
    print(f"生成的日期时间: {dt}")
    assert isinstance(dt, datetime)

# 限制日期时间范围
@given(st.datetimes(
    min_value=datetime(2020, 1, 1, 0, 0, 0),
    max_value=datetime(2020, 12, 31, 23, 59, 59)
))
def test_datetimes_2020(dt):
    print(f"2020年的日期时间: {dt}")
    assert dt.year == 2020

# 使用时区
@given(st.datetimes(timezones=st.just(timezone.utc)))
def test_datetimes_with_timezone(dt):
    print(f"带时区的日期时间: {dt}")
    assert dt.tzinfo == timezone.utc



# timedeltas
# 基本用法
@given(st.times())
def test_times_basic(t):
    print(f"生成的时间: {t}")
    assert isinstance(t, time)

# 限制时间范围（只生成工作时间）
@given(st.times(
    min_value=time(9, 0, 0),
    max_value=time(17, 0, 0)
))
def test_business_hours(t):
    print(f"工作时间: {t}")
    assert time(9, 0, 0) <= t <= time(17, 0, 0)


from hypothesis import given, strategies as st
from decimal import Decimal, InvalidOperation

# decimals
# 基本用法
@given(st.decimals())
def test_decimals_basic(d):
    print(f"生成的十进制小数: {d}")
    assert isinstance(d, Decimal)


# 限制范围和精度
@given(st.decimals(
    min_value=Decimal('0.0'),
    max_value=Decimal('100.0'),
    places=2  # 限制为2位小数
))
def test_bounded_decimals(d):
    print(f"有界十进制小数: {d}")
    assert Decimal('0.0') <= d <= Decimal('100.0')

    # 检查小数位数
    try:
        # 转换为字符串并检查小数部分
        s = str(d)
        if '.' in s:
            decimal_places = len(s.split('.')[1])
            assert decimal_places <= 2
    except InvalidOperation:
        pass  # 处理特殊情况如无穷大


# 排除特殊值
@given(st.decimals(allow_nan=False, allow_infinity=False))
def test_finite_decimals(d):
    print(f"有限十进制小数: {d}")
    # 确保不是 NaN 或无穷大
    assert not d.is_nan()
    assert not d.is_infinite()




# fractions
# 基本用法
@given(st.fractions())
def test_fractions_basic(f):
    print(f"生成的分数: {f}")
    assert isinstance(f, Fraction)


# 限制范围和分母大小
@given(st.fractions(
    min_value=Fraction(0, 1),
    max_value=Fraction(1, 1),
    max_denominator=100
))
def test_unit_fractions(f):
    print(f"单位分数: {f}")
    assert 0 <= f <= 1
    assert f.denominator <= 100  # 分母不超过100


# 测试分数运算
@given(st.fractions(), st.fractions())
def test_fraction_operations(f1, f2):
    print(f"分数1: {f1}, 分数2: {f2}")

    # 测试加法
    try:
        sum_result = f1 + f2
        print(f"和: {sum_result}")
    except (OverflowError, ZeroDivisionError):
        pass  # 处理可能的异常

    # 测试乘法
    try:
        product = f1 * f2
        print(f"积: {product}")
    except (OverflowError, ZeroDivisionError):
        pass  # 处理可能的异常