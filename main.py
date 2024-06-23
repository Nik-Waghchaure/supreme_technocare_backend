import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Application.view import router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add media folder
# app.mount("/media", StaticFiles(directory="media"), name="media")


@app.get("/")
async def root():
    return {"message": "Hello World"}


# add api which read image from media folder
@app.get("/media/{file_path:path}")
async def read_file(file_path: str):
    return FileResponse(file_path)


app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8888, reload=True)