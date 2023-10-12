# # Исходные данные
# product_data_c = {
#     "items": [
#         {
#             "created_at": "28.06.2022 16:52:41",
#             "updated_at": None,
#             "description": None,
#             # ...
#             "photos": [
#                 {
#                     "created_at": "12.10.2023 00:09:47",
#                     "product_id": 260,
#                     "id": 353,
#                     "photo_url": "https://api.bikeland.uz/media/products//1.jpg"
#                 },
#                 {
#                     "created_at": "12.10.2023 00:09:47",
#                     "product_id": 260,
#                     "id": 352,
#                     "photo_url": "https://api.bikeland.uz/media/products//2.jpg"
#                 },
#                 {
#                     "created_at": "12.10.2023 00:09:47",
#                     "product_id": 260,
#                     "id": 351,
#                     "photo_url": "https://api.bikeland.uz/media/products//3.jpg"
#                 },
#                 # ... другие фотографии
#             ]
#         }
#     ]
# }

# product_data = {
#     "items": [
#         {
#             "created_at": "28.06.2022 16:52:41",
#             "updated_at": None,
#             "description": None,
#             # ...
#             "photos": [
#                 {
#                     "created_at": "12.10.2023 00:09:47",
#                     "product_id": 260,
#                     "id": 353,
#                     "photo_url": "https://api.bikeland.uz/media/products//1.jpg"
#                 },
#                 {
#                     "created_at": "12.10.2023 00:09:47",
#                     "product_id": 260,
#                     "id": 352,
#                     "photo_url": "https://api.bikeland.uz/media/products//2.jpg"
#                 },
#                 {
#                     "created_at": "12.10.2023 00:09:47",
#                     "product_id": 260,
#                     "id": 351,
#                     "photo_url": "https://api.bikeland.uz/media/products//3.jpg"
#                 },
#                 # ... другие фотографии
#             ]
#         }
#     ]
# }



# # Проходим по товарам и изменяем порядок символов в URL фотографий
# # Проходим по товарам и изменяем порядок символов в URL фотографий
# # Проходим по товарам и меняем порядок элементов в списке photos
# # Перебираем фотографии в product_data_c и product_data
# for photo_c, photo in zip(product_data_c["items"][0]["photos"], product_data["items"][0]["photos"][::-1]):
#     photo_c["photo_url"] = photo["photo_url"]

# # Выводим обновленный product_data_c
# print(product_data_c)



