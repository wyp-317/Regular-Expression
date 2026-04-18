# 正则表达式应用(以物流收货地址为例) / Chinese Receiver Info Parser

&lt;p align="center"&gt;
  &lt;b&gt;轻量级 | 零依赖 | 高精度&lt;/b&gt;&lt;br&gt;
  &lt;i&gt;从非结构化中文文本中智能提取收件人姓名、手机号与四级结构化地址&lt;/i&gt;
&lt;/p&gt;

&lt;p align="center"&gt;
  &lt;img src="https://img.shields.io/badge/python-3.6+-blue.svg" alt="Python 3.6+"&gt;
  &lt;img src="https://img.shields.io/badge/dependencies-zero-brightgreen.svg" alt="Zero Dependencies"&gt;
  &lt;img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License"&gt;
&lt;/p&gt;

---

## 📑 目录

- [功能特性](#功能特性)
- [快速开始](#快速开始)
- [安装与使用](#安装与使用)
- [API 文档](#api-文档)
- [正则表达式原理详解](#正则表达式原理详解)
- [实现原理](#实现原理)
- [测试用例](#测试用例)
- [已知局限](#已知局限)
- [性能基准](#性能基准)
- [常见问题](#常见问题)
- [更新日志](#更新日志)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## ✨ 功能特性

| 功能模块 | 说明 | 覆盖范围 |
|---------|------|---------|
| **文本预处理** | 智能清洗原始输入，统一多种分隔符 | 全角/半角逗号、分号、竖线、斜杠、多余空格 |
| **手机号提取** | 精准识别中国大陆手机号，自动边界过滤 | 1[3-9]开头的 11 位数字，防止长串数字误匹配 |
| **姓名识别** | 基于位置启发式提取收件人姓名 | 开头连续的 2-4 个中文字符 |
| **地址结构化** | 四级地址智能拆分 | 省/自治区/直辖市、市/自治州/地区、区/县/旗、详细街道 |

**核心优势：**
- 🚀 **纯标准库**：仅依赖 `re` 模块，无任何第三方包
- 🔒 **类型安全**：完整 Type Hints 注解（`Dict`, `Optional`）
- 🧩 **模块化设计**：每个解析步骤均为独立函数，可单独调用
- 📝 **原始保留**：输出包含 `original_text` 字段，便于结果追溯与校对

---

## 🚀 快速开始

### 单行解析

```python
from receiver_parser import parse_receiver_info

text = "张三，13812345678，广东省深圳市南山区粤海街道科技园科苑路15号"
result = parse_receiver_info(text)

print(result)