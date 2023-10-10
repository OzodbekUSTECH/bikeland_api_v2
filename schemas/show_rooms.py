from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema

class CreateShowRoomSchema(CreateBaseModel):
    city: str
    address: str
    landmark: str
    phone_number: str
    location_url: str

class UpdateShowRoomSchema(UpdateBaseModel, CreateShowRoomSchema):
    pass

class ShowRoomSchema(IdResponseSchema, UpdateShowRoomSchema):
    pass