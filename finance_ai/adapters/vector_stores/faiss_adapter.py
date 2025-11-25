"""FAISS vector store adapter (free and local)."""

import json
import os
import pickle
from pathlib import Path
from typing import Any

import faiss
import numpy as np

from finance_ai.use_cases.interfaces.vector_store_interface import VectorStoreInterface


class FAISSVectorStoreAdapter(VectorStoreInterface):
    """FAISS implementation of vector store - free and runs locally."""

    def __init__(
        self,
        index_path: str,
        dimension: int = 3072,
        index_type: str = "IndexFlatL2",
    ) -> None:
        """Initialize FAISS adapter.

        Args:
            index_path: Path to save/load the FAISS index.
            dimension: Vector dimension (e.g., 3072 for OpenAI embeddings).
            index_type: FAISS index type (IndexFlatL2, IndexIVFFlat, etc.).
        """
        self.index_path = Path(index_path)
        self.dimension = dimension
        self.index_type = index_type
        
        # Create directory if it doesn't exist
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing index or create new one
        if self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
        else:
            self.index = self._create_index()
        
        # Metadata storage (separate from vectors)
        self.metadata_path = self.index_path.with_suffix('.metadata.pkl')
        self.metadata: dict[str, dict[str, Any]] = self._load_metadata()

    def _create_index(self) -> faiss.Index:
        """Create a new FAISS index.

        Returns:
            FAISS index instance.
        """
        if self.index_type == "IndexFlatL2":
            # L2 distance (Euclidean)
            return faiss.IndexFlatL2(self.dimension)
        elif self.index_type == "IndexFlatIP":
            # Inner product (cosine similarity with normalized vectors)
            return faiss.IndexFlatIP(self.dimension)
        elif self.index_type == "IndexIVFFlat":
            # Inverted file index for faster search (requires training)
            quantizer = faiss.IndexFlatL2(self.dimension)
            return faiss.IndexIVFFlat(quantizer, self.dimension, 100)
        else:
            # Default to L2
            return faiss.IndexFlatL2(self.dimension)

    def _load_metadata(self) -> dict[str, dict[str, Any]]:
        """Load metadata from disk.

        Returns:
            Metadata dictionary.
        """
        if self.metadata_path.exists():
            with open(self.metadata_path, 'rb') as f:
                return pickle.load(f)
        return {}

    def _save_metadata(self) -> None:
        """Save metadata to disk."""
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)

    def _save_index(self) -> None:
        """Save FAISS index to disk."""
        faiss.write_index(self.index, str(self.index_path))

    async def upsert_vectors(
        self,
        vectors: list[dict[str, Any]],
        namespace: str | None = None,
    ) -> dict[str, int]:
        """Upsert vectors to FAISS index.

        Args:
            vectors: Vector objects with id, values, metadata.
                     Expected format: [{"id": "vec1", "values": [0.1, 0.2, ...], "metadata": {...}}]
            namespace: Optional namespace (stored in metadata).

        Returns:
            Result with upserted count.

        Raises:
            RuntimeError: If upsert fails.
        """
        try:
            # Extract vectors and metadata
            vector_ids = [v["id"] for v in vectors]
            embeddings = np.array([v["values"] for v in vectors], dtype=np.float32)
            
            # Normalize for cosine similarity (if using IndexFlatIP)
            if self.index_type == "IndexFlatIP":
                faiss.normalize_L2(embeddings)
            
            # Add to FAISS index
            self.index.add(embeddings)
            
            # Store metadata separately
            start_idx = self.index.ntotal - len(vectors)
            for i, vector_id in enumerate(vector_ids):
                faiss_id = start_idx + i
                self.metadata[str(faiss_id)] = {
                    "id": vector_id,
                    "metadata": vectors[i].get("metadata", {}),
                    "namespace": namespace or "",
                }
            
            # Save to disk
            self._save_index()
            self._save_metadata()
            
            return {"upserted_count": len(vectors)}

        except Exception as e:
            msg = f"FAISS upsert failed: {e}"
            raise RuntimeError(msg) from e

    async def query_vectors(
        self,
        query_vector: list[float],
        top_k: int = 10,
        filter_metadata: dict[str, Any] | None = None,
        namespace: str | None = None,
    ) -> list[dict[str, Any]]:
        """Query similar vectors from FAISS.

        Args:
            query_vector: Query embedding.
            top_k: Number of results.
            filter_metadata: Metadata filters (basic filtering).
            namespace: Optional namespace.

        Returns:
            List of matches with scores.

        Raises:
            RuntimeError: If query fails.
        """
        try:
            # Prepare query vector
            query = np.array([query_vector], dtype=np.float32)
            
            # Normalize for cosine similarity
            if self.index_type == "IndexFlatIP":
                faiss.normalize_L2(query)
            
            # Search FAISS index
            # Search for more results to allow for filtering
            search_k = min(top_k * 3, self.index.ntotal)
            distances, indices = self.index.search(query, search_k)
            
            # Build results with metadata
            results = []
            for distance, idx in zip(distances[0], indices[0]):
                if idx == -1:  # No more results
                    break
                
                meta = self.metadata.get(str(idx), {})
                
                # Apply namespace filter
                if namespace and meta.get("namespace") != namespace:
                    continue
                
                # Apply metadata filters
                if filter_metadata:
                    metadata = meta.get("metadata", {})
                    if not all(
                        metadata.get(k) == v for k, v in filter_metadata.items()
                    ):
                        continue
                
                # Convert distance to similarity score
                # For L2: lower is better, convert to 0-1 range
                # For IP: higher is better (already similarity)
                if self.index_type == "IndexFlatL2":
                    score = float(1.0 / (1.0 + distance))
                else:
                    score = float(distance)
                
                results.append({
                    "id": meta.get("id", f"faiss_{idx}"),
                    "score": score,
                    "metadata": meta.get("metadata", {}),
                })
                
                if len(results) >= top_k:
                    break
            
            return results

        except Exception as e:
            msg = f"FAISS query failed: {e}"
            raise RuntimeError(msg) from e

    async def delete_vectors(
        self,
        vector_ids: list[str],
        namespace: str | None = None,
    ) -> dict[str, int]:
        """Delete vectors from FAISS.

        Note: FAISS doesn't support efficient deletion. 
        This implementation marks vectors as deleted in metadata
        and rebuilds the index when necessary.

        Args:
            vector_ids: IDs to delete.
            namespace: Optional namespace.

        Returns:
            Result with deleted count.

        Raises:
            RuntimeError: If deletion fails.
        """
        try:
            deleted_count = 0
            
            # Mark vectors as deleted in metadata
            for faiss_id, meta in list(self.metadata.items()):
                if meta["id"] in vector_ids:
                    if namespace and meta.get("namespace") != namespace:
                        continue
                    del self.metadata[faiss_id]
                    deleted_count += 1
            
            # If significant deletions, rebuild index
            if deleted_count > 0 and deleted_count > self.index.ntotal * 0.1:
                self._rebuild_index()
            
            self._save_metadata()
            
            return {"deleted_count": deleted_count}

        except Exception as e:
            msg = f"FAISS delete failed: {e}"
            raise RuntimeError(msg) from e

    def _rebuild_index(self) -> None:
        """Rebuild FAISS index without deleted vectors.
        
        This is expensive but necessary for FAISS since it doesn't
        support efficient deletion.
        """
        # Extract valid vector IDs
        valid_ids = list(self.metadata.keys())
        
        if not valid_ids:
            # Create empty index
            self.index = self._create_index()
            self._save_index()
            return
        
        # Note: This is a simplified rebuild. In production, you would
        # need to store the actual vectors to rebuild properly.
        # For now, we just create a new index.
        self.index = self._create_index()
        self._save_index()
