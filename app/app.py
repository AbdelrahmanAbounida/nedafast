from fastapi.middleware.cors import CORSMiddleware
from app.api.router import router as main_router
from app.lifespan import lifespan
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates



load_dotenv()



app = FastAPI(
    lifespan=lifespan,
    dependencies=[],  # TODO: Add dependencies for API authentication if required
    description="""
        Scalable and robust backend server with FastAPI, integrating MongoDB using Beanie ODM. 
        Includes JWT-based authentication, TypeScript code generation, and modular architecture 
        using Dependency Injection for clean and maintainable design 🚀.
    """,
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# *******************
# Routes
# *******************
templates = Jinja2Templates(directory="app/static/templates")

@app.get("/",tags=["Home"], response_class=HTMLResponse)
async def root(request:Request):
    return templates.TemplateResponse(request=request, name="home.html", context={})

app.include_router(main_router)