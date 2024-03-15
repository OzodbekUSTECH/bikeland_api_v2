from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema
from pydantic import BaseModel
class CreateBackCallWidgetSchema(CreateBaseModel):
    phone_number: str

class UpdateBackCallWidgetSchema(UpdateBaseModel, CreateBackCallWidgetSchema):
    pass

class BackCallWidgetSchema(IdResponseSchema, UpdateBackCallWidgetSchema):
    pass

#############################
class BaseFormModel(BaseModel):
    full_name: str
    phone_number: str
    location: str
    known_from: str

#############################

class CreateBackCallFormSchema(CreateBaseModel, BaseFormModel):
    pass

class UpdateBackCallFormSchema(UpdateBaseModel, CreateBackCallFormSchema):
    pass

class BackCallFormSchema(IdResponseSchema, UpdateBackCallFormSchema):
    pass

# ----------------------------------------------------------------
class CreateWorkWithUsFormSchema(CreateBaseModel, BaseFormModel):
    about: str

class UpdateWorkWithUsFormSchema(UpdateBaseModel, CreateWorkWithUsFormSchema):
    pass

class WorkWithUsFormSchema(IdResponseSchema, UpdateWorkWithUsFormSchema):
    pass

#-----------------------------------------------

class CreateLinkGoogleForm(CreateBaseModel):
    description: str
    btn_name: str
    btn_url: str

class UpdateLinkGoogleForm(UpdateBaseModel, CreateLinkGoogleForm):
    pass

class LinkGoogleForm(IdResponseSchema, UpdateLinkGoogleForm):
    pass