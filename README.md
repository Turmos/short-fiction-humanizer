# 中文短篇小说去 AI 改造

在不损伤剧情、人物动机、节奏、逻辑和情绪力度的前提下，清理中文短篇小说里的 AI 腔与别扭表达。

`short-fiction-humanizer` 是面向约 8 千至 3 万字中文短篇的编辑 skill。它同时处理故事层面的 AI 痕迹，以及对白和叙述层面的逐句润色，适用于悬疑、言情、世情、重生、玄幻、系统、游戏等题材的初稿、大纲、改稿和精修。

## 检查内容

- 开头钩子、信息释放、冲突结果、主角主动性、反转或情绪闭环、结尾画面
- 因果关系生硬、设定矛盾、时序错乱、条件句缺失
- 动宾和量词搭配错误、宾语缺失、悬空动词、翻译腔、生造术语
- 对话归属不明、人物语气失真、书面化对白、动作打断对白、指代不明
- 人物行为机械化、动作脱离场景、比较不自然、标点节奏僵硬
- AI 式总结、系统机制解释过多、高频词复读、刻意对称结构

skill 会优先保护剧情事实、设定规则、专有名词、人物关系、有意保留的声线、题材语言和自然的粗粝感。它不会承诺绕过 AI 检测器。

## 安装

把仓库克隆到本地 skills 目录：

```bash
git clone https://github.com/Turmos/short-fiction-humanizer.git
```

在 Codex 或其他支持 skill 的 agent 中，读取 `SKILL.md` 和所需的 `references/` 文件即可使用。短篇小说的完整工作流见 [references/short-fiction.md](references/short-fiction.md)。

## 用法

完整改稿：

```text
使用 $short-fiction-humanizer 修改这章中文短篇小说。
保留剧情、设定、人物动机和章节结构。
清理 AI 味和别扭对白，但不要把人物声线磨平。
```

逐句精修：

```text
使用 $short-fiction-humanizer 找出这段文字里所有别扭的句子。
每一处按“原句 / 问题 / 修改”输出，最后给出保持原段落结构的完整修改稿。
```

只做诊断：

```text
使用 $short-fiction-humanizer 的 annotation mode，只标出问题，不改写正文。
```

## 目录说明

- `SKILL.md`：skill 入口和工作流
- `references/short-fiction.md`：中文短篇去 AI 规则和逐句审校交付格式
- `scripts/audit_short_fiction.py`：词汇级复查提示，不能替代结构判断
- `agents/openai.yaml`：Codex UI 元数据
- `.claude-plugin/`：Claude Code 插件元数据

## 许可证

[MIT](LICENSE)

本仓库不包含第三方小说正文、语料库或评测档案。skill 无需自带小说语料才能运行，使用者应只提交自己有权编辑的文本。
