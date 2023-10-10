import httpx
from schemas.products import CreateProductSchema
from models import Product

class ParserHandler:
    url = "http://jurayed.uz/bl/hs/goods"
    username = "ws"
    password = "ws" 

    @staticmethod
    async def get_all_1c_products() -> list[dict]:
        async with httpx.AsyncClient(auth=(ParserHandler.username, ParserHandler.password)) as client:
            response = await client.get(ParserHandler.url)
            response.raise_for_status()
            products = response.json()

            data = products["Data"]
            return data
    
    @staticmethod
    async def get_filtered_products():
        products = await ParserHandler.get_all_1c_products()
        filtered_products = {}

        for product in products:
            naimenovanie = product.get("naimenovanie")
            if naimenovanie:
                if naimenovanie not in filtered_products:
                    # Если товар с таким названием еще не добавлен, создаем запись в словаре
                    filtered_products[naimenovanie] = product
                    filtered_products[naimenovanie]['keys'] = [product['kod']]  # Создаем список keys
                else:
                    # Если товар с таким названием уже есть, добавляем key к списку keys
                    filtered_products[naimenovanie]['keys'].append(product['kod'])
                    # Также складываем значения 'ostatok'
                    filtered_products[naimenovanie]['ostatok'] += product.get("ostatok", 0)

        # Преобразуем словарь в список значений
        filtered_product_list = list(filtered_products.values())
        return filtered_product_list
    

    
    @staticmethod
    async def create_product_dict(
        product: dict,
    ) -> dict:
        product_data = CreateProductSchema(
            title=product.get('naimenovanie', ""),
            quantity= product.get('ostatok'),
            key = product.get("kod", ""), 
            uzb_price = product.get("cena", 0), #check
            usd_price= product.get("cenaVal", 0), #check
            is_deleted = product.get('pometka_udaleniya', False), #eto
            created_at=product.get('dataSozdaniya') 
        )

        return product_data.model_dump()
    
    @staticmethod
    async def has_changes_in_columns_of_1C_products(
        our_product: Product,
        their_product: dict,
    ):  
        # counter = await ParserHandler.count_quantity_of_1c_products(their_product.get("naimenovanie", ""))
        if our_product.title != their_product.get("naimenovanie", ""):
            return True
        elif our_product.quantity != their_product.get("ostatok"):
            return True
        elif our_product.uzb_price != their_product.get("cena", 0):
            return True
        elif our_product.is_deleted != their_product.get("pometka_udaleniya", False):
            return True
       
        
        else:
            return False
    
    
    