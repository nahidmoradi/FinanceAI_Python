"""Vector store interface for semantic search operations."""

from abc import ABC, abstractmethod
from typing import Any


class VectorStoreInterface(ABC):
    """Interface for vector database implementations (FAISS, Weaviate, Chroma)."""

    @abstractmethod
    async def upsert_vectors(
        self,
        vectors: list[dict[str, Any]],
        namespace: str | None = None,
    ) -> dict[str, int]:
        """Insert or update vectors in the store.

        Args:
            vectors: List of vector objects with id, values, and metadata.
            namespace: Optional namespace for vector isolation.

        Returns:
            Result with count of upserted vectors.

        Raises:
            VectorStoreError: If upsert operation fails.
        """

    @abstractmethod
    async def query_vectors(
        self,
        query_vector: list[float],
        top_k: int = 10,
        filter_metadata: dict[str, Any] | None = None,
        namespace: str | None = None,
    ) -> list[dict[str, Any]]:
        """Query similar vectors using semantic search.

        Args:
            query_vector: Query vector for similarity search.
            top_k: Number of top results to return.
            filter_metadata: Optional metadata filters.
            namespace: Optional namespace to search within.

        Returns:
            List of matching vectors with scores and metadata.

        Raises:
            VectorStoreError: If query operation fails.
        """

    @abstractmethod
    async def delete_vectors(
        self,
        vector_ids: list[str],
        namespace: str | None = None,
    ) -> dict[str, int]:
        """Delete vectors by IDs.

        Args:
            vector_ids: List of vector IDs to delete.
            namespace: Optional namespace.

        Returns:
            Result with count of deleted vectors.

        Raises:
            VectorStoreError: If delete operation fails.
        """
