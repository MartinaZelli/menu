from fastapi import FastAPI
from src import router
import uvicorn


app = FastAPI()
app.include_router(router.router)


def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()

