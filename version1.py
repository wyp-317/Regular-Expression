# 正则表达式.py
import re
from typing import Dict, Optional


def clean_text(text: str) -> str:
    """清理多余字符，将各种标点符号统一切换为空格，压缩多个连续空格"""
    text = text.strip()
    text = re.sub(r"[，,;；|/]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def extract_phone(text: str) -> Optional[str]:
    """
    提取手机号：使用负向断言确保11位数字前后没有其他数字
    """
    pattern = r"(?<!\d)(1[3-9]\d{9})(?!\d)"
    match = re.search(pattern, text)
    return match.group(1) if match else None


def remove_phone(text: str, phone: Optional[str]) -> str:
    if not phone:
        return text
    return text.replace(phone, " ")


def extract_address_parts(text: str) -> Dict[str, Optional[str]]:
    """
    使用极其严格的正则组提取省、市、区、详细地址。
    包含了直辖市无省份、少字等常见边界情况。
    """
    result = {
        "province": None,
        "city": None,
        "district": None,
        "detail": None
    }

    # 运用命名捕获组 (?P<name>...) 以及非捕获组 (?:...)
    full_pattern = (
        r"^\s*"
        # 匹配省份/直辖市/自治区（直辖市后续可能没有市字）
        r"(?:(?P<province>[\u4e00-\u9fa5]{2,8}?(?:省|自治区|特别行政区)|内蒙古(?:自治区)?|(?:北京|天津|上海|重庆)(?:市)?)\s*)?"
        # 匹配城市
        r"(?:(?P<city>[\u4e00-\u9fa5]{1,8}?(?:市|自治州|地区|盟))\s*)?"
        # 匹配区县
        r"(?:(?P<district>[\u4e00-\u9fa5]{1,8}?(?:区|县|市|旗|自治县|林区|特区))\s*)?"
        # 剩余全部为详细地址
        r"(?P<detail>.*)$"
    )

    match = re.search(full_pattern, text)

    if match:
        result["province"] = match.group("province")
        result["city"] = match.group("city")
        result["district"] = match.group("district")

        detail = match.group("detail")
        result["detail"] = detail.strip() if detail else None

    return result


def parse_receiver_info(text: str) -> Dict[str, Optional[str]]:
    original = text
    text = clean_text(text)

    # 1. 提取并移除手机号
    phone = extract_phone(text)
    if phone:
        text = remove_phone(text, phone)
    text = text.strip()

    # 2. 提取姓名并从文本中分离地址
    # 通过空格切块寻找不包含地址特征的独立短词作为姓名
    parts = text.split()
    name = None
    address_parts = []

    # 常见地址特征后缀，用于排除非姓名词汇
    not_name_suffix_pattern = r"(?:省|市|区|县|镇|街道|路|号|村|大厦|室|楼|广场|园)$"

    for part in parts:
        # 姓名特征：长度2~4，且不包含省市区等地址特征后缀
        if not name and 2 <= len(part) <= 4 and not re.search(not_name_suffix_pattern, part):
            name = part
        else:
            address_parts.append(part)

    address_text = " ".join(address_parts)

    # 3. 兜底策略：如果没有通过空格区分开（比如所有的字粘连在一起）
    # 使用正则表达式的正向先行断言 (?=...) 强制提取地址前方的 2~4 个汉字
    if not name and address_text:
        fallback_pattern = r"^([\u4e00-\u9fa5]{2,4}?)(?=(?:[\u4e00-\u9fa5]{2,8}?(?:省|市|自治区|特别行政区)|北京|天津|上海|重庆|内蒙古))"
        match = re.match(fallback_pattern, address_text)
        if match:
            name = match.group(1)
            address_text = address_text[len(name):].strip()

    # 4. 提取地址组件
    parsed_address = extract_address_parts(address_text)

    return {
        "original_text": original,
        "name": name,
        "phone": phone,
        "province": parsed_address["province"],
        "city": parsed_address["city"],
        "district": parsed_address["district"],
        "detail": parsed_address["detail"],
    }


if __name__ == "__main__":
    print("=" * 50)
    print(" 📦 快递收件信息正则解析器 (编译原理小组作业)")
    print("=" * 50)
    print("支持自动识别 姓名、手机号、省市区及详细地址！")
    print("支持乱序输入（如：地址 手机号 姓名）。")
    print("输入 'q', 'quit' 或 'exit' 退出程序。\n")
    print("【测试示例】")
    print("1. 张三，13812345678，广东省深圳市南山区粤海街道科技园科苑路15号")
    print("2. 北京市海淀区中关村大街27号 13700001111 王五")
    print("-" * 50)

    # 交互式输入循环
    while True:
        try:
            user_input = input("\n👉 请输入收件信息: ").strip()

            # 退出指令
            if user_input.lower() in ['q', 'quit', 'exit']:
                print("程序已退出。祝编译原理拿高分！👋")
                break

            # 过滤空输入
            if not user_input:
                continue

            # 调用正则解析
            result = parse_receiver_info(user_input)

            # 格式化输出结果
            print("\n" + "-" * 30 + " 解析结果 " + "-" * 30)
            key_map = {
                "original_text": "原始文本",
                "name": "姓    名",
                "phone": "手 机 号",
                "province": "省    份",
                "city": "城    市",
                "district": "区 /  县",
                "detail": "详细地址"
            }
            for k, v in result.items():
                print(f"🔹 {key_map.get(k, k)} : {v if v else '（未提取到）'}")
            print("-" * 70)

        except KeyboardInterrupt:
            # 拦截 Ctrl+C 导致的报错
            print("\n程序已退出。👋")
            break