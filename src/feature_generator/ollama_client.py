"""
Ollama client wrapper for local AI model interactions.

Handles communication with Ollama for both vision and LLM models,
including health checks, model management, and inference.
"""

import asyncio
import base64
from pathlib import Path
from typing import Any

import httpx
import ollama
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class OllamaClient:
    """Client for interacting with Ollama local AI models."""

    def __init__(self, host: str = "http://localhost:11434") -> None:
        """
        Initialize Ollama client.

        Args:
            host: Ollama server host URL
        """
        self.host = host
        self.client = ollama.Client(host=host)

    async def check_health(self) -> bool:
        """
        Check if Ollama server is running and accessible.

        Returns:
            True if Ollama is healthy, False otherwise
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.host}/api/tags", timeout=5.0)
                return response.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException):
            return False

    async def list_models(self) -> list[dict[str, Any]]:
        """
        List all available models in Ollama.

        Returns:
            List of model information dictionaries
        """
        try:
            models = self.client.list()
            return models.get("models", [])
        except Exception as e:
            console.print(f"[red]Error listing models: {e}[/red]")
            return []

    async def pull_model(self, model: str, show_progress: bool = True) -> bool:
        """
        Pull a model from Ollama registry.

        Args:
            model: Model name (e.g., "llava:latest", "llama3:latest")
            show_progress: Whether to show download progress

        Returns:
            True if successful, False otherwise
        """
        try:
            if show_progress:
                console.print(f"[yellow]Pulling model {model}...[/yellow]")

            # Pull model using the ollama library
            # The pull method returns a generator of progress updates
            for progress in self.client.pull(model, stream=True):
                if show_progress and "status" in progress:
                    console.print(f"  {progress['status']}", end="\r")

            if show_progress:
                console.print(f"[green]✓ Model {model} ready[/green]")
            return True

        except Exception as e:
            console.print(f"[red]Error pulling model {model}: {e}[/red]")
            return False

    async def model_exists(self, model: str) -> bool:
        """
        Check if a model exists locally.

        Args:
            model: Model name to check

        Returns:
            True if model exists, False otherwise
        """
        models = await self.list_models()
        model_names = [m["name"] for m in models]

        # Handle both "model:tag" and "model" formats
        if ":" not in model:
            model = f"{model}:latest"

        return model in model_names

    async def ensure_model(self, model: str) -> bool:
        """
        Ensure a model is available, pulling it if necessary.

        Args:
            model: Model name

        Returns:
            True if model is available, False otherwise
        """
        if await self.model_exists(model):
            return True

        console.print(f"[yellow]Model {model} not found locally. Pulling...[/yellow]")
        return await self.pull_model(model)

    async def analyze_image(
        self,
        image_path: Path,
        model: str = "llava:latest",
        prompt: str = "Analyze this UI mockup in detail.",
    ) -> str:
        """
        Analyze an image using a vision model.

        Args:
            image_path: Path to the image file
            model: Vision model to use
            prompt: Analysis prompt

        Returns:
            Analysis result as text
        """
        # Ensure the model is available
        if not await self.ensure_model(model):
            raise RuntimeError(f"Failed to ensure model {model} is available")

        # Read and encode image
        with open(image_path, "rb") as f:
            image_data = f.read()

        # Generate response using vision model
        try:
            response = self.client.generate(
                model=model,
                prompt=prompt,
                images=[image_data],
            )
            return response.get("response", "")
        except Exception as e:
            raise RuntimeError(f"Error analyzing image with {model}: {e}")

    async def generate_text(
        self,
        prompt: str,
        model: str = "llama3:latest",
        system: str = "",
    ) -> str:
        """
        Generate text using an LLM.

        Args:
            prompt: Text generation prompt
            model: LLM model to use
            system: System prompt (optional)

        Returns:
            Generated text
        """
        # Ensure the model is available
        if not await self.ensure_model(model):
            raise RuntimeError(f"Failed to ensure model {model} is available")

        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat(
                model=model,
                messages=messages,
            )
            return response["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"Error generating text with {model}: {e}")

    async def get_recommended_models(self) -> dict[str, str]:
        """
        Get recommended model names for vision and LLM tasks.

        Returns:
            Dictionary with 'vision' and 'llm' model names
        """
        return {
            "vision": "llava:latest",
            "llm": "llama3:latest",
        }
