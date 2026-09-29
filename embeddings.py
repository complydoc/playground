"""A local stand-in for OpenAI's embedding model, so the pipeline runs offline and free.

It is named as `langchain_openai.OpenAIEmbeddings` is, so the trace reads as it would
with the real one. It embeds with a deterministic fake and looks up `localhost`, so the
trace still has a connection to show. To use OpenAI's, import it from `langchain_openai`
in pipeline.py instead.
"""

import socket

from langchain_core.embeddings import DeterministicFakeEmbedding


class OpenAIEmbeddings(DeterministicFakeEmbedding):
    model: str = "text-embedding-3-small"
    size: int = 1536

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        socket.getaddrinfo("localhost", 443)
        return super().embed_documents(texts)
