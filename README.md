# Custom Skills for AI Agents

A collection of reusable skills that extend AI agent capabilities with specialized workflows, scripts, and techniques.

## What Are Skills?

Skills are modular, self-contained packages that teach AI agents how to perform specific tasks. Each skill includes:

- **SKILL.md** - Instructions and workflow documentation the AI follows
- **scripts/** - Supporting code and utilities
- **Resources** - Any additional files needed

## Available Skills

| Skill | Description |
|-------|-------------|
| [transparent-background](./transparent-background/) | Extract true alpha transparency from images using the two-pass technique |

## How to Use

### With GitHub Copilot Agent Mode

1. Clone or copy the skill folder into your project's `.agent/skills/` directory
2. The AI agent will automatically discover and use the skill when relevant
3. Reference the skill explicitly by mentioning its name in your prompt

### Skill Structure

```
skill-name/
├── SKILL.md          # Main skill documentation (required)
└── scripts/          # Supporting scripts (optional)
    └── tool.py
```

## Creating New Skills

To add a new skill:

1. Create a new folder with a descriptive name
2. Add a `SKILL.md` file with frontmatter:
   ```yaml
   ---
   name: skill-name
   description: Brief description of when and how to use this skill
   ---
   ```
3. Document the complete workflow in the SKILL.md
4. Add any supporting scripts in a `scripts/` subfolder
5. Update this README to include the new skill

## Contributing

Feel free to submit pull requests with new skills or improvements to existing ones!

## License

MIT
