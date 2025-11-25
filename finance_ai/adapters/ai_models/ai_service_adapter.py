"""AI service adapter implementation using LangGraph and LangChain."""

import json
from typing import Any

from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from finance_ai.use_cases.interfaces.ai_service_interface import AIServiceInterface


class AIServiceAdapter(AIServiceInterface):
    """AI service implementation using LangChain/LangGraph."""

    def __init__(
        self,
        openai_api_key: str | None = None,
        gemini_api_key: str | None = None,
        default_model: str = "gemini-2.0-flash-exp",
    ) -> None:
        """Initialize AI service adapter.

        Args:
            openai_api_key: OpenAI API key.
            gemini_api_key: Google Gemini API key.
            default_model: Default model to use.
        """
        self.openai_api_key = openai_api_key
        self.gemini_api_key = gemini_api_key
        self.default_model = default_model
        self._llm_cache: dict[str, Any] = {}

    def _get_llm(self, model_name: str, temperature: float = 0.3) -> Any:
        """Get or create LLM instance with caching.

        Args:
            model_name: Name of the model.
            temperature: Temperature parameter.

        Returns:
            LLM instance.
        """
        cache_key = f"{model_name}_{temperature}"
        if cache_key in self._llm_cache:
            return self._llm_cache[cache_key]

        if "gpt" in model_name.lower():
            llm = ChatOpenAI(
                model=model_name,
                temperature=temperature,
                api_key=self.openai_api_key,
            )
        elif "gemini" in model_name.lower():
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                google_api_key=self.gemini_api_key,
            )
        else:
            llm = ChatGoogleGenerativeAI(
                model=self.default_model,
                temperature=temperature,
                google_api_key=self.gemini_api_key,
            )

        self._llm_cache[cache_key] = llm
        return llm

    async def process_prompt(
        self,
        prompt_template: str,
        input_variables: dict[str, Any],
        model_config: dict[str, Any],
    ) -> dict[str, Any]:
        """Process prompt using LangChain.

        Args:
            prompt_template: Jinja2 prompt template.
            input_variables: Variables for template.
            model_config: Model configuration.

        Returns:
            Structured AI response.

        Raises:
            AIServiceError: If processing fails.
        """
        try:
            model_name = model_config.get("model_hint", self.default_model)
            temperature = model_config.get("temperature", 0.3)

            llm = self._get_llm(model_name, temperature)
            prompt = ChatPromptTemplate.from_template(prompt_template)
            chain = prompt | llm

            result = await chain.ainvoke(input_variables)
            content = result.content if hasattr(result, "content") else str(result)

            return self._parse_json_response(content)

        except Exception as e:
            msg = f"AI service processing failed: {e}"
            raise RuntimeError(msg) from e

    async def generate_embeddings(self, text: str) -> list[float]:
        """Generate embeddings using OpenAI.

        Args:
            text: Input text.

        Returns:
            Embedding vector.

        Raises:
            AIServiceError: If embedding generation fails.
        """
        try:
            embeddings = OpenAIEmbeddings(api_key=self.openai_api_key)
            result = await embeddings.aembed_query(text)
            return result

        except Exception as e:
            msg = f"Embedding generation failed: {e}"
            raise RuntimeError(msg) from e

    async def run_agentic_workflow(
        self,
        workflow_name: str,
        input_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute agentic workflow using LangGraph.

        Args:
            workflow_name: Workflow identifier.
            input_data: Workflow input.

        Returns:
            Workflow result.

        Raises:
            AIServiceError: If workflow fails.
        """
        msg = "Agentic workflows not yet implemented"
        raise NotImplementedError(msg)

    def _parse_json_response(self, content: str) -> dict[str, Any]:
        """Parse JSON from LLM response.

        Args:
            content: Response content.

        Returns:
            Parsed JSON dictionary.
        """
        try:
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1

            if start_idx == -1 or end_idx == 0:
                return {"raw_content": content}

            json_str = content[start_idx:end_idx]
            return json.loads(json_str)

        except json.JSONDecodeError:
            return {"raw_content": content}
