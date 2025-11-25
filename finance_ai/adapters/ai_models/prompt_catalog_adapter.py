"""Prompt catalog adapter for loading and managing AI prompts."""

from pathlib import Path
from typing import Any

import yaml

from finance_ai.use_cases.interfaces.prompt_catalog_interface import PromptCatalogInterface


class PromptCatalogAdapter(PromptCatalogInterface):
    """File-based prompt catalog implementation."""

    def __init__(self, prompts_directory: Path) -> None:
        """Initialize prompt catalog adapter.

        Args:
            prompts_directory: Directory containing prompt YAML files.
        """
        self.prompts_directory = prompts_directory
        self._cache: dict[str, dict[str, Any]] = {}

    async def get_prompt(self, prompt_name: str, version: str | None = None) -> dict[str, Any]:
        """Load prompt configuration from YAML file.

        Args:
            prompt_name: Prompt identifier.
            version: Optional version (ignored for file-based).

        Returns:
            Prompt configuration dictionary.

        Raises:
            PromptNotFoundError: If prompt file doesn't exist.
        """
        cache_key = f"{prompt_name}_{version or 'latest'}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        prompt_file = self.prompts_directory / f"{prompt_name}.yaml"

        if not prompt_file.exists():
            msg = f"Prompt not found: {prompt_name}"
            raise FileNotFoundError(msg)

        with prompt_file.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        self._cache[cache_key] = config
        return config

    async def list_prompts(self) -> list[dict[str, Any]]:
        """List all available prompts in directory.

        Returns:
            List of prompt metadata.
        """
        prompts = []

        for yaml_file in self.prompts_directory.glob("*.yaml"):
            try:
                with yaml_file.open("r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)

                prompts.append({
                    "id": config.get("id", yaml_file.stem),
                    "version": config.get("version", "unknown"),
                    "description": config.get("description", ""),
                })
            except Exception:
                continue

        return prompts
