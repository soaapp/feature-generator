# Contributing to Feature Generator

Thank you for your interest in contributing to Feature Generator! This project is designed to be community-driven, and we welcome contributions of all kinds.

## Ways to Contribute

### 1. Report Bugs
- Use the [GitHub Issues](https://github.com/jjahanzad/feature-generator/issues) page
- Include steps to reproduce the bug
- Share the mockup image (if possible) or describe it
- Include your system info (OS, Python version, Ollama version)

### 2. Request Features
- Open an issue with the "enhancement" label
- Describe the feature and its use case
- Explain how it would benefit users

### 3. Submit Pull Requests

**Areas for contribution:**
- Improve vision analysis prompts for better component detection
- Add new requirement templates (dashboard, admin panel, etc.)
- Improve LLM prompts for better requirements generation
- Add support for new output formats
- Improve error handling and user experience
- Write tests
- Improve documentation

**Before submitting a PR:**
1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run tests (if applicable): `pytest`
5. Update documentation if needed
6. Commit with clear message
7. Push and open a PR

### 4. Create Templates
Share custom templates for different UI types:
- Create a `.yaml` file in `src/feature_generator/templates/`
- Follow the existing template structure
- Submit via PR with example output

### 5. Improve Model Prompts
The quality of analysis depends heavily on prompts:
- **Vision prompts**: `src/feature_generator/analyzer.py`
- **Requirements prompts**: `src/feature_generator/prompt_builder.py`

Test your improvements with various mockups and share results!

## Development Setup

```bash
# Clone the repo
git clone https://github.com/jjahanzad/feature-generator.git
cd feature-generator

# Install in development mode
pip install -e ".[dev]"

# Install Ollama and models
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llava:latest
ollama pull llama3:latest

# Run the CLI
feature-gen --help
```

## Code Style

- Python 3.10+ with type hints
- Black for formatting: `black .`
- Ruff for linting: `ruff check .`
- Write clear docstrings for public functions

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=feature_generator
```

## Project Structure

```
feature-generator/
├── src/feature_generator/
│   ├── cli.py              # CLI interface
│   ├── ollama_client.py    # Ollama integration
│   ├── analyzer.py         # Vision analysis
│   ├── prompt_builder.py   # Requirements generation
│   └── templates/          # Requirement templates
├── tests/                  # Test files
├── docs/                   # Documentation
└── examples/               # Example mockups and outputs
```

## Community Guidelines

- Be respectful and constructive
- Help others in discussions
- Share your use cases and examples
- Celebrate contributions from others

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Open a [Discussion](https://github.com/jjahanzad/feature-generator/discussions) or reach out via Issues.

Thank you for making Feature Generator better!
