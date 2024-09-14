"""added_table_users_progects_categories

Revision ID: 9df39095da9d
Revises: 
Create Date: 2024-09-13 16:50:30.942577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy.orm import Session
from users.models import UserOrm
from users.auth import get_password_hash
from config import ADMIN_EMAIL, ADMIN_PASSWORD


# revision identifiers, used by Alembic.
revision: str = '9df39095da9d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('description', sa.String(), nullable=True),
            sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
            sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('occupation', sa.String(), nullable=True),
    sa.Column('company', sa.String(), nullable=True),
    sa.Column('photo', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('is_super', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('cat_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('photos', sa.JSON(), nullable=True),
    sa.Column('views', sa.Integer(), nullable=True),
    sa.Column('likes', sa.Integer(), nullable=True),
    sa.Column('tags', sa.JSON(), nullable=True),
    sa.Column('contenttype', sa.String(), nullable=True),
    sa.Column('orientation', sa.String(), nullable=True),
    sa.Column('size', sa.String(), nullable=True),
    sa.Column('colorscheme', sa.String(), nullable=True),
    sa.Column('popularity', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
    sa.ForeignKeyConstraint(['cat_id'], ['categories.id'], onupdate='RESTRICT', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='RESTRICT', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )

    bind = op.get_bind()
    session = Session(bind=bind)

    # Створення адміністратора
    admin_pass = ADMIN_PASSWORD
    admin_user = UserOrm(
        email=ADMIN_EMAIL,
        password=get_password_hash(admin_pass),
        is_super=True,
    )
    session.add(admin_user)
    session.commit()
    print("*" * 60)
    print(f"Create superuser, email: {admin_user.email}, password: {admin_pass}")
    print("Please log in as an superuser and change your password")
    print("*" * 60)

    # Додавання тригера до таблиці projects
    op.execute("""
               CREATE OR REPLACE FUNCTION update_updated_at()
               RETURNS TRIGGER AS $$
               BEGIN
                   NEW.updated_at = NOW();
                   RETURN NEW;
               END;
               $$ LANGUAGE plpgsql;
           """)

    op.execute("""
               CREATE TRIGGER set_updated_at
               BEFORE UPDATE ON public.projects
               FOR EACH ROW
               EXECUTE FUNCTION update_updated_at();
           """)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('projects')
    op.drop_table('users')
    op.drop_table('categories')

    # Видалення тригера і функції в разі відкату міграції
    op.execute("""DROP TRIGGER IF EXISTS set_updated_at ON public.projects;""")
    op.execute("""DROP FUNCTION IF EXISTS update_updated_at();""")
    # ### end Alembic commands ###
