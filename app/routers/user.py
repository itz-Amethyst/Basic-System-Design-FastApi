from fastapi import Depends , HTTPException , status , APIRouter , UploadFile , File , Request , Form
from pydantic import SecretStr , EmailStr
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models.user import RoleOptions
from app.deps.auth import user_required
from app.managers import UserManager , PermissionManager
from app import schemas
from app.deps import rate_limit

from app.db.models import User
from Cyrus import cache

router = APIRouter(
    prefix = '/user',
    # You can add multiple tags
    tags = ['Users'],
    dependencies = [Depends(user_required), Depends(PermissionManager.is_admin), rate_limit('user', 60, 30)]
)

@router.post('/', status_code = status.HTTP_201_CREATED, response_model = schemas.UserView)
async def create_user(request: Request, email: EmailStr = Form(),
    password: SecretStr = Form(),
    # is_superuser: bool = Form(),
    terms_of_service_accepted: bool = Form(),
    profile_picture: UploadFile = File(...)):

    # user_data = {
    #     "email": email,
    #     "password": password,
    #     "terms_of_service_accepted": terms_of_service_accepted,
    #     "profile_picture": profile_picture
    # }

    user_data = schemas.UserRegister(
        email = email,
        password = password,
        terms_of_service_accepted = terms_of_service_accepted,
        profile_picture = profile_picture
    )


    return await UserManager.register(user_data, request)

@router.get('/{id}', response_model = schemas.UserView)
@cache(expire = 30)
def get_user(id: str, db: Session = Depends(get_db)):

    user = db.query(User).get(id)

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with this id {id} does not exists")

    return user

# Note Careful about dependency order check is user logged in must be at first position
# , dependencies = [ Depends(AuthManager.get_current_user) ,Depends(PermissionManager.is_admin)], openapi_extra = {'errors': [same_role]}

@router.post('/{id}', response_model = schemas.UserView)
def change_role(id:str, role: RoleOptions):

    return UserManager.ChangeRole(user_id = id, role = role)