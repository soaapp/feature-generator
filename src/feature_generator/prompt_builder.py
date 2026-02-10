"""
Requirements and prompt builder.

Converts vision analysis results into structured requirements,
implementation prompts, and technical specifications using local LLMs.
"""

import yaml
from pathlib import Path
from typing import Any

from rich.console import Console

from feature_generator.ollama_client import OllamaClient

console = Console()


class RequirementsBuilder:
    """Builds structured requirements from vision analysis using local LLMs."""

    # System prompt for the requirements generation LLM
    SYSTEM_PROMPT = """You are an expert software requirements analyst and technical writer.
Your task is to convert UI mockup analysis into clear, actionable requirements and implementation guidance.
Be specific, structured, and focus on both functional and technical aspects."""

    def __init__(self, ollama_client: OllamaClient | None = None) -> None:
        """
        Initialize the requirements builder.

        Args:
            ollama_client: Optional OllamaClient instance. Creates new one if not provided.
        """
        self.ollama = ollama_client or OllamaClient()
        self.templates_dir = Path(__file__).parent / "templates"

    async def build_requirements(
        self,
        analysis: dict[str, Any],
        template: str = "web_app",
        model: str = "llama3:latest",
        output_format: str = "markdown",
    ) -> str:
        """
        Build structured requirements from vision analysis.

        Args:
            analysis: Vision analysis results from ImageAnalyzer
            template: Template name to use (e.g., "web_app", "mobile_app")
            model: LLM model to use
            output_format: Output format ("markdown", "json", "yaml")

        Returns:
            Structured requirements as text
        """
        console.print(f"[cyan]Generating requirements with {model}...[/cyan]")

        # Load template
        template_config = self._load_template(template)

        # Build the prompt for the LLM
        prompt = self._build_prompt(analysis, template_config, output_format)

        # Generate requirements using local LLM
        requirements = await self.ollama.generate_text(
            prompt=prompt,
            model=model,
            system=self.SYSTEM_PROMPT,
        )

        console.print("[green]Requirements generated[/green]")

        return requirements

    async def build_multi_screen_requirements(
        self,
        analyses: list[dict[str, Any]],
        template: str = "web_app",
        model: str = "llama3:latest",
    ) -> str:
        """
        Build requirements for multiple related screens/mockups.

        Args:
            analyses: List of vision analysis results
            template: Template name to use
            model: LLM model to use

        Returns:
            Comprehensive requirements covering all screens
        """
        console.print(
            f"[cyan]Generating multi-screen requirements for {len(analyses)} screens...[/cyan]"
        )

        # Load template
        template_config = self._load_template(template)

        # Build comprehensive prompt
        prompt = self._build_multi_screen_prompt(analyses, template_config)

        # Generate requirements
        requirements = await self.ollama.generate_text(
            prompt=prompt,
            model=model,
            system=self.SYSTEM_PROMPT,
        )

        console.print("[green]Multi-screen requirements generated[/green]")

        return requirements

    async def refine_requirements(
        self,
        requirements: str,
        user_feedback: str,
        model: str = "llama3:latest",
    ) -> str:
        """
        Refine requirements based on user feedback.

        Args:
            requirements: Original requirements
            user_feedback: User's refinement instructions
            model: LLM model to use

        Returns:
            Refined requirements
        """
        console.print("[cyan]Refining requirements based on feedback...[/cyan]")

        prompt = f"""Here are the current requirements:

{requirements}

The user has provided this feedback:
{user_feedback}

Please update the requirements to incorporate this feedback. Maintain the same structure and format."""

        refined = await self.ollama.generate_text(
            prompt=prompt,
            model=model,
            system=self.SYSTEM_PROMPT,
        )

        console.print("[green]Requirements refined[/green]")

        return refined

    def _load_template(self, template_name: str) -> dict[str, Any]:
        """
        Load a template configuration.

        Args:
            template_name: Name of the template (without .yaml extension)

        Returns:
            Template configuration dictionary
        """
        template_path = self.templates_dir / f"{template_name}.yaml"

        if not template_path.exists():
            console.print(
                f"[yellow]Template {template_name} not found, using default structure[/yellow]"
            )
            return self._get_default_template()

        with open(template_path, "r") as f:
            return yaml.safe_load(f)

    def _get_default_template(self) -> dict[str, Any]:
        """Get default template structure if no template file exists."""
        return {
            "name": "Default Template",
            "description": "Basic requirements structure",
            "sections": [
                "UI Components Overview",
                "Functional Requirements",
                "Technical Recommendations",
                "Implementation Guide",
            ],
        }

    def _build_prompt(
        self,
        analysis: dict[str, Any],
        template_config: dict[str, Any],
        output_format: str,
    ) -> str:
        """
        Build the prompt for the LLM to generate requirements.

        Args:
            analysis: Vision analysis results
            template_config: Template configuration
            output_format: Desired output format

        Returns:
            Formatted prompt
        """
        image_name = analysis.get("image_name", "mockup")
        raw_analysis = analysis.get("raw_analysis", "")
        components = analysis.get("parsed_components", {})

        prompt = f"""Convert this UI mockup analysis into structured {output_format} requirements.

**Image Analyzed**: {image_name}

**Vision Analysis**:
{raw_analysis}

**Extracted Components**:
"""

        # Add parsed components
        for category, items in components.items():
            if items:
                prompt += f"\n{category.replace('_', ' ').title()}:\n"
                for item in items:
                    prompt += f"- {item}\n"

        # Add template-specific instructions
        template_name = template_config.get("name", "Default")
        sections = template_config.get("sections", [])
        tech_stack = template_config.get("tech_stack_defaults", [])

        prompt += f"\n\n**Output Structure** (use {template_name} format):\n"
        prompt += "Please organize the requirements into these sections:\n"
        for section in sections:
            prompt += f"- {section}\n"

        if tech_stack:
            prompt += f"\n**Recommended Tech Stack**:\n"
            for tech in tech_stack:
                prompt += f"- {tech}\n"

        prompt += f"""

Generate clear, actionable requirements that a developer can use to implement this UI.
Include specific details about:
1. What components need to be built
2. How they should behave
3. What data they need
4. Any important UX considerations

Format the output as well-structured {output_format}."""

        return prompt

    def _build_multi_screen_prompt(
        self,
        analyses: list[dict[str, Any]],
        template_config: dict[str, Any],
    ) -> str:
        """Build prompt for multiple screens."""
        prompt = f"""Convert these {len(analyses)} UI mockup analyses into comprehensive requirements for a multi-screen application.

**Screens Analyzed**:
"""

        for idx, analysis in enumerate(analyses, 1):
            image_name = analysis.get("image_name", f"Screen {idx}")
            raw_analysis = analysis.get("raw_analysis", "")
            prompt += f"\n### Screen {idx}: {image_name}\n"
            prompt += f"{raw_analysis}\n"

        prompt += """

Please generate comprehensive requirements that:
1. Cover all screens and their relationships
2. Identify shared components and patterns
3. Define navigation and user flows
4. Specify data requirements across screens
5. Suggest overall architecture and tech stack

Format as well-structured markdown with clear sections."""

        return prompt

    def save_output(
        self,
        content: str,
        output_path: Path | str,
        format: str = "md",
    ) -> None:
        """
        Save requirements to a file.

        Args:
            content: Requirements content
            output_path: Path to save file
            format: File format extension
        """
        output_path = Path(output_path)

        # Ensure correct extension
        if not output_path.suffix:
            output_path = output_path.with_suffix(f".{format}")

        output_path.write_text(content)
        console.print(f"[green]Requirements saved to: {output_path}[/green]")
