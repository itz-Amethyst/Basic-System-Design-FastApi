import mimetypes
import os
from secrets import token_hex

import magic.magic
from fastapi import UploadFile , File
from starlette.requests import Request

from app.services.backblaze import get_b2_resource , upload_file , list_objects_browsable_url
from app.shared import settings
from app.shared.errors import bad_file
from utils.file_operation import read_write_file

allowed_extensions = {'.jpeg', '.png', '.jpg'}
b2_rw = get_b2_resource(settings.ENDPOINT_URL_BUCKET, settings.KEY_ID_YOUR_ACCOUNT, settings.APPLICATION_KEY_YOUR_ACCOUNT)

class UploadManager:

    @staticmethod
    def upload_image(request: Request, flag: bool = False, file: UploadFile = File(...) ):

        mime = magic.magic.from_buffer(file.file.read(2048) , mime = True)

        if mime is None:
            raise bad_file

        ext = mimetypes.guess_extension(mime)

        # f.e.g .rb .rs files like this will throw an error
        if ext is None or len(ext) < 2:
            raise bad_file

        # ! Only allowed files
        if ext is None or ext.lower() not in allowed_extensions:
            raise bad_file

        # if file was greater than 40mb
        if file.size > 40 * 1024 * 1024:
            raise bad_file

        file.file.seek(0)

        filename = file.filename.split('.').pop(-2)  # it will only get name of file
        file_name_pattern = token_hex(5)

        #! Note is debug is true files will upload to upload folder if not will upload to s3 server
        if settings.DEBUG:
            upload_dir = settings.Upload_Dir / "UserAvatars"
            upload_dir.mkdir(parents = True , exist_ok = True)
            path = upload_dir / (file_name_pattern + filename + ext)

            read_write_file(path , file = file)

            simple_path = os.path.join(upload_dir.name , path.name)
            image_path = os.path.join(str(request.base_url) , simple_path).replace('\\' , '/')

        else:
            b2 = b2_rw
            path = os.path.join(settings.Upload_Dir_temp_for_service , file_name_pattern + file.filename)

            read_write_file(path , file = file)

            upload_file(settings.PUBLIC_BUCKET_NAME , path , file.filename , b2)

            image_path = f"https://{settings.PUBLIC_BUCKET_NAME}.{settings.ENDPOINT_URL_BUCKET.replace('https://','')}/{file.filename}"
            # image_path = f"https://{settings.PUBLIC_BUCKET_NAME}.{settings.ENDPOINT_URL_BUCKET.replace('https://','')}/{(file_name_pattern + file.filename)}"

            # Remove the file in temp for better performances
            os.remove(path)


        if flag is True:
            return {"success": True , **({'file_path': path} if settings.DEBUG else {}), "access_url": image_path, 'message': "File Uploaded successfully" , 'size': file.size}

        # return (mime , image_path , ext , filename) if settings.DEBUG is False else (mime , path , ext , filename)
        return mime, image_path, ext, filename


    @staticmethod
    def get_browsable_urls_in_sw3():

        return list_objects_browsable_url(bucket = settings.PUBLIC_BUCKET_NAME, endpoint = settings.ENDPOINT_URL_BUCKET, b2 = b2_rw)
