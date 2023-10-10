"""blogs

Revision ID: 7f6297c2d336
Revises: 369220800a2e
Create Date: 2023-10-10 12:03:10.728908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f6297c2d336'
down_revision: Union[str, None] = '369220800a2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('blog_media_groups_blog_id_fkey', 'blog_media_groups', type_='foreignkey')
    op.create_foreign_key(None, 'blog_media_groups', 'blogs', ['blog_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'blog_media_groups', type_='foreignkey')
    op.create_foreign_key('blog_media_groups_blog_id_fkey', 'blog_media_groups', 'blogs', ['blog_id'], ['id'])
    # ### end Alembic commands ###
