from fastapi import UploadFile
import os
from config import settings
from typing import Union
import requests
def generate_filename(base_name, extension, counter, directory):
    new_filename = f"{base_name}_{counter}{extension}"
    generated_name = directory + new_filename

    if os.path.exists(generated_name):
        return generate_filename(base_name, extension, counter + 1, directory)
    
    return generated_name

class MediaHandler:
    media_dir = f"./{settings.media_filename}/"
    users_media_dir = settings.users_media_dir
    dealers_media_dir = settings.dealers_media_dir
    blogs_media_dir = settings.blogs_media_dir
    products_media_dir = settings.products_media_dir
    logos_media_dir = settings.logos_media_dir
    payment_methods_media_dir = settings.payment_methods_media_dir
    social_media_media_dir = settings.social_media_media_dir
    contacts_media_dir = settings.contacts_media_dir
    delivery_media_dir = settings.delivery_media_dir




    @staticmethod
    async def save_media(
        media: Union[list[UploadFile], UploadFile],
        directory: str,
    ) -> Union[list[str], str]:
        directory = MediaHandler.media_dir + directory

        if isinstance(media, list):
            # Если передан список файлов (media_group), обработаем его аналогично save_media_group.
            filenames = []
            for item in media:
                media_name = item.filename
                base_name, extension = os.path.splitext(media_name)
                generated_name = generate_filename(base_name, extension, 1, directory)                
                
                file_content = await item.read()
                with open(generated_name, 'wb') as media_file:
                    media_file.write(file_content)
                media_file.close()
                filename = generated_name[len(directory):] 
                filenames.append(filename)
            
            return filenames
        else:
            # Если передан одиночный файл (media), обработаем его аналогично update_media.
            media_name = media.filename
            base_name, extension = os.path.splitext(media_name)
            generated_name = generate_filename(base_name, extension, 1, directory)                
            
            file_content = await media.read()
            with open(generated_name, 'wb') as media_file:
                media_file.write(file_content)
            media_file.close()
            filename = generated_name[len(directory):] 

            return filename
        
    @staticmethod
    async def save_media_from_url(photo_objs: list[str], directory: str):
        saved_filenames = []
        directory = MediaHandler.media_dir + directory

        for photo_obj in photo_objs:
            url = photo_obj["photo_url"]
            # Проверьте, что URL действителен
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                # Обработайте ошибку, если URL недействителен
                print(f"Ошибка при получении медиафайла из URL: {str(e)}")
                return None

            
            # Получите имя файла из URL (последний сегмент URL)
            media_name = os.path.basename(url)
            base_name, extension = os.path.splitext(media_name)
            generated_name = generate_filename(base_name, extension, 1, directory)

            # Сохраните файл
            with open(generated_name, 'wb') as media_file:
                media_file.write(response.content)
            media_file.close()
            filename = generated_name[len(directory):]
            saved_filenames.append(filename)

        return saved_filenames







        
        
        

