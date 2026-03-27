from typing import Protocol, runtime_checkable
from pathlib import Path



@runtime_checkable
class FileParserProtocol(Protocol):
    """Контракт парсера файлов, получающих данные из различных файлов"""

    def parse(self, path: str | Path) -> list[dict]: ...