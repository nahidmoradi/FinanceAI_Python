"""Prompt catalog interface for managing AI prompts."""

from abc import ABC, abstractmethod
from typing import Any


class PromptCatalogInterface(ABC):
    """Interface for prompt catalog implementations."""

    @abstractmethod
    async def get_prompt(self, prompt_name: str, version: str | None = None) -> dict[str, Any]:
        """Retrieve a prompt by name and optional version.

        Args:
            prompt_name: Name/ID of the prompt.
            version: Optional specific version (defaults to latest).

        Returns:
            Prompt configuration including template, metadata, and schema.

        Raises:
            PromptNotFoundError: If prompt does not exist.
        """

    @abstractmethod
    async def list_prompts(self) -> list[dict[str, Any]]:
        """List all available prompts.

        Returns:
            List of prompt metadata.
        """
