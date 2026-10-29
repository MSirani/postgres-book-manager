"""create authors and books tables

Revision ID: 0001_authors_books
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_authors_books"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.UniqueConstraint("name", name="uq_authors_name"),
    )
    op.create_index("ix_authors_name", "authors", ["name"], unique=True)

    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["author_id"], ["authors.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_books_title", "books", ["title"], unique=False)
    op.create_index("ix_books_author_id", "books", ["author_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_books_author_id", table_name="books")
    op.drop_index("ix_books_title", table_name="books")
    op.drop_table("books")
    op.drop_index("ix_authors_name", table_name="authors")
    op.drop_table("authors")
