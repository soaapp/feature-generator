"""
Image analyzer for UI mockups and wireframes.

Uses local vision models via Ollama to extract UI components,
layout information, and functional requirements from images.
"""

import json
from pathlib import Path
from typing import Any

from rich.console import Console

from feature_generator.ollama_client import OllamaClient

console = Console()


class ImageAnalyzer:
    """Analyzes UI mockups and wireframes using local vision models."""

    # Vision prompt for analyzing UI mockups
    VISION_PROMPT = """Analyze this UI mockup or wireframe image in detail. Extract the following information:

1. **UI Components**: List all visible UI elements (buttons, forms, navigation bars, cards, etc.)
2. **Layout Structure**: Describe the overall layout and hierarchy (header, main content, footer, sidebars, etc.)
3. **Text Content**: Extract all visible text, labels, and headings
4. **User Interactions**: Identify interactive elements and potential user actions
5. **Visual Style**: Note any styling patterns (colors, spacing, typography hints)
6. **Data Elements**: Identify areas that would need dynamic data (lists, tables, user profiles, etc.)

Provide the analysis in a structured format with clear sections.
Be specific and detailed. If this is a hand-drawn sketch, interpret it as best as possible."""

    def __init__(self, ollama_client: OllamaClient | None = None) -> None:
        """
        Initialize the image analyzer.

        Args:
            ollama_client: Optional OllamaClient instance. Creates new one if not provided.
        """
        self.ollama = ollama_client or OllamaClient()

    async def analyze_image(
        self,
        image_path: Path | str,
        model: str = "llava:latest",
        custom_prompt: str = "",
    ) -> dict[str, Any]:
        """
        Analyze a single UI mockup image.

        Args:
            image_path: Path to the image file
            model: Vision model to use
            custom_prompt: Optional custom analysis prompt

        Returns:
            Dictionary containing analysis results
        """
        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        if not image_path.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp"]:
            raise ValueError(f"Unsupported image format: {image_path.suffix}")

        console.print(f"[cyan]🔍 Analyzing {image_path.name} with {model}...[/cyan]")

        # Use custom prompt if provided, otherwise use default
        prompt = custom_prompt or self.VISION_PROMPT

        # Analyze the image using Ollama vision model
        analysis_text = await self.ollama.analyze_image(
            image_path=image_path,
            model=model,
            prompt=prompt,
        )

        console.print("[green]✓ Vision analysis complete[/green]")

        # Structure the analysis result
        return {
            "image_path": str(image_path),
            "image_name": image_path.name,
            "model_used": model,
            "raw_analysis": analysis_text,
            "parsed_components": self._parse_components(analysis_text),
        }

    async def analyze_batch(
        self,
        image_paths: list[Path | str],
        model: str = "llava:latest",
    ) -> list[dict[str, Any]]:
        """
        Analyze multiple UI mockup images.

        Args:
            image_paths: List of paths to image files
            model: Vision model to use

        Returns:
            List of analysis results
        """
        results = []

        console.print(f"[cyan]Analyzing {len(image_paths)} images...[/cyan]")

        for idx, image_path in enumerate(image_paths, 1):
            console.print(f"\n[bold]Image {idx}/{len(image_paths)}[/bold]")
            try:
                result = await self.analyze_image(image_path, model)
                results.append(result)
            except Exception as e:
                console.print(f"[red]Error analyzing {image_path}: {e}[/red]")
                results.append({
                    "image_path": str(image_path),
                    "error": str(e),
                })

        return results

    def _parse_components(self, analysis_text: str) -> dict[str, list[str]]:
        """
        Parse the vision model output into structured components.

        This is a simple parser that looks for common sections.
        Can be enhanced with more sophisticated parsing.

        Args:
            analysis_text: Raw analysis text from vision model

        Returns:
            Dictionary of parsed component categories
        """
        components: dict[str, list[str]] = {
            "ui_elements": [],
            "layout": [],
            "text_content": [],
            "interactions": [],
            "styling_notes": [],
            "data_requirements": [],
        }

        lines = analysis_text.split("\n")
        current_section = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Detect section headers
            lower_line = line.lower()
            if "component" in lower_line or "element" in lower_line:
                current_section = "ui_elements"
            elif "layout" in lower_line or "structure" in lower_line:
                current_section = "layout"
            elif "text" in lower_line or "content" in lower_line:
                current_section = "text_content"
            elif "interaction" in lower_line or "action" in lower_line:
                current_section = "interactions"
            elif "style" in lower_line or "visual" in lower_line:
                current_section = "styling_notes"
            elif "data" in lower_line:
                current_section = "data_requirements"
            elif current_section and line.startswith(("-", "•", "*", "–")):
                # Add list items to current section
                item = line.lstrip("-•*– ").strip()
                if item:
                    components[current_section].append(item)

        return components

    async def analyze_video(
        self,
        video_path: Path | str,
        frame_interval: int = 30,
        model: str = "llava:latest",
    ) -> dict[str, Any]:
        """
        Analyze a video of UI mockup/demo by extracting key frames.

        Args:
            video_path: Path to the video file
            frame_interval: Extract one frame every N frames
            model: Vision model to use

        Returns:
            Dictionary containing analysis of extracted frames
        """
        import cv2

        video_path = Path(video_path)

        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        console.print(f"[cyan]📹 Extracting frames from {video_path.name}...[/cyan]")

        # Extract frames
        cap = cv2.VideoCapture(str(video_path))
        frames = []
        frame_count = 0
        saved_frame_count = 0

        # Create temporary directory for frames
        temp_dir = Path(f"/tmp/feature-gen-frames-{video_path.stem}")
        temp_dir.mkdir(exist_ok=True)

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_count % frame_interval == 0:
                    frame_path = temp_dir / f"frame_{saved_frame_count:04d}.png"
                    cv2.imwrite(str(frame_path), frame)
                    frames.append(frame_path)
                    saved_frame_count += 1

                frame_count += 1

            cap.release()

            console.print(f"[green]✓ Extracted {len(frames)} frames[/green]")

            # Analyze each frame
            frame_analyses = await self.analyze_batch(frames, model=model)

            return {
                "video_path": str(video_path),
                "video_name": video_path.name,
                "total_frames": frame_count,
                "analyzed_frames": len(frames),
                "frame_interval": frame_interval,
                "model_used": model,
                "frame_analyses": frame_analyses,
            }

        finally:
            # Clean up temporary frames
            for frame_path in frames:
                frame_path.unlink(missing_ok=True)
            temp_dir.rmdir()
