# Examples

This directory contains example mockups and their generated requirements to demonstrate Feature Generator's capabilities.

## How to Use These Examples

1. Install Feature Generator and Ollama (see main README)
2. Run the examples:

```bash
# Analyze an example mockup
feature-gen analyze examples/mockup.png

# Or try with different templates
feature-gen analyze examples/mobile-mockup.png --template mobile_app
```

## Adding Your Examples

Contributions of example mockups are welcome! Please submit:
1. The mockup image (PNG/JPG)
2. The generated requirements output
3. A brief description of what it demonstrates

This helps others understand what Feature Generator can do.

## Example Categories

- **Web Applications**: Landing pages, dashboards, admin panels
- **Mobile Apps**: App screens, onboarding flows, navigation
- **Wireframes**: Low-fidelity sketches and wireframes
- **Hand-drawn**: Whiteboard sketches and paper prototypes

## Tips for Good Results

1. **Clear images**: Higher resolution yields better analysis
2. **Good lighting**: For photos of sketches/whiteboard drawings
3. **Multiple angles**: Avoid too much perspective distortion
4. **Annotations**: Text labels help the vision model understand intent
5. **Context**: For multi-screen flows, analyze screens together
