"""
Feature Generator - Convert UI mockups to structured requirements using local AI models.

A 100% free and open-source tool that uses Ollama to analyze UI mockups and wireframes
locally, generating structured requirements and code prompts without any API costs.
"""

__version__ = "0.1.0"
__author__ = "Jay"
__license__ = "MIT"

from feature_generator.analyzer import ImageAnalyzer
from feature_generator.prompt_builder import RequirementsBuilder

__all__ = ["ImageAnalyzer", "RequirementsBuilder", "__version__"]
