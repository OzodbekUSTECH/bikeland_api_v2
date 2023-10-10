from schemas.blogs import (
    CreateBlogMediaGroup,
    CreateBlogSchema,
    UpdateBlogSchema
)
import models
from database import uow
from utils.media_handler import MediaHandler
from fastapi import UploadFile
class BlogsService:

    async def create_blog(self, blog_data: CreateBlogSchema) -> models.Blog:
        async with uow:
            blog: models.Blog = await uow.blogs.create(blog_data.model_dump())
            filenames = await MediaHandler.save_media(blog_data.media_group, MediaHandler.blogs_media_dir)
            await uow.blog_media_group.bulk_create(
                data_list=[CreateBlogMediaGroup(
                    blog_id=blog.id,
                    filename=filename
                ).model_dump() for filename in filenames]
            )

            await uow.commit()

            return blog
        
    async def get_blogs(self) -> list[models.Blog]:
        async with uow:
            return await uow.blogs.get_all(reverse=True)
        
    async def get_blog_by_id(self, id: int) -> models.Blog:
        async with uow:
            return await uow.blogs.get_by_id(id)
        
    async def update_blog(self, id: int, blog_data: UpdateBlogSchema) -> models.Blog:
        async with uow:
            blog: models.Blog = await uow.blogs.get_by_id(id)
            await uow.blogs.update(blog.id, blog_data.model_dump())
            await uow.commit()
            return blog
        
    async def delete_blog(self, id: int) -> models.Blog:
        async with uow:
            blog: models.Blog = await uow.blogs.get_by_id(id)
            blog = await uow.blogs.delete(blog.id)
            await uow.commit()
            return blog
    

    ################################ blog media group ################################
    async def add_media_group(self, blog_id: int, media_group: list[UploadFile]) -> None:
        async with uow:
            blog: models.Blog = await uow.blogs.get_by_id(id)

            filenames = await MediaHandler.save_media(media_group, MediaHandler.blogs_media_dir)
            await uow.blog_media_group.bulk_create(
                data_list=[CreateBlogMediaGroup(
                    blog_id=blog.id,
                    filename=filename
                ).model_dump() for filename in filenames]
            )
            await uow.commit()

    async def delete_photo(self, id: int) -> models.BlogMediaGroup:
        async with uow:
            blog_photo: models.BlogMediaGroup = await uow.blog_media_group.get_by_id(id)
            await uow.blog_media_group.delete(blog_photo.id)
            await uow.commit()
            return blog_photo

blogs_service = BlogsService()