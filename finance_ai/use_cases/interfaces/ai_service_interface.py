"""AI Service interface for agentic AI operations."""

from abc import ABC, abstractmethod
from typing import Any


class AIServiceInterface(ABC):
    """Interface for AI service implementations (LangGraph, OpenAI, Gemini)."""

    @abstractmethod
    async def process_prompt(
        self,
        prompt_template: str,
        input_variables: dict[str, Any],
        model_config: dict[str, Any],
    ) -> dict[str, Any]:
        """Process a prompt with given variables and return AI response.

        Args:
            prompt_template: The prompt template string.
            input_variables: Variables to substitute in the template.
            model_config: Model configuration (temperature, model name, etc.).

        Returns:
            AI-generated response as dictionary.

        Raises:
            AIServiceError: If processing fails.
        """

    @abstractmethod
    async def generate_embeddings(self, text: str) -> list[float]:
        """Generate vector embeddings for given text.

        Args:
            text: Input text to embed.

        Returns:
            Vector embedding as list of floats.

        Raises:
            AIServiceError: If embedding generation fails.
        """

    @abstractmethod
    async def run_agentic_workflow(
        self,
        workflow_name: str,
        input_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute a multi-agent workflow using LangGraph.

        Args:
            workflow_name: Name of the workflow to execute.
            input_data: Input data for the workflow.

        Returns:
            Workflow execution result.

        Raises:
            AIServiceError: If workflow execution fails.
        """
