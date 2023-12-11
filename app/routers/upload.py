from fastapi import  APIRouter , UploadFile , File , status
from starlette.requests import Request

from app.managers.upload import UploadManager
from app.shared.errors import bad_file , database_error
from app.deps import rate_limit

router = APIRouter(
    prefix = '/upload',
    tags = ['Upload'],
    dependencies = [rate_limit('upload', 60, 30, use_id = False)]
)
@router.post('/', status_code = status.HTTP_201_CREATED, openapi_extra = {'errors': [bad_file]})
def upload_file(request: Request, file: UploadFile = File(..., description='Provide an avatar', media_type=['image/jpeg', 'image/png'])):

    # result = Upload_By_Chunk(request = request, file = file, flag = True)

    result = UploadManager.upload_image(request = request, file = file , flag = True)


    return result

@router.get('/', status_code = status.HTTP_200_OK, openapi_extra = {'errors': [database_error]})
def get_browsable_urls_in_sw3():

    return UploadManager.get_browsable_urls_in_sw3()
