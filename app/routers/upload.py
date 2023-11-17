from fastapi import  APIRouter , UploadFile , File , status

from utils.AvatarUpload import Upload_Avatar


router = APIRouter(
    prefix = '/upload',
    tags = ['Upload']
)
@router.post('/', status_code = status.HTTP_201_CREATED)
def upload_file(file: UploadFile = File(..., description='Provide an avatar', media_type=['image/jpeg', 'image/png'])):
    result = Upload_Avatar(file)

    return result
