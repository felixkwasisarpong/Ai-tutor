"""restore placeholder for missing migration

Revision ID: fe934723b720
Revises:
Create Date: 2026-01-20 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "fe934723b720"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "departments",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("faculty", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_departments_code"), "departments", ["code"], unique=True)

    op.create_table(
        "courses",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("department_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["department_id"],
            ["departments.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_courses_code"), "courses", ["code"], unique=True)

    op.create_table(
        "documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("document_type", sa.String(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("uploaded_by", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["courses.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_documents_course_id"), "documents", ["course_id"], unique=False)
    op.create_index(op.f("ix_documents_active"), "documents", ["active"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_documents_active"), table_name="documents")
    op.drop_index(op.f("ix_documents_course_id"), table_name="documents")
    op.drop_table("documents")
    op.drop_index(op.f("ix_courses_code"), table_name="courses")
    op.drop_table("courses")
    op.drop_index(op.f("ix_departments_code"), table_name="departments")
    op.drop_table("departments")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
