import os
import shelve
from typing import Optional, Any


class CacheService:
    def store(self, key: Any, value: Any, namespace: Optional[str] = None) -> None:
        raise NotImplementedError()

    def retrieve(self, key: Any, namespace: Optional[str] = None) -> Optional[Any]:
        raise NotImplementedError()


class ShelveCacheService(CacheService):
    def __init__(self, cache_dir: str, action_id: str):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

        self.default_namespace = action_id

    def _prepare_key(self, key: Any) -> str:
        return str(key)

    def _load_shelf(self, namespace: str):
        return shelve.open(
            os.path.join(self.cache_dir, f"{namespace}.db"),
            writeback=True,
        )

    def store(self, key: Any, value: Any, namespace: Optional[str] = None) -> None:
        if namespace is None:
            namespace = self.default_namespace

        shelf = self._load_shelf(namespace)
        key = self._prepare_key(key)
        shelf[key] = value
        shelf.close()

    def retrieve(self, key: Any, namespace: Optional[str] = None) -> Optional[Any]:
        if namespace is None:
            namespace = self.default_namespace

        shelf = self._load_shelf(namespace)
        key = self._prepare_key(key)
        value = shelf.get(key)
        shelf.close()

        return value
