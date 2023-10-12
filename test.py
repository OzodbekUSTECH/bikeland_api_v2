# # import re

# # text = [
# #     "№ 892412. Комплект крашенного пластика CLICK/50QT-14 (красный Ламборгини.) 11-деталей (комплект)",
# #     "№LF1752СF0201. Clutch Lever Comp",
# #     "№201268. Задние амортизаторы CUB завод оригинал (пара)",
# #     "№201268 Задние амортизаторы CUB завод оригинал (пара)",
# #     "№ 201268 Задние амортизаторы CUB завод оригинал (пара)",
# #     "№ 201268 Задние амортизаторы. CUB завод оригинал (пара)",
# #     "№ 892412. Комплект крашенного пластика CLICK/50QT-14. (красный Ламборгини.) 11-деталей (комплект)",
# #     "№LF15013F0310. Рычаг переднего барабанного тормоза c хомутом LF150-13 (F03-10)",
# #     "№ 892434. Элемент пластика 50QT-12X / ITALIA. Порог левый Цвет: черный"
# # ]

# # for t in text:
# #     cleaned_text = re.sub(r'^№\s*\S+\s*', '', t).strip()  # Updated regex pattern

# #     print(cleaned_text)


# # text = "79017440007"
# # print(text.replace("+", ""))

# # import asyncio
# # from telegram.services import welcome_service

# # if __name__ == "__main__":
# #     asyncio.run(welcome_service.check_users_and_telegram_clients())
# import asyncio
# import services
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
    
    
    
#     # Добавляем задержку в 60 секунд, чтобы скрипт оставался активным.
    

# # if __name__ == "__main__":
# scheduler = AsyncIOScheduler()

# scheduler.add_job(services.parser_service.check_products_from_1c, 'cron', hour=2, minute=2)
# scheduler.start()

# asyncio.get_event_loop().run_forever()

