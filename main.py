from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuring CORS policy
origins = ["https://objdetectionserver-production.up.railway.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/data")
async def get_data():
    # Simulating an async task, like a search on the database
    # await asyncio.sleep(1)
    return {"message": "Let's FUCKING GO!!!"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0')
