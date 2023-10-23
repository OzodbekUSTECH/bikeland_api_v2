from database import UnitOfWork
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from telegram.states import WelcomeStates
from telegram.reply_kbs import rkbs_handler
import models
from schemas.tgclients import CreateTgClientSchema, UpdateTgClientSchema
class WelcomeService:

    async def _say_welcome(self, uow: UnitOfWork, message: Message) -> None:
        dealers: list[models.Dealer] = await uow.dealers.get_all_without_pagination()
        dealers_tg_id = [dealer.telegram_id for dealer in dealers if dealer.telegram_id]
        rkb_markup = await rkbs_handler.get_welcome_rkbs(tg_id=message.from_user.id, dealers_tg_id=dealers_tg_id)
        message_text = (
            "Добро пожаловать в BIKELAND bot,\n"
            f"{message.from_user.full_name}"
        )
        await message.answer(message_text, reply_markup=rkb_markup)

    async def ask_for_contacts(self, message: Message, state: FSMContext, uow: UnitOfWork) -> None:
            existing_tgclient = await uow.tgclients.get_one_by(telegram_id=message.from_user.id)
            if not existing_tgclient:

                rkb_markup = await rkbs_handler.get_sender_contact()
                message_text = (
                    "Для начала работы с ботом BikelandUz нужно зарегистрироваться, нажмите «отправить контакт»"
                )
                await state.set_state(WelcomeStates.contact)
                await message.answer(message_text, reply_markup=rkb_markup)
            
            else:
                await self._say_welcome(uow, message)

    async def _is_dealer(self, message: Message, uow: UnitOfWork) -> None:
        dealer: models.Dealer = await uow.dealers.get_one_by_phone_number(message.contact.phone_number)
        if dealer:
            dealer.telegram_id = message.from_user.id
            

    async def register_tg_client(self, message: Message, state: FSMContext, uow: UnitOfWork) -> None:
        if not message.contact:
            await self.ask_for_contacts(message, state, uow)
        else:
                await self._is_dealer(message, uow)
                existing_tg_client: models.TgClient = await uow.tgclients.get_one_by_phone_number(message.contact.phone_number)
                if not existing_tg_client:
                    client_dict = CreateTgClientSchema(
                        telegram_id=message.from_user.id,
                        full_name=message.from_user.full_name,
                        username=message.from_user.username,
                        phone_number=message.contact.phone_number
                    ).model_dump()
                    await uow.tgclients.create(client_dict)
                else:
                    client_dict = UpdateTgClientSchema(
                        telegram_id=message.from_user.id,
                        full_name=message.from_user.full_name,
                        username=message.from_user.username,
                        phone_number=message.contact.phone_number
                    ).model_dump()
                    await uow.tgclients.update(existing_tg_client.id, client_dict)

                await uow.commit()
                await state.clear()
                await self._say_welcome(uow, message)
                    
                    

welcome_service = WelcomeService()