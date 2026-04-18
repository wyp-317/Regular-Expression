import re
from typing import Dict, Optional


def clean_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"[，,;；|/]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def extract_phone(text: str) -> Optional[str]:
    pattern = r"(?<!\d)(1[3-9]\d{9})(?!\d)"
    match = re.search(pattern, text)
    return match.group(1) if match else None


def remove_phone(text: str, phone: Optional[str]) -> str:
    if not phone:
        return text
    return text.replace(phone, " ")


def extract_name(text: str) -> Optional[str]:
    """
    粗略提取姓名：默认取开头连续的2~4个中文字符作为姓名
    """
    pattern = r"^\s*([\u4e00-\u9fa5]{2,4})"
    match = re.search(pattern, text)
    return match.group(1) if match else None


def extract_address_parts(text: str) -> Dict[str, Optional[str]]:
    result = {
        "province": None,
        "city": None,
        "district": None,
        "detail": None
    }

    province_pattern = (
        r"(?P<province>"
        r"(?:[\u4e00-\u9fa5]{2,8}省)"
        r"|(?:内蒙古自治区|广西壮族自治区|宁夏回族自治区|西藏自治区|新疆维吾尔自治区)"
        r"|(?:北京市|天津市|上海市|重庆市)"
        r"|(?:香港特别行政区|澳门特别行政区)"
        r")?"
    )

    city_pattern = (
        r"(?P<city>"
        r"(?:[\u4e00-\u9fa5]{2,8}市)"
        r"|(?:[\u4e00-\u9fa5]{2,8}自治州)"
        r"|(?:[\u4e00-\u9fa5]{2,8}地区)"
        r"|(?:[\u4e00-\u9fa5]{2,8}盟)"
        r")?"
    )

    district_pattern = (
        r"(?P<district>"
        r"(?:[\u4e00-\u9fa5]{1,8}区)"
        r"|(?:[\u4e00-\u9fa5]{1,8}县)"
        r"|(?:[\u4e00-\u9fa5]{1,8}市)"
        r"|(?:[\u4e00-\u9fa5]{1,8}旗)"
        r"|(?:[\u4e00-\u9fa5]{1,8}自治县)"
        r")?"
    )

    detail_pattern = r"(?P<detail>.*)"

    full_pattern = province_pattern + city_pattern + district_pattern + detail_pattern
    match = re.search(full_pattern, text)

    if match:
        result["province"] = match.group("province") or None
        result["city"] = match.group("city") or None
        result["district"] = match.group("district") or None

        detail = (match.group("detail") or "").strip(" ,，;；")
        result["detail"] = detail if detail else None

    return result


def parse_receiver_info(text: str) -> Dict[str, Optional[str]]:
    original = text
    text = clean_text(text)

    phone = extract_phone(text)
    text_wo_phone = remove_phone(text, phone).strip()

    name = extract_name(text_wo_phone)

    if name:
        address_text = re.sub(rf"^\s*{re.escape(name)}", "", text_wo_phone, count=1).strip()
    else:
        address_text = text_wo_phone

    address_text = re.sub(r"^[,\s，;；]+", "", address_text)

    address_parts = extract_address_parts(address_text)

    return {
        "original_text": original,
        "name": name,
        "phone": phone,
        "province": address_parts["province"],
        "city": address_parts["city"],
        "district": address_parts["district"],
        "detail": address_parts["detail"],
    }


if __name__ == "__main__":
    samples = [
        "张三，13812345678，广东省深圳市南山区粤海街道科技园科苑路15号讯美科技广场3栋5楼",
        "李四 13988887777 浙江省杭州市西湖区文三路90号东部软件园创新大厦1202室",
        "王五, 13700001111, 北京市海淀区中关村大街27号",
        "赵六 13666668888 上海市浦东新区张江路100号",
        "孙七，13512341234，广西壮族自治区南宁市青秀区民族大道88号"
    ]

    for s in samples:
        result = parse_receiver_info(s)
        print("=" * 60)
        for k, v in result.items():
            print(f"{k}: {v}")