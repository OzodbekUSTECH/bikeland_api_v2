# # # import re

# # # text = [
# # #     "№ 892412. Комплект крашенного пластика CLICK/50QT-14 (красный Ламборгини.) 11-деталей (комплект)",
# # #     "№LF1752СF0201. Clutch Lever Comp",
# # #     "№201268. Задние амортизаторы CUB завод оригинал (пара)",
# # #     "№201268 Задние амортизаторы CUB завод оригинал (пара)",
# # #     "№ 201268 Задние амортизаторы CUB завод оригинал (пара)",
# # #     "№ 201268 Задние амортизаторы. CUB завод оригинал (пара)",
# # #     "№ 892412. Комплект крашенного пластика CLICK/50QT-14. (красный Ламборгини.) 11-деталей (комплект)",
# # #     "№LF15013F0310. Рычаг переднего барабанного тормоза c хомутом LF150-13 (F03-10)",
# # #     "№ 892434. Элемент пластика 50QT-12X / ITALIA. Порог левый Цвет: черный"
# # # ]

# # # for t in text:
# # #     cleaned_text = re.sub(r'^№\s*\S+\s*', '', t).strip()  # Updated regex pattern

# # #     print(cleaned_text)


# # # text = "79017440007"
# # # print(text.replace("+", ""))

# # # import asyncio
# # # from telegram.services import welcome_service

# # # if __name__ == "__main__":
# # #     asyncio.run(welcome_service.check_users_and_telegram_clients())
# # import asyncio
# # import services
# # from apscheduler.schedulers.asyncio import AsyncIOScheduler
    
    
    
# #     # Добавляем задержку в 60 секунд, чтобы скрипт оставался активным.
    

# # # if __name__ == "__main__":
# # scheduler = AsyncIOScheduler()

# # scheduler.add_job(services.parser_service.check_products_from_1c, 'cron', hour=2, minute=2)
# # scheduler.start()

# # asyncio.get_event_loop().run_forever()

# # from services import products_service

# # import asyncio

# # asyncio.run(products_service.change_sub_status())

# products_url = "https://api.minzifatravel.ru/v1/users?page=1&size=50"
# categories_url = "https://api.minzifatravel.ru/v1/roles/en?page=1&size=50"
# sub_categories_url = "https://api.minzifatravel.ru/v1/activities/en?page=1&size=50"
# sub_categories_url2 = "https://api.minzifatravel.ru/v1/languages/en?page=1&size=50"
# sub_categories_url3 = "https://api.minzifatravel.ru/v1/accommodations/en?page=1&size=50"
# brands_url = "https://api.minzifatravel.ru/v1/tours?locale=en&only_with_discounts=false&page=1&size=50"
# blogs_url = "https://api.minzifatravel.ru/v1/tour/comments/en?page=1&size=50"
# blogs_url2 = "https://api.minzifatravel.ru/v1/blogs?locale=en&page=1&size=50"

# import asyncio
# import aiohttp

# async def fetch_url(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return await response.text()

# async def main():
#     urls = [products_url] * 10  # Создайте список URL-ов для запросов

#     # Создайте список задач для выполнения запросов
#     tasks = [fetch_url(url) for url in urls]

#     # Запустите все задачи параллельно
#     responses = await asyncio.gather(*tasks)

#     # Обработайте ответы здесь, например, выведите содержимое или сохраните в файл

# if __name__ == "__main__":
#     asyncio.run(main())
