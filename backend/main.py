from api.v1_dashboard import router as dashboards_router
from api.v1_projects import router as projects_router
from api.v1_settings import router as settings_router
from api.v1_tasks import router as tasks_router
from fastapi import FastAPI
from models.project import Project
from models.setting import Setting

Setting.model_rebuild()
Project.model_rebuild()

app = FastAPI()

v1_endpoints = [
    dashboards_router,
    projects_router,
    settings_router,
    tasks_router,
]

for endpoint in v1_endpoints:
    app.include_router(endpoint, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
