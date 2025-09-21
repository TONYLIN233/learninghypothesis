import math

from hypothesis import given, strategies as st, note

"""
  1.取值范围为 min_value，max_value,闭区间
  2.allow_nan为是否使用是否允许生成 NaN (Not a Number) 值，默认值：True，基本使用False实际上的取数是使用不到NaN
  3.allow_infinity是否允许生成无穷大 (±inf) 值，默认值：True 基本在自动化测中确定确定范围使用不到这个参数，不确定范围定位以False
  4.allow_subnormal是否允许生成次正规数（非常接近零的数），默认值：True 基本在自动化测中确定确定范围使用不到这个参数，不确定范围定位以False
  5.width浮点数的位宽，可以是 16, 32 或 64，默认值：64(双精度);FP64 (双精度),FP32 (单精度),FP16(半精度),
    精度越高内存占用最大，涉及入参的宽度可以限制，涉及用例进度缓慢推荐设置为32位
  6.取值范围exclude_min，exclude_max，开区间
  """
# 生成 0.0 到 1.0 之间的有限浮点数（不包括 NaN 和无穷大）
@given(st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False))
def test_unit_interval(x):
    assert 0.0 <= x <= 1.0
    print(f"Testing with: {x}")


# 生成正浮点数（不包括 0.0）
@given(st.floats(min_value=0.0, exclude_min=True, allow_nan=False, allow_infinity=False))
def test_positive_floats(x):
    assert x > 0.0
    print(f"Testing with positive: {x}")


# 生成任意浮点数（包括特殊值）
@given(st.floats())
def test_any_float(x):
    # 这个测试可能会收到 NaN、无穷大等特殊值
    print(f"Testing with any float: {x}")

    # 检查是否为特殊值
    if x != x:  # NaN 的唯一特性：NaN != NaN
        print("Got NaN")
    elif x == float('inf'):
        print("Got +inf")
    elif x == float('-inf'):
        print("Got -inf")
@given(st.floats(min_value=0.0, max_value=1.0).filter(lambda x: not math.isnan(x) and x != float('inf')))
#排除 NaN 和无穷大;等于示例1
def test_filter(x):
    assert 0.0 <= x <= 1.0
    print(f"Testing with: {x}")