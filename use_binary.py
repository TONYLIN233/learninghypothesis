from hypothesis import given, strategies as st, example

"""
1.入参有min_size，max_size二进制数据的长度
2.并非常用作为了解，遇到需要使用的情况再做补充
"""
def parse_packet(data: bytes) -> bytes:
    """一个可能有bug的解析器：从数据包中提取数据部分。"""
    if len(data) < 2:
        raise ValueError("Packet too short")
    length = int.from_bytes(data[:2], 'big')
    if len(data) < 2 + length:
        raise ValueError("Packet data incomplete")
    return data[2:2+length]

def build_packet(payload: bytes) -> bytes:
    """构建数据包：长度 + 负载"""
    length_bytes = len(payload).to_bytes(2, 'big')
    return length_bytes + payload




@given(st.binary(max_size=1000)) # 生成最大1000字节的测试数据
@example(b'')                    # 确保测试空数据
@example(b'\x00\x01\xff')        # 确保测试一个特定案例
def test_packet_round_trip(payload):
    # 属性测试：构建数据包再解析，应该得到原始负载
    packet = build_packet(payload)
    assert parse_packet(packet) == payload


# 一个更针对解析器错误处理的测试
@given(st.data())
def test_parse_packet_robustness(data):
    # 生成任意的、可能是损坏的二进制数据
    random_data = data.draw(st.binary(min_size=0, max_size=2000))
    try:
        # 如果解析器没崩溃，结果应该满足一些条件
        result = parse_packet(random_data)
        # 例如，结果应该是bytes，并且长度不能大于输入长度减2
        assert isinstance(result, bytes)
        assert len(result) <= len(random_data) - 2
    except ValueError:
        # 解析器抛出ValueError是预期行为之一（对于无效输入）
        pass