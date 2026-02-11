# Feature Generator

> Transform UI mockups into structured requirements using **100% free, local AI models**. No API keys, no costs, complete privacy.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Quick Setup

### 1. Install Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Or download from https://ollama.com
```

### 2. Install Feature Generator

```bash
git clone https://github.com/jjahanzad/feature-generator.git
cd feature-generator
pip install -e .
```

### 3. Initialize

```bash
feature-gen init
```

This pulls the recommended models (~9.4 GB total):
- **llava:latest** - Vision model for image analysis
- **llama3:latest** - LLM for requirements generation

### 4. Analyze Your First Mockup

```bash
feature-gen analyze mockup.png
```

Output saved to [mockup-requirements.md](mockup-requirements.md)

## Common Usage

```bash
# Multiple screens
feature-gen analyze screen1.png screen2.png screen3.png

# Mobile app template
feature-gen analyze app.png --template mobile_app

# Custom output
feature-gen analyze mockup.png --output requirements.md --format json

# List available templates
feature-gen templates
```

## Why Feature Generator?

- **100% Free** - No API costs, ever
- **Privacy-First** - All processing happens locally
- **Offline-Capable** - Works without internet after setup
- **Open Source** - MIT licensed, community-driven

## Advanced Usage

### CLI Options

```bash
feature-gen analyze [OPTIONS] IMAGES...

Options:
  -o, --output PATH         Output file path
  -t, --template TEXT       Template: web_app, mobile_app, dashboard
  --vision-model TEXT       Vision model (default: llava:latest)
  --llm-model TEXT          LLM model (default: llama3:latest)
  -f, --format TEXT         Output format: markdown, json, yaml
```

### Recommended Models

**Vision Models:**
- `llava:latest` (4.7 GB) - Default, best for most cases
- `llava:13b` (7.4 GB) - Higher quality
- `llava:34b` (19 GB) - Maximum accuracy

**LLM Models:**
- `llama3:latest` (4.7 GB) - Default, balanced
- `llama3:70b` (39 GB) - Best quality
- `mistral:latest` (4.1 GB) - Lightweight

Pull with: `ollama pull MODEL_NAME`

### Configuration

Config file: `~/.config/feature-generator/config.yaml`

```yaml
models:
  vision: "llava:latest"
  llm: "llama3:latest"

output:
  default_template: "web_app"
  default_format: "markdown"
```

### Custom Templates

Create YAML files in `~/.config/feature-generator/templates/`:

```yaml
name: "My Template"
sections:
  - "Overview"
  - "Components"
  - "Requirements"
```

## Features

- Analyze UI mockups (PNG, JPG, WEBP) and videos
- Multiple output formats (Markdown, JSON, YAML)
- Built-in templates for web apps, mobile apps, and dashboards
- Custom template support
- Multi-screen analysis for understanding user flows
- All processing happens locally - complete privacy

## Contributing

Contributions welcome! Report bugs or request features via [GitHub Issues](https://github.com/jjahanzad/feature-generator/issues).

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built with [Ollama](https://ollama.com) • Inspired by local-first philosophy**

Star the repo if you find it useful!
