"""
Command-line interface for feature-generator.

Provides commands for analyzing UI mockups and generating requirements
using local AI models via Ollama.
"""

import asyncio
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from feature_generator import __version__
from feature_generator.analyzer import ImageAnalyzer
from feature_generator.ollama_client import OllamaClient
from feature_generator.prompt_builder import RequirementsBuilder

app = typer.Typer(
    name="feature-gen",
    help="Convert UI mockups into structured requirements using local AI models",
    add_completion=False,
)
console = Console()


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console.print(f"feature-generator version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """Feature Generator - Convert UI mockups to requirements using local AI."""
    pass


@app.command()
def init() -> None:
    """
    Initialize feature-generator and check Ollama setup.

    This command:
    - Checks if Ollama is installed and running
    - Lists available models
    - Offers to pull recommended models
    """
    console.print(
        Panel.fit(
            "[bold cyan]Feature Generator Initialization[/bold cyan]\n"
            "Checking Ollama setup and models...",
            border_style="cyan",
        )
    )

    async def _init() -> None:
        ollama = OllamaClient()

        # Check Ollama health
        console.print("\n[cyan]Checking Ollama installation...[/cyan]")
        is_healthy = await ollama.check_health()

        if not is_healthy:
            console.print(
                "[red]✗ Ollama is not running or not installed[/red]\n"
                "\nPlease install Ollama first:\n"
                "  macOS/Linux: curl -fsSL https://ollama.com/install.sh | sh\n"
                "  Or visit: https://ollama.com\n"
            )
            raise typer.Exit(1)

        console.print("[green]✓ Ollama is running[/green]")

        # List available models
        console.print("\n[cyan]Checking available models...[/cyan]")
        models = await ollama.list_models()

        if models:
            table = Table(title="Available Models")
            table.add_column("Model", style="cyan")
            table.add_column("Size", style="magenta")

            for model in models:
                name = model.get("name", "unknown")
                size = model.get("size", 0)
                size_gb = size / (1024**3) if size else 0
                table.add_row(name, f"{size_gb:.1f} GB")

            console.print(table)
        else:
            console.print("[yellow]No models found locally[/yellow]")

        # Check for recommended models
        recommended = await ollama.get_recommended_models()
        vision_model = recommended["vision"]
        llm_model = recommended["llm"]

        console.print(f"\n[cyan]Checking recommended models...[/cyan]")
        console.print(f"  Vision model: {vision_model}")
        console.print(f"  LLM model: {llm_model}")

        has_vision = await ollama.model_exists(vision_model)
        has_llm = await ollama.model_exists(llm_model)

        if has_vision and has_llm:
            console.print("\n[green]✓ All recommended models are available![/green]")
        else:
            console.print("\n[yellow]Some recommended models are missing.[/yellow]")
            should_pull = typer.confirm("Would you like to pull the recommended models?")

            if should_pull:
                if not has_vision:
                    await ollama.pull_model(vision_model)
                if not has_llm:
                    await ollama.pull_model(llm_model)

                console.print("\n[green]✓ Setup complete![/green]")
            else:
                console.print(
                    "\n[yellow]You can pull models later with:[/yellow]\n"
                    f"  ollama pull {vision_model}\n"
                    f"  ollama pull {llm_model}"
                )

        console.print(
            "\n[green]✓ Initialization complete![/green]\n"
            "\nNext steps:\n"
            "  1. Analyze a mockup: feature-gen analyze mockup.png\n"
            "  2. View help: feature-gen --help"
        )

    asyncio.run(_init())


@app.command()
def analyze(
    images: list[Path] = typer.Argument(..., help="Path(s) to image or video file(s) to analyze"),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path for requirements (default: auto-generated)",
    ),
    template: str = typer.Option(
        "web_app",
        "--template",
        "-t",
        help="Template to use (web_app, mobile_app, dashboard)",
    ),
    vision_model: str = typer.Option(
        "llama3.2-vision:latest",
        "--vision-model",
        help="Vision model to use for image analysis",
    ),
    llm_model: str = typer.Option(
        "llama3:latest",
        "--llm-model",
        help="LLM model to use for requirements generation",
    ),
    format: str = typer.Option(
        "markdown",
        "--format",
        "-f",
        help="Output format (markdown, json, yaml)",
    ),
    frame_interval: int = typer.Option(
        30,
        "--frame-interval",
        help="For videos: extract one frame every N frames (default: 30)",
    ),
) -> None:
    """
    Analyze UI mockup image(s) or video(s) and generate requirements.

    Examples:
      feature-gen analyze mockup.png
      feature-gen analyze screen1.png screen2.png --template mobile_app
      feature-gen analyze wireframe.jpg -o requirements.md
      feature-gen analyze demo.mp4 --frame-interval 30
    """
    # Determine file type for display
    video_extensions = [".mp4", ".mov", ".avi", ".mkv", ".webm"]
    file_type = "video" if len(images) == 1 and images[0].suffix.lower() in video_extensions else "image(s)"

    console.print(
        Panel.fit(
            f"[bold cyan]Analyzing {len(images)} {file_type}[/bold cyan]",
            border_style="cyan",
        )
    )

    async def _analyze() -> None:
        ollama = OllamaClient()
        analyzer = ImageAnalyzer(ollama)
        builder = RequirementsBuilder(ollama)

        # Check if input is a video
        video_extensions = [".mp4", ".mov", ".avi", ".mkv", ".webm"]
        is_video = len(images) == 1 and images[0].suffix.lower() in video_extensions

        # Analyze images or video
        if is_video:
            # Handle video file
            video_analysis = await analyzer.analyze_video(
                images[0],
                frame_interval=frame_interval,
                model=vision_model
            )
            # Convert video analysis to format expected by builder
            # Use the frame analyses from the video
            frame_analyses = video_analysis.get("frame_analyses", [])
            if len(frame_analyses) == 1:
                analysis = frame_analyses[0]
                requirements = await builder.build_requirements(
                    analysis=analysis,
                    template=template,
                    model=llm_model,
                    output_format=format,
                )
            else:
                requirements = await builder.build_multi_screen_requirements(
                    analyses=frame_analyses,
                    template=template,
                    model=llm_model,
                )
        elif len(images) == 1:
            # Single image
            analysis = await analyzer.analyze_image(images[0], model=vision_model)
            requirements = await builder.build_requirements(
                analysis=analysis,
                template=template,
                model=llm_model,
                output_format=format,
            )
        else:
            # Multiple images
            analyses = await analyzer.analyze_batch(images, model=vision_model)
            requirements = await builder.build_multi_screen_requirements(
                analyses=analyses,
                template=template,
                model=llm_model,
            )

        # Determine output path
        if output is None:
            base_name = images[0].stem
            output_path = Path(f"{base_name}-requirements.md")
        else:
            output_path = output

        # Save requirements
        builder.save_output(requirements, output_path, format)

        # Display summary
        console.print(
            Panel.fit(
                f"[green]✓ Analysis complete![/green]\n\n"
                f"Requirements saved to: [cyan]{output_path}[/cyan]\n\n"
                f"Next steps:\n"
                f"  • Review: cat {output_path}\n"
                f"  • Generate code: feature-gen build {images[0]} (coming soon)\n"
                f"  • Use with any LLM or Claude Code",
                border_style="green",
                title="Success",
            )
        )

    asyncio.run(_analyze())


@app.command(name="models")
def list_models() -> None:
    """List available Ollama models."""
    console.print("[cyan]Fetching available models...[/cyan]")

    async def _list_models() -> None:
        ollama = OllamaClient()
        models = await ollama.list_models()

        if not models:
            console.print("[yellow]No models found. Pull models with:[/yellow]")
            console.print("  ollama pull llama3.2-vision:latest")
            console.print("  ollama pull llama3:latest")
            return

        table = Table(title="Available Ollama Models")
        table.add_column("Model", style="cyan", no_wrap=True)
        table.add_column("Size", style="magenta")
        table.add_column("Modified", style="blue")

        for model in models:
            name = model.get("name", "unknown")
            size = model.get("size", 0)
            size_gb = size / (1024**3) if size else 0
            modified = model.get("modified_at", "")[:10] if "modified_at" in model else ""
            table.add_row(name, f"{size_gb:.1f} GB", modified)

        console.print(table)

    asyncio.run(_list_models())


@app.command()
def templates() -> None:
    """List available requirement templates."""
    templates_dir = Path(__file__).parent / "templates"

    console.print("[cyan]Available Templates:[/cyan]\n")

    import yaml

    for template_file in templates_dir.glob("*.yaml"):
        with open(template_file, "r") as f:
            template_config = yaml.safe_load(f)

        name = template_config.get("name", template_file.stem)
        description = template_config.get("description", "No description")

        console.print(f"  [bold]{template_file.stem}[/bold]: {description}")

    console.print(
        "\nUse with: [cyan]feature-gen analyze mockup.png --template TEMPLATE_NAME[/cyan]"
    )


if __name__ == "__main__":
    app()
