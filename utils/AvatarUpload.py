from fastapi import UploadFile , File , HTTPException , status
from secrets import token_hex
from pathlib import Path


MB = 1024 * 1024
Upload_Dir = Path() / 'Uploads/Avatars'

def Upload_Avatar(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Please Provide an Avatar!")

    if file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Please Only select .jpg and .png files!")

    if not 0 < len(file.file.read()) <= 1 * MB:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "The Size must be between 0 - 1 Mb")

    file_ext = file.filename.split(".").pop()  # to get only name file f.e.g image22.png => image22
    file_name = token_hex(10)
    file_path = Upload_Dir / f"{file_name}.{file_ext}"

    with open(file_path, 'wb') as f:
        content = file.file.read()
        f.write(content)

    return {"success": True, "file_path": file_path, 'message': "File Uploaded successfully", 'size': file.size}

