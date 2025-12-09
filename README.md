# Excalidraw Diagrams - Claude Code Skill

A [Claude Code](https://claude.ai/claude-code) skill for generating [Excalidraw](https://excalidraw.com) diagrams programmatically. Create flowcharts, architecture diagrams, and system designs without ASCII art.

## Installation

### Quick Install (Recommended)

```bash
git clone https://github.com/robtaylor/excalidraw-diagrams ~/.claude/skills/excalidraw-diagrams
```

### Manual Install

1. Create the skills directory if it doesn't exist:
   ```bash
   mkdir -p ~/.claude/skills
   ```

2. Clone this repository:
   ```bash
   cd ~/.claude/skills
   git clone https://github.com/robtaylor/excalidraw-diagrams
   ```

3. Restart Claude Code to pick up the new skill.

## Usage

Once installed, Claude Code will automatically use this skill when you ask for diagrams. For example:

> "Create a flowchart showing user authentication flow"

> "Draw an architecture diagram for a microservices system"

> "Make a diagram showing the data flow between frontend, API, and database"

Claude will generate `.excalidraw` files that you can:
- Open at [excalidraw.com](https://excalidraw.com) (drag & drop)
- Edit in VS Code with the [Excalidraw extension](https://marketplace.visualstudio.com/items?itemName=pomdtr.excalidraw-editor)
- Export to PNG/SVG

## Example Output

The skill generates professional diagrams like:

```
┌──────────┐    REST API    ┌──────────┐      SQL      ┌──────────┐
│ Frontend │ ──────────────▶│ Backend  │ ─────────────▶│ Database │
└──────────┘                └──────────┘               └──────────┘
```

But as actual Excalidraw diagrams with:
- Hand-drawn aesthetic
- Color-coded components
- Editable after generation
- Professional appearance

## API

The skill provides three diagram builders:

### Diagram (General Purpose)

```python
from excalidraw_generator import Diagram

d = Diagram()
box1 = d.box(100, 100, "Step 1", color="blue")
box2 = d.box(300, 100, "Step 2", color="green")
d.arrow_between(box1, box2, "next")
d.save("diagram.excalidraw")
```

### Flowchart (Auto-positioning)

```python
from excalidraw_generator import Flowchart

fc = Flowchart(direction="vertical")
fc.start("Begin")
fc.process("p1", "Process")
fc.decision("d1", "OK?")
fc.end("Done")
fc.connect("__start__", "p1")
fc.connect("p1", "d1")
fc.save("flowchart.excalidraw")
```

### ArchitectureDiagram (System Design)

```python
from excalidraw_generator import ArchitectureDiagram

arch = ArchitectureDiagram()
arch.user("user", "User", x=100, y=100)
arch.service("api", "API", x=300, y=100)
arch.database("db", "PostgreSQL", x=500, y=100)
arch.connect("user", "api", "HTTPS")
arch.connect("api", "db", "SQL")
arch.save("architecture.excalidraw")
```

## Colors

Available colors: `blue`, `green`, `red`, `yellow`, `orange`, `violet`, `cyan`, `teal`, `gray`, `black`

## Requirements

- Python 3.8+
- No external dependencies (uses only standard library)

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! Please open an issue or PR.

## Credits

- [Excalidraw](https://excalidraw.com) - The fantastic open-source whiteboard tool
- [Claude Code](https://claude.ai/claude-code) - Anthropic's CLI for Claude
