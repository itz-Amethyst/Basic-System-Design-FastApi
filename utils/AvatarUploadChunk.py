import mimetypes
from secrets import token_hex
from fastapi import UploadFile
import magic.magic

from app.shared import settings
from app.shared.errors import bad_file
def Upload_By_Chunk(file: UploadFile, flag = False):
    # 2048 idk
    # Maybe need a debug here
    mime = magic.magic.from_buffer(file.file.read(2048), mime = True)

    if mime is None:
        raise bad_file

    ext = mimetypes.guess_extension(mime)

    # f.e.g .rb .rs files like this will throw an error
    if ext is None or len(ext) < 2:
        raise bad_file

    # if file was greater than 40mb
    if file.size > 40 * 1024 * 1024:
        raise bad_file

    file.file.seek(0)

    filename = file.filename.split('.').pop(-2) # it will only get name of file
    file_name_pattern = token_hex(5)

    upload_dir = settings.Upload_Dir / "UserAvatars"
    upload_dir.mkdir(parents = True, exist_ok = True)

    path = upload_dir / (file_name_pattern + filename + ext)

    with open(path, 'wb') as f:
        while chunk := file.file.read():
            f.write(chunk)

    if flag is True:
        return {"success": True , "file_path": path , 'message': "File Uploaded successfully" , 'size': file.size}

    return mime, path , ext , filename