from task_platform.sources.api_source import ApiTaskSource
from task_platform.sources.file_source import JsonFileTaskSource
from task_platform.sources.generator_source import GeneratorTaskSource

FileTaskSource = JsonFileTaskSource

__all__ = ["ApiTaskSource", "FileTaskSource", "GeneratorTaskSource", "JsonFileTaskSource"]
