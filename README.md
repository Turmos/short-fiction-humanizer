# Short Fiction Humanizer

Humanize AI-sounding Chinese short fiction without losing plot, voice, pacing, logic, character motives, or emotional impact.

`short-fiction-humanizer` is an editorial skill for Chinese short fiction of roughly 8k–30k characters. It combines story-level de-AI review with sentence-level editing for awkward dialogue and narration. It is designed for drafts, outlines, rewrites, and line edits in genres such as suspense, romance, social realism, rebirth, fantasy, system fiction, and game fiction.

## What It Checks

- Opening hook, information release, conflict results, character agency, reversal or emotional closure, and ending image
- Unsupported or awkward causality, setting contradictions, sequence errors, and broken conditionals
- Verb-object and measure-word mismatches, missing objects, translation-like phrasing, and invented jargon
- Dialogue attribution, speaker voice, overly formal dialogue, interrupted dialogue beats, and missing referents
- Mechanical characterization, scene-detached actions, unnatural comparisons, and stiff punctuation rhythm
- AI-style summary lines, over-explained system mechanics, repeated high-frequency phrasing, and artificial symmetry

The skill preserves protected content: plot facts, setting rules, named terms, character relationships, intentional voice, genre-specific language, and meaningful roughness. It does not promise to evade AI detectors.

## Installation

Clone the repository into your local skills directory:

```bash
git clone https://github.com/Turmos/short-fiction-humanizer.git
```

For Codex or another skill-aware agent, load `SKILL.md` and the relevant files in `references/`. The full short-fiction workflow is in [references/short-fiction.md](references/short-fiction.md).

## Usage

Ask for a complete revision:

```text
Use $short-fiction-humanizer to revise this Chinese short-fiction chapter.
Preserve the plot, setting, character motives, and chapter structure.
Remove AI-like phrasing and awkward dialogue, but do not flatten the voice.
```

Ask for line editing:

```text
Use $short-fiction-humanizer to identify every awkward sentence in this passage.
For each issue, output: Original / Problem / Revision.
Then provide the complete revised text with the original paragraph structure.
```

Ask for diagnosis only:

```text
Use $short-fiction-humanizer in annotation mode. Identify awkward sentences only; do not rewrite the text.
```

## Layout

- `SKILL.md`: entrypoint and workflow
- `references/short-fiction.md`: Chinese short-fiction editing rules and line-edit output contract
- `scripts/audit_short_fiction.py`: lexical review hints; it is not a structural validator
- `agents/openai.yaml`: Codex UI metadata
- `.claude-plugin/`: Claude Code plugin metadata

## License

[MIT](LICENSE)

The repository deliberately contains no third-party prose corpus or benchmark
archive. The skill does not need a supplied novel corpus to run; users provide
the text they are authorized to edit.
