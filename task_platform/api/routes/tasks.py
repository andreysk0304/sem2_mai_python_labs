from fastapi import APIRouter

from task_platform.api.schemas import TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

DEMO_TASKS: list[TaskResponse] = [
    TaskResponse(id="api-1", payload={"source": "api", "action": "demo"}),
    TaskResponse(id="api-2", payload={"source": "api", "action": "sync"}),
    TaskResponse(id="api-3", payload={"source": "api", "action": "сказать, приветикиии!!!"})
]


@router.get("", response_model=list[TaskResponse])
async def get_tasks() -> list[TaskResponse]:
    return DEMO_TASKS
