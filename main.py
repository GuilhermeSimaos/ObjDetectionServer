import asyncio
from fastapi import FastAPI

app = FastAPI()


@app.get("/api/data")
async def get_data():
    # Simulating an async task, like a search on the database
    await asyncio.sleep(1)
    return {"message": "Hello World using FastAPI"}


if __name__ == '__main__':
    app.run(host='0.0.0.0')
