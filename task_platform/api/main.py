from fastapi import FastAPI

from task_platform.api.routes.tasks import router as tasks_router

app = FastAPI()
app.include_router(tasks_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("task_platform.api.main:app", host="0.0.0.0", port=8000, reload=True)