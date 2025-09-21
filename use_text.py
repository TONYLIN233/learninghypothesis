
from hypothesis import given, strategies as st,assume

from email_validator import validate_email,EmailNotValidError
"""
1.alphabet非常实用的参数
    # 只使用字母字符st.text(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    # 只使用数字 st.text(alphabet='0123456789')
    # 使用自定义字符集 st.text(alphabet='abc123!@#')
    # 使用字符策略定义字母表 st.text(alphabet=st.characters(min_codepoint=65, max_codepoint=90))  # 只大写字母
2.生成字符串长度min_size，max_size
3.filter 排除特定字符
"""
@given(st.text())
def test_string_operations(s):
    # 测试字符串基本操作
    assert len(s) >= 0
    assert s == s
    assert s + "" == s
    print(f"Testing with: {repr(s)}")

@given(st.text(alphabet="abc", min_size=1, max_size=5))
def test_limited_alphabet(s):
    # 字符串只包含 a, b, c
    assert all(c in "abc" for c in s)
    assert 1 <= len(s) <= 5
    print(f"Testing with: {repr(s)}")

# 生成可能有效的电子邮件本地部分
email_local_part = st.text(
    alphabet=st.characters(
        min_codepoint=33,  # 从!开始，排除空格和控制字符
        max_codepoint=126, # ASCII可打印字符
        blacklist_characters='()<>@,;:\\"[]'  # 排除电子邮件中的特殊字符
    ),
    min_size=1,
    max_size=64
)
@given(email_local_part)
# 测试电子邮件本地部分处理
def test_email_local_part(local_part):
    mail_addr = f"{local_part}@126.com"
    try:
        validation_result = validate_email(mail_addr,check_deliverability=False)
        normalized_email = validation_result.email  # 获取标准化后的邮箱地址
        assert "@" in normalized_email
    except EmailNotValidError as e:
        assume(False)


# 使用 filter 方法排除包含非法字符的字符串
def is_valid_filename(s):
    illegal_chars = '<>:"/\\|?*'
    return all(c not in illegal_chars for c in s)

filename_text = st.text(
    min_size=1,
    max_size=10
).filter(is_valid_filename)

@given(filename_text)
def test_valid_filenames(s):
    # 确保字符串适合作为文件名
    illegal_chars = '<>:"/\\|?*'
    assert all(c not in illegal_chars for c in s)
    print(f"有效文件名: {repr(s)}")