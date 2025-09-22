from hypothesis import given, strategies as st
import struct
"""
1.从AI拿了几个示例，因为之前并未接触过相关的内容，仅供参考
2.min_codepoint，max_codepoint长度取值
3. 关于一些黑白名单，包括排除的用法仅做了解
    exclude_categories: Optional[Collection[CategoryName]] = None,
    exclude_characters: Optional[Collection[str]] = None,
    include_characters: Optional[Collection[str]] = None,
    blacklist_categories: Optional[Collection[CategoryName]] = None,
    whitelist_categories: Optional[Collection[CategoryName]] = None,
    blacklist_characters: Optional[Collection[str]] = None,
    whitelist_characters: Optional[Collection[str]] = None,
"""
def encode_message(data: bytes) -> bytes:
    """将数据编码为协议格式: [4字节长度][数据]"""
    length = len(data)
    # 使用网络字节序（大端）打包长度，确保跨平台一致性
    return struct.pack('>I', length) + data

def decode_message(packet: bytes) -> bytes:
    """从协议数据包中解码出原始数据"""
    if len(packet) < 4:
        raise ValueError("Packet too short to contain length header")
    # 提取头4字节并解包为长度整数
    (length,) = struct.unpack('>I', packet[:4])
    if len(packet) < 4 + length:
        raise ValueError("Packet body incomplete")
    return packet[4:4+length]

# 针对 6.139.2 版本的属性测试
@given(st.binary(max_size=2048))  # 生成最大2KB的随机二进制数据
def test_message_round_trip_original(data):
    """测试核心属性：编码后再解码，应得到原始数据。"""
    encoded = encode_message(data)
    decoded = decode_message(encoded)
    assert decoded == data

# 一个更健壮的压力测试，测试解析器对损坏数据的处理能力
@given(st.data())
def test_decode_robustness(data):
    """测试解码器处理任意（可能损坏的）二进制数据时不会崩溃。"""
    # 使用data()策略动态绘制测试用例
    random_binary_data = data.draw(st.binary(min_size=0, max_size=1024))
    try:
        result = decode_message(random_binary_data)
        # 如果解码成功，结果应该是bytes对象
        assert isinstance(result, bytes)
    except (ValueError, struct.error):
        # 预期中的异常，说明解析器正确处理了错误输入
        pass

from hypothesis import given, strategies as st
import re

def to_safe_filename(s: str) -> str:
    """将一个字符串转换为适合做文件名的格式。"""
    # 定义文件名中通常不允许的字符
    unsafe_chars = r'[<>:"/\\|?*\x00-\x1f]'
    # 替换掉非法字符，并去除首尾空格
    safe_name = re.sub(unsafe_chars, '_', s).strip()
    # 确保文件名不为空，如果为空则返回一个默认名称
    return safe_name if safe_name else 'unnamed'

# 1. 首先，定义一个生成“潜在不安全”字符的策略
# 这些字符在我们的规则里会被替换成下划线
unsafe_char_strategy = st.characters(
    # 包含控制字符 (Cc), 以及特定符号
    whitelist_categories=('Cc', 'Cs'),
    whitelist_characters='<>:"/\\|?*' # 直接列出要包含的ASCII字符
)

# 2. 定义一个生成“安全”字符的策略（字母、数字、常用标点）
safe_char_strategy = st.characters(
    whitelist_categories=('Lu', 'Ll', 'Nd', 'Pd', 'Pc'),
    whitelist_characters='-_. ',
    blacklist_characters='<>:"/\\|?*\x00-\x1f'
)

# 3. 创建一个混合策略，生成可能包含不安全字符的测试字符串
test_string_strategy = st.text(
    alphabet=st.one_of(unsafe_char_strategy, safe_char_strategy),
    min_size=1
)

# 针对 6.139.2 版本的属性测试
@given(test_string_strategy)
def test_to_safe_filename_properties(original_name):
    """测试安全文件名转换函数的几个关键属性。"""
    safe_name = to_safe_filename(original_name)

    # 属性 1: 返回值必须是字符串
    assert isinstance(safe_name, str)

    # 属性 2: 结果中不能包含任何非法字符
    assert not re.search(r'[<>:"/\\|?*\x00-\x1f]', safe_name)

    # 属性 3: 如果原始名称经过处理后不为空，结果不应是'unnamed'
    intermediate_name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', original_name).strip()
    if intermediate_name:
        assert safe_name != 'unnamed'
    else:
        assert safe_name == 'unnamed'

    # 属性 4: 结果的长度应小于或等于原字符串长度（因为只做替换和去除）
    assert len(safe_name) <= len(original_name)