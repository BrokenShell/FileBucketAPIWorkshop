from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from app.bucket import FileBucket

API = FastAPI(
    title="File Bucket API",
    version="0.0.1",
    docs_url="/",
)
API.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)
file_bucket = FileBucket()


@API.put("/upload", tags=["File Bucket Router"])
async def upload(file: UploadFile = File(...)):
    """<h3>Docs HERE</h3>
    <pre><code>@param file: bytes
    @return: JSON success
    </code></pre>"""
    try:
        file_content = await file.read()
        file_bucket.upload(file_content, file.filename)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}


@API.get("/download/{filename}", tags=["File Bucket Router"])
async def download(filename: str):
    file_content = file_bucket.download(filename)
    return StreamingResponse(
        file_content,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@API.delete("/delete/{filename}", tags=["File Bucket Router"])
async def delete(filename: str):
    file_bucket.delete(filename)
    return {"success": True}
