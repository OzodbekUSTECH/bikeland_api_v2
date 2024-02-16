from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema
from pydantic import Field

class CustomCategorySchema(IdResponseSchema):
    name: str    

################################################################
class CreateProductMediaGroup(CreateBaseModel):
    product_id: int
    filename: str

class ProductMediaGroup(IdResponseSchema, CreateProductMediaGroup):
    photo_url: str

    filename: str = Field(exclude=True)



class CreateProductSchema(CreateBaseModel):
    title: str
    quantity: int
    key: str
    uzb_price: int
    usd_price: int
    is_deleted: bool

class UpdateProductSchema(UpdateBaseModel):
    description: str | None
    min_quantity: int 
    video_link: str | None
    tag: str | None
    weight: str | None
    clearance: str | None
    fuel_tank_volume: str | None
    fuel_consumption: str | None
    engine: str | None
    max_power: str | None
    max_speed: str | None 
    ignition_system: str | None
    gearbox: str | None
    main_gear: str | None
    front_lighting: str | None
    back_lighting: str | None
    front_brake: str | None
    back_brake: str | None
    front_tires: str | None
    back_tires: str | None
    sizes: str | None

    show_on_main_page: bool
    show_on_see_also: bool

    dealer_id: int | None
    category_id: int | None
    sub_category_id: int | None
    brand_id: int | None

    photos: list | None = None

from schemas.statuses import StatusSchema
from schemas.sub_categories import SubCategorySchema
from schemas.brands import BrandSchema
from schemas.dealers import DealerSchema
from schemas.product_options import ProductOptionSchema
from schemas.product_video_links import ProductVideoLinkSchema
from fastapi import UploadFile
class CustomDealerSchema(IdResponseSchema):
    full_name: str
    filename: UploadFile | None
    phone_number: str

class ProductSchema(IdResponseSchema, CreateProductSchema, UpdateProductSchema):
    photos: list[ProductMediaGroup]
    status: StatusSchema
    dealer: CustomDealerSchema | None
    category: CustomCategorySchema | None   
    sub_category: SubCategorySchema | None
    brand: BrandSchema | None
    options: list[ProductOptionSchema]
    video_links: list[ProductVideoLinkSchema]

    dealer_id: int | None = Field(exclude=True)
    category_id: int | None = Field(exclude=True)
    sub_category_id: int | None = Field(exclude=True)
    brand_id: int | None = Field(exclude=True)



