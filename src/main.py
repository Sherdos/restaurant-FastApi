from fastapi import FastAPI

from src.menu.router import router as router_menu

app = FastAPI(
    title='Menu API'
)


app.include_router(router_menu)




