"""Base AI agent use case for common functionality."""

from abc import ABC, abstractmethod
from typing import Any

from finance_ai.entities.ai_agent_models.prompt_names import PromptNames
from finance_ai.use_cases.interfaces.ai_service_interface import AIServiceInterface
from finance_ai.use_cases.interfaces.prompt_catalog_interface import PromptCatalogInterface


class BaseAIAgentUseCase(ABC):
    """Base class for AI agent use cases."""

    def __init__(
        self,
        prompt_catalog: PromptCatalogInterface,
        ai_service: AIServiceInterface,
    ) -> None:
        """Initialize base AI agent use case.

        Args:
            prompt_catalog: Prompt catalog for loading prompts.
            ai_service: AI service for processing.
        """
        self.prompt_catalog = prompt_catalog
        self.ai_service = ai_service
        self.prompt_name: PromptNames | None = None

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the use case logic.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Use case result.

        Raises:
            UseCaseError: If execution fails.
        """

    async def load_prompt_config(self, version: str | None = None) -> dict[str, Any]:
        """Load prompt configuration from catalog.

        Args:
            version: Optional specific prompt version.

        Returns:
            Prompt configuration.

        Raises:
            PromptNotFoundError: If prompt doesn't exist.
        """
        if not self.prompt_name:
            msg = "Prompt name not set in use case"
            raise ValueError(msg)

        return await self.prompt_catalog.get_prompt(self.prompt_name.value, version)

    def build_prompt_variables(self, **kwargs: Any) -> dict[str, Any]:
        """Build variables for prompt template substitution.

        Args:
            **kwargs: Variable key-value pairs.

        Returns:
            Variables dictionary.
        """
        return kwargs
