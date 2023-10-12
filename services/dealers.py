from schemas.dealers import CreateDealerSchema, UpdateDealerSchema
import models
from database import uow
from utils.media_handler import MediaHandler

class DealersService:

    async def create_dealer(self, dealer_data: CreateDealerSchema) -> models.Dealer:
        dealer_dict = dealer_data.model_dump()
        if dealer_data.filename is not None:
            filename = await MediaHandler.save_media(dealer_data.filename, MediaHandler.dealers_media_dir)
            dealer_dict["filename"] = filename

        async with uow:
            dealer: models.Dealer = await uow.dealers.create(dealer_dict)
            tgclient: models.TgClient = await uow.tgclients.get_one_by_phone_number(phone_number=dealer.phone_number)
            if tgclient:
                dealer.telegram_id = tgclient.telegram_id
            await uow.commit()
            return dealer
        
    async def get_dealers(self) -> list[models.Dealer]:
        async with uow:
            return await uow.dealers.get_all()
        
    async def get_dealer_by_id(self, id: int) -> models.Dealer:
        async with uow:
            return await uow.dealers.get_by_id(id)
        
    async def update_dealer(self, id: int, dealer_data: UpdateDealerSchema) -> models.Dealer:
        dealer_dict = dealer_data.model_dump(exclude={"filename"})
        if dealer_data.filename is not None:
            filename = await MediaHandler.save_media(dealer_data.filename, MediaHandler.dealers_media_dir)
            dealer_dict["filename"] = filename
        
        async with uow:
            dealer: models.Dealer = await uow.dealers.get_by_id(id)
            dealer = await uow.dealers.update(dealer.id, dealer_dict)
            tgclient: models.TgClient = await uow.tgclients.get_one_by_phone_number(phone_number=dealer.phone_number)
            if tgclient:
                dealer.telegram_id = tgclient.telegram_id
            await uow.commit()
            return dealer
        
    async def delete_dealer(self, id: int) -> models.Dealer:
        async with uow:
            dealer: models.Dealer = await uow.dealers.get_by_id(id)
            await uow.dealers.delete(dealer.id)
            await uow.commit()
            return dealer
    
dealers_service = DealersService()