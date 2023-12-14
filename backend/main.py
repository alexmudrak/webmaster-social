from api.v1_dashboard import router as dashboards_router
from api.v1_projects import router as projects_router
from api.v1_settings import router as settings_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(settings_router)
app.include_router(projects_router)
app.include_router(dashboards_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
