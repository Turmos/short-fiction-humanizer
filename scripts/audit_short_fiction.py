#!/usr/bin/env python3
"""Flag likely short-fiction AI patterns for human review.

This is a lexical-only diagnostic pass, not a structural validator or
auto-rewriter. Matches are hints; context and full-manuscript review decide
whether a phrase is actually a problem.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


PATTERNS: list[tuple[str, str, str]] = [
    ("空泛升华", r"给这片[^。！？]{0,20}重新起名|文明重新点燃|命运的齿轮|这一刻[，,]?新的时代", "检查是否在替代场面；改回可见变化或下一步动作"),
    ("命名式总结", r"这(叫|就是)[^。！？]{0,20}(懂吗|的道理|的代价)|所谓的[^。！？]{0,16}(就是|才是)", "确认是不是给现象贴标签；若是，改成事实、动作或人物判断"),
    ("否定翻转骨架", r"不是[^。！？]{1,30}，?而是|与其[^。！？]{1,30}，?不如", "人工检查是否为口号式对比；正常选择句可保留"),
    ("条件-资源对照口号", r"(?:一旦|如果|要是|真要|一打穿|一冲破|一断)[^。！？]{0,40}(?:不缺|有的是|够多)[^。！？]{0,20}(?:先缺|先断|先没|先出问题|先撑不住)", "短篇正文强制禁用这类三拍骨架；拆成具体的供给变化、人物反应或实际选择"),
    ("职能宣言/伪格言对白", r"我(?:负责|就是来|的工作是)[^。！？]{0,30}(?:让|把|做)|[^。！？]{1,12}没有[^。！？]{1,16}只(是|能)|[^。！？]{1,10}比[^。！？]{1,10}(?:还|更)(?:难|麻烦|会说话|懂事)|[^。！？]{1,12}(?:不卖|不管|不负责)[^。！？]{1,20}(?:才|才能|才会)", "短篇正文强制过滤抽象职责、万能对比和物件伪格言；改成现场动作、具体故障、数字变化或人物冲突"),
    ("概念接力式对白", r"我信[^。！？]{1,10}[。！？]|[^。！？]{1,16}(?:也是|都是)人(?:写|定|做)的|把每一笔[^。！？]{0,16}(?:摊开|写清|摆出来)|只盯着[^。！？]{0,18}(?:还是|却也|也肯)[^。！？]{0,18}(?:翻账|看账|看)|别把[^。！？]{1,20}(?:做成|写成)[^。！？]{0,16}(?:假数|好看的)", "检查是否把对话写成围绕抽象概念互相接答案；改回眼前的账目、动作、异议和实际损失"),
    ("前言不搭后语/反向口号", r"这不是[^。！？]{1,24}[，,]这(是|就)[^。！？]{1,24}|别[^。！？]{1,18}[，,][^。！？]{0,18}(?:也没有|还是没有|照样没|也没)", "检查两个概念是否硬拼，或对白是否否定动作后只补无效结果；改成具体对象、阻力和人物目的"),
    ("情绪盖章/模板弹幕", r"(?:震惊|反转|打脸|太燃了|这波稳了|全场傻眼|弹幕炸了|直播间沸腾)", "确认是不是作者替现场盖章；改成停顿、猜测、嘴硬、动作失误或互相不一致的碎片反应"),
    ("硬造口吻/动作链断裂", r"螺丝(?:只)?咬|咬半圈|直播间先吵|晨雾(?:还没散|被冲破)|海面像墙|他刚张嘴", "不要为去 AI 硬造行业黑话或跳过动作顺序；改成普通词和连贯的声音→视线→动作链"),
    ("硬拗因果/拟人召唤", r"被[^。！？]{0,16}(电|城市|命运|时代|世界)叫来|节点.*长出来|由[^。！？]{0,20}(抽水泵|发电机|系统).*出来的", "补足来处、主体、动作和因果"),
    ("系统说明书", r"【系统[^】]{0,80}】|系统提示|(?:需求条|属性|任务|奖励|工具栏).{0,30}(?:解锁|激活|提升|完成)|解锁[^。！？]{0,30}(功能|等级|建筑)", "检查是否在复述界面；用户或作品明确建立的系统排队提示可保留，重点删除重复播报并补上新的动作、反馈或代价"),
    ("宣传/拔高腔", r"彻底征服|拉满|幸福感|凝聚力|新的篇章|伟大时代|史诗级|神迹诞生", "落到可观察的反应、代价或变化"),
    ("高频渲染词", r"仿佛|犹如|宛如|似乎|缓缓|渐渐|顿时|忽然|终于|心头一震|呼吸一滞|眼神复杂", "只在同段聚集时处理；保留最贴切的一处，其余改为动作或感官"),
    ("抽象比喻", r"像一[道种片]闪电|像是[^。！？]{0,20}(宣言|序幕|答案|开关)|仿佛[^。！？]{0,20}(世界|命运|时代)", "检查比喻是否能被现场细节验证"),
    ("角色工具化", r"好感度(爆表|拉满)|倒贴效忠|三美环伺|美女角色|身材火辣|深V|乳胶兔女郎", "确认外貌/标签是否替代人物目标、专业动作和选择"),
    ("技术名词拼贴", r"(过滤出来的热咖啡|电叫来|系统空气墙|排队交命)", "核对动作主体和设定物理关系"),
]

FRAGMENT_RE = re.compile(r"^[，。！？、；：,.!?;:]+$|^[一-龥A-Za-z]{1,2}$")
REPETITION_TERMS = ("盯着那行字", "愣住", "忽然", "然后", "这账", "那口气", "心没落地", "看着")


def snippet(lines: list[str], index: int, start: int, end: int) -> str:
    line = lines[index]
    left = max(0, start - 18)
    right = min(len(line), end + 30)
    value = line[left:right].strip()
    previous = lines[index - 1].strip() if index else ""
    following = lines[index + 1].strip() if index + 1 < len(lines) else ""
    context = " ".join(part for part in (previous[-40:], value, following[:40]) if part)
    return context if len(context) <= 130 else f"{context[:127]}..."


def audit(path: Path) -> int:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8")

    lines = text.splitlines()
    findings: list[tuple[int, str, str, str]] = []
    for number in range(1, len(lines)):
        if lines[number].strip() and lines[number].strip() == lines[number - 1].strip():
            findings.append((number + 1, "相邻重复句", lines[number].strip(), "同一事实不要保留旧句和新句两次；系统提示保留时，旁白改写成新的反馈或代价"))
    paragraphs = text.split("\n\n")
    for paragraph in paragraphs:
        first_line = text[: text.find(paragraph)].count("\n") + 1
        for term in REPETITION_TERMS:
            count = paragraph.count(term)
            if count >= 3:
                findings.append((first_line, "高频复读", f"本段“{term}”出现 {count} 次", "保留必要重复，其余检查是否只是凑节奏"))
        if len(re.findall(r"一半[^。！？]{0,24}一半|没有[^。！？]{0,24}没有|——|……", paragraph)) >= 2:
            findings.append((first_line, "对仗/破折号聚集", paragraph.strip()[:100], "确认是否连续制造对仗答案感；需要时改回普通连接或停顿"))
    for number, line in enumerate(lines, 1):
        for label, pattern, advice in PATTERNS:
            for match in re.finditer(pattern, line):
                findings.append((number, label, snippet(lines, number - 1, match.start(), match.end()), advice))
        stripped = line.strip()
        quoted = stripped.startswith(("“", "\"")) and stripped.endswith(("”", "\""))
        if stripped and FRAGMENT_RE.fullmatch(stripped) and not quoted and not stripped.startswith(("###", "【")):
            findings.append((number, "疑似断词/残句", stripped, "确认是否为有意节奏；否则补齐对白或动作"))

    print(f"文件: {path}")
    print(f"字符数: {len(text)}  行数: {len(lines)}  命中: {len(findings)}")
    print("范围: 仅词法线索；前三句、主线、反转比例、线索、钩子和结尾等全篇项目需人工检查。")
    if not findings:
        print("未发现规则命中；仍需人工通读结构、因果和人物动机。")
        return 0
    for number, label, value, advice in findings:
        print(f"{number}: [{label}] {value}")
        print(f"    建议: {advice}")
    print("以上仅为复查线索，不执行自动替换。")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Chinese short fiction for likely AI patterns")
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    return max(audit(path) for path in args.paths)


if __name__ == "__main__":
    raise SystemExit(main())
