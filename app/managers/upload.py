from fastapi import UploadFile , File

from app.services.backblaze import get_b2_resource , upload_file
from app.shared import settings

b2_rw = get_b2_resource(settings.ENDPOINT_URL_BUCKET, settings.KEY_ID_YOUR_ACCOUNT, settings.APPLICATION_KEY_YOUR_ACCOUNT)

class UploadManager:

    @staticmethod
    def upload_to_service( file: UploadFile = File(...) ):
        b2 = b2_rw

        response = upload_file(settings.PUBLIC_BUCKET_NAME , settings.LOCAL_DIR , file.filename , b2)

        print('RESPONSE:  ' , response)

        return response

        # generate_friendly_url(NEW_BUCKET_NAME , endpoint , b2)