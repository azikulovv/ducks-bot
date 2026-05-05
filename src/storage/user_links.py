from __future__ import annotations

import asyncio
import json
from pathlib import Path


class UserLinkStorage:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._lock = asyncio.Lock()

    async def get(self, telegram_user_id: int) -> str | None:
        async with self._lock:
            data = self._read()
            return data.get(str(telegram_user_id))

    async def set(self, telegram_user_id: int, backend_user_id: str) -> None:
        async with self._lock:
            data = self._read()
            data[str(telegram_user_id)] = backend_user_id
            self._write(data)

    def _read(self) -> dict[str, str]:
        if not self._path.exists():
            return {}
        with self._path.open("r", encoding="utf-8") as file:
            raw = json.load(file)
        if not isinstance(raw, dict):
            return {}
        return {str(key): str(value) for key, value in raw.items()}

    def _write(self, data: dict[str, str]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self._path.with_suffix(f"{self._path.suffix}.tmp")
        with tmp_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2, sort_keys=True)
        tmp_path.replace(self._path)
