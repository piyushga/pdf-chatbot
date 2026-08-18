from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"


class EmbeddingService:
    def __init__(self, api_key: str) -> None:
        self.client = OpenAI(api_key=api_key)

    def create_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        response = self.client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=texts,
        )
        ordered_embeddings = sorted(response.data, key=lambda item: item.index)
        return [item.embedding for item in ordered_embeddings]
