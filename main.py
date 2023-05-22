from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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


@app.get("/api/post-photo")
async def post_photo(request: Request):
    response = JSONResponse(content={"message": "Let's FUCKING GO!!!"})
    response.headers["Access-Control-Allow-Origin"] = request.headers.get("origin", "*")
    return response

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0')
