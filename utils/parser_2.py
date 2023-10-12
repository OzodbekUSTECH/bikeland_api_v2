import httpx

from schemas import CreateBaseModel
from pydantic import Field
class CreateProduct(CreateBaseModel):
    title: str
    description: str | None
    status_id: int
    quantity: int | None
    min_quantity: int | None
    key: str | None
    tag: str | None
    uzb_price: int | None
    usd_price: int | None
    video_link: str | None
    # dealer_id: int | None
    category_id: int | None
    sub_category_id: int | None
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
    is_deleted: bool
    show_on_main_page: bool
    show_on_see_also: bool
    created_at: str
    updated_at: str | None
    photos: list = Field(exclude=True)

class CreateCategory(CreateBaseModel):
    name: str

class CreateSubCategory(CreateBaseModel):
    name: str
    category_id: int

class CreateBrand(CreateBaseModel):
    name: str

class CreateCategory(CreateBaseModel):
    title: str
    meta_description: str | None
    description: str
    updated_at: str | None
    photos: list = Field(exclude=True)    

class ParserHandlerSecond:
    products_url = "https://api.it-test.uz/v1/products?with_pagination=false&page=1&size=50"
    categories_url = "https://api.it-test.uz/v1/categories"
    sub_categories_url = "https://api.it-test.uz/v1/sub/categories"
    brands_url = "https://api.it-test.uz/v1/brands"
    blogs_url = "https://api.it-test.uz/v1/blogs?with_pagination=false&page=1&size=50"

    @staticmethod
    async def get_all_data_by_url(url: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            items = response.json()

            
            return items

   
      
        
    @staticmethod
    async def create_product_model(product: dict) -> CreateProduct:
        model = CreateProduct.model_validate(product)
        return model

    @staticmethod
    async def create_category_model(category: dict) -> CreateCategory:
        model = CreateCategory.model_validate(category)
        return model
    
    @staticmethod
    async def create_sub_category_model(subcategory: dict) -> CreateSubCategory:
        model = CreateSubCategory.model_validate(subcategory)
        return model
    
    @staticmethod
    async def create_brand_model(brand: dict) -> CreateBrand:
        model = CreateBrand.model_validate(brand)
        return model
    
    @staticmethod
    async def create_blog_model(blog: dict) -> CreateCategory:
        model = CreateCategory.model_validate(blog)
        return model