# Feature Generator

> Transform UI mockups and wireframes into structured requirements using **100% free, local AI models**. No API keys, no costs, complete privacy.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Overview

**Feature Generator** is a CLI tool that converts photos or videos of UI mockups, wireframes, and sketches into detailed, actionable software requirements using local AI models via [Ollama](https://ollama.com).

**Why Feature Generator?**
- **100% Free** - No API costs, ever
- **Privacy-First** - All processing happens locally on your machine
- **Offline-Capable** - Works without internet after initial setup
- **Open Source** - MIT licensed, community-driven
- **No Vendor Lock-in** - Use any Ollama-compatible model

Perfect for solo developers who want to move quickly from mockup to code without depending on paid APIs.

## Features

- **Image Analysis**: Analyze UI mockups (PNG, JPG, WEBP) using local vision models (LLaVA, CogVLM)
- **Video Support**: Extract and analyze key frames from video demos
- **Structured Requirements**: Generate detailed requirements in Markdown, JSON, or YAML
- **Multiple Templates**: Built-in templates for web apps, mobile apps, and dashboards
- **Custom Templates**: Create your own requirement templates
- **Multi-Screen Analysis**: Analyze multiple related screens to understand flows
- **Model Flexibility**: Choose from various local vision and LLM models

## Installation

### Prerequisites

**1. Install Ollama**

```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Or download from https://ollama.com
```

**2. Install Feature Generator**

```bash
git clone https://github.com/jjahanzad/feature-generator.git
cd feature-generator
pip install -e .
```

**3. Initialize and Pull Models**

```bash
# This will check Ollama and offer to pull recommended models
feature-gen init
```

The recommended models are:
- **llava:latest** (~4.7 GB) - Vision model for image analysis
- **llama3:latest** (~4.7 GB) - LLM for requirements generation

## Quick Start

### 1. Analyze a Single Mockup

```bash
feature-gen analyze mockup.png
```

This will:
1. Analyze the image using local vision model
2. Generate structured requirements using local LLM
3. Save output to `mockup-requirements.md`

### 2. Analyze Multiple Screens

```bash
feature-gen analyze screen1.png screen2.png screen3.png
```

Generates comprehensive requirements covering all screens and their relationships.

### 3. Use Different Templates

```bash
# For mobile apps
feature-gen analyze app-mockup.png --template mobile_app

# For dashboards
feature-gen analyze dashboard.png --template dashboard

# List all templates
feature-gen templates
```

### 4. Customize Models

```bash
# Use larger vision model for better accuracy
feature-gen analyze mockup.png --vision-model llava:13b --llm-model llama3:70b
```

### 5. Specify Output

```bash
# Save to specific file
feature-gen analyze mockup.png --output my-requirements.md

# Different format
feature-gen analyze mockup.png --format json
```

## Usage Examples

### Example 1: Web Application Wireframe

```bash
feature-gen analyze homepage-wireframe.png --template web_app
```

**Output**: `homepage-wireframe-requirements.md`
```markdown
# Homepage - Requirements

## Overview
Landing page for a SaaS application with hero section, features grid, and call-to-action.

## UI Components Breakdown
- Navigation bar with logo and menu items
- Hero section with heading, subheading, and CTA button
- Three-column features grid
- Footer with links and social media icons

## Functional Requirements
1. Navigation should be sticky on scroll
2. CTA button should trigger signup modal
3. Features should be responsive (stacked on mobile)
...
```

### Example 2: Mobile App Screens

```bash
feature-gen analyze onboarding1.png onboarding2.png onboarding3.png --template mobile_app
```

Generates a comprehensive document covering:
- Screen flow and navigation
- Swipe gestures for onboarding
- Platform-specific considerations
- Data requirements

### Example 3: Video Demo

```bash
feature-gen analyze app-demo.mp4 --frame-interval 30
```

Extracts frames every 30 frames and analyzes the UI flow.

## Configuration

Feature Generator uses a configuration file at `~/.config/feature-generator/config.yaml`.

Create one with:

```bash
feature-gen init
```

**Example Configuration:**

```yaml
# Model Configuration
models:
  vision: "llava:latest"
  llm: "llama3:latest"
  auto_pull: true

# Output Settings
output:
  default_template: "web_app"
  default_format: "markdown"
  auto_open: false

# Cache Settings
cache:
  enabled: true
  ttl_hours: 24
```

## Templates

Feature Generator includes built-in templates optimized for different UI types:

### Web App Template
- Component hierarchy and reusability
- Responsive design considerations
- State management recommendations
- API integration points
- SEO and accessibility

### Mobile App Template
- Touch-friendly UI patterns
- Platform-specific guidelines (iOS/Android)
- Gesture interactions
- Offline-first considerations
- Device-specific features

### Create Custom Templates

Create a YAML file in `~/.config/feature-generator/templates/`:

```yaml
name: "Dashboard Template"
description: "Template for admin dashboards"

sections:
  - "Dashboard Overview"
  - "Data Visualizations"
  - "Filters & Controls"
  - "API Requirements"

tech_stack_defaults:
  - "React with TypeScript"
  - "Recharts for data visualization"
  - "TanStack Table for data tables"
```

## Available Commands

```bash
# Initialize and check setup
feature-gen init

# Analyze images
feature-gen analyze IMAGE [IMAGE...] [OPTIONS]

# List available models
feature-gen models

# List available templates
feature-gen templates

# Show version
feature-gen --version

# Show help
feature-gen --help
```

## CLI Options

### `analyze` command

```bash
feature-gen analyze [OPTIONS] IMAGES...

Options:
  -o, --output PATH         Output file path
  -t, --template TEXT       Template name (default: web_app)
  --vision-model TEXT       Vision model (default: llava:latest)
  --llm-model TEXT          LLM model (default: llama3:latest)
  -f, --format TEXT         Output format: markdown, json, yaml
  --help                    Show help
```

## Model Recommendations

### Vision Models (for image analysis)

| Model | Size | Quality | Speed | Use Case |
|-------|------|---------|-------|----------|
| `llava:latest` (7B) | 4.7 GB | Good | Fast | Default, best for most use cases |
| `llava:13b` | 7.4 GB | Better | Medium | Higher quality analysis |
| `llava:34b` | 19 GB | Best | Slow | Maximum accuracy |
| `cogvlm:latest` | ~10 GB | Excellent | Medium | Alternative vision model |

### LLM Models (for requirements generation)

| Model | Size | Quality | Speed | Use Case |
|-------|------|---------|-------|----------|
| `llama3:latest` (8B) | 4.7 GB | Good | Fast | Default, balanced performance |
| `llama3:70b` | 39 GB | Excellent | Slow | Best quality requirements |
| `mistral:latest` | 4.1 GB | Good | Fast | Lightweight alternative |
| `qwen:latest` | 4.4 GB | Good | Fast | Another quality option |

Pull models with: `ollama pull MODEL_NAME`

## How It Works

1. **Image Input**: You provide photos/screenshots of UI mockups
2. **Vision Analysis**: Local vision model (LLaVA) analyzes the image to identify:
   - UI components (buttons, forms, navigation, etc.)
   - Layout and hierarchy
   - Text content
   - User interactions
   - Visual styling
3. **Requirements Generation**: Local LLM (Llama 3) converts the analysis into:
   - Structured requirements
   - Implementation guidance
   - Technical recommendations
   - User stories
4. **Output**: Formatted requirements in Markdown/JSON/YAML

All processing happens locally - no data leaves your machine!

## Use Cases

- **Solo Developers**: Quickly turn sketches into actionable requirements
- **Rapid Prototyping**: Convert whiteboard drawings to structured specs
- **Documentation**: Generate documentation from existing UI screenshots
- **Design Handoff**: Convert Figma screenshots into developer-friendly requirements
- **Learning**: Understand UI patterns by analyzing existing applications

## Comparison with Cloud APIs

| Feature | Feature Generator | Cloud APIs (e.g., Claude, GPT-4 Vision) |
|---------|-------------------|------------------------------------------|
| Cost | **Free** | $0.01-0.10 per image |
| Privacy | **Local only** | Data sent to servers |
| Internet | After setup, **works offline** | Requires internet |
| Limits | **No limits** | Rate limits, quotas |
| Setup | Install Ollama + models | API key required |
| Quality | Good (improving) | Excellent |

## Contributing

Contributions are welcome! This project is designed to be community-driven.

**Ways to contribute:**
- Report bugs and request features via [Issues](https://github.com/jjahanzad/feature-generator/issues)
- Submit PRs for improvements
- Create and share custom templates
- Improve model prompts for better analysis
- Add new output formats

## Roadmap

- [ ] Code generation mode (generate actual code from requirements)
- [ ] Interactive refinement mode
- [ ] Support for more vision models
- [ ] Fine-tuned models for UI analysis
- [ ] Web UI (Gradio/Streamlit)
- [ ] VS Code extension
- [ ] Browser extension for screenshot analysis
- [ ] Figma plugin
- [ ] Template marketplace

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by [Docling](https://github.com/DS4SD/docling) and its local-first philosophy
- Built with [Ollama](https://ollama.com) for local AI model management
- Uses [Typer](https://typer.tiangolo.com/) for the CLI framework
- Uses [Rich](https://rich.readthedocs.io/) for beautiful terminal output

## Support

- **Issues**: [GitHub Issues](https://github.com/jjahanzad/feature-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jjahanzad/feature-generator/discussions)

---

**Made with ❤️ by the open-source community**

If you find this tool useful, consider ⭐ starring the repo!
