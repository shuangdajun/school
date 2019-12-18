"""empty message

Revision ID: e472ea2de93e
Revises: 
Create Date: 2019-12-13 16:41:56.573723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e472ea2de93e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Permission',
    sa.Column('perm_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('perm_name', sa.String(length=20), nullable=True),
    sa.Column('StartTime', sa.Date(), nullable=True),
    sa.Column('StopTime', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('perm_id')
    )
    op.create_table('PricesWarn',
    sa.Column('price_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_name', sa.String(length=20), nullable=True),
    sa.Column('teacher_name', sa.String(length=20), nullable=True),
    sa.Column('subject_name', sa.String(length=20), nullable=True),
    sa.Column('startTime', sa.Date(), nullable=True),
    sa.Column('stopTime', sa.Date(), nullable=True),
    sa.Column('ClassHours', sa.String(length=20), nullable=True),
    sa.Column('prices', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('price_id')
    )
    op.create_table('Role',
    sa.Column('role_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role_name', sa.String(length=20), nullable=True),
    sa.Column('StartTime', sa.Date(), nullable=True),
    sa.Column('StopTime', sa.Date(), nullable=True),
    sa.Column('description', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('role_id')
    )
    op.create_table('Students',
    sa.Column('student_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_name', sa.String(length=20), nullable=True),
    sa.Column('student_sex', sa.String(length=10), nullable=True),
    sa.Column('student_age', sa.Integer(), nullable=True),
    sa.Column('student_phone', sa.String(length=25), nullable=True),
    sa.Column('student_landline', sa.String(length=25), nullable=True),
    sa.PrimaryKeyConstraint('student_id'),
    sa.UniqueConstraint('student_name')
    )
    op.create_table('Subjects',
    sa.Column('subject_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('subject_name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('subject_id'),
    sa.UniqueConstraint('subject_name')
    )
    op.create_table('Teachers',
    sa.Column('teacher_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('teacher_name', sa.String(length=20), nullable=False),
    sa.Column('teacher_address', sa.String(length=100), nullable=True),
    sa.Column('teacher_phone', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('teacher_id'),
    sa.UniqueConstraint('teacher_name')
    )
    op.create_table('Prices',
    sa.Column('price_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('stu_id', sa.Integer(), nullable=True),
    sa.Column('tea_id', sa.Integer(), nullable=True),
    sa.Column('sub_id', sa.Integer(), nullable=True),
    sa.Column('startTime', sa.Date(), nullable=True),
    sa.Column('stopTime', sa.Date(), nullable=True),
    sa.Column('ClassHours', sa.String(length=20), nullable=True),
    sa.Column('prices', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['stu_id'], ['Students.student_id'], ),
    sa.ForeignKeyConstraint(['sub_id'], ['Subjects.subject_id'], ),
    sa.ForeignKeyConstraint(['tea_id'], ['Teachers.teacher_id'], ),
    sa.PrimaryKeyConstraint('price_id'),
    sa.UniqueConstraint('stu_id')
    )
    op.create_table('User',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user', sa.String(length=20), nullable=True),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('password', sa.String(length=20), nullable=True),
    sa.Column('startTime', sa.Date(), nullable=True),
    sa.Column('stopTime', sa.Date(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['Role.role_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user'),
    sa.UniqueConstraint('username')
    )
    op.create_table('to_role_permission',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('perm_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['perm_id'], ['Permission.perm_id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['Role.role_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('to_stu_sub',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('stu_id', sa.Integer(), nullable=True),
    sa.Column('sub_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['stu_id'], ['Students.student_id'], ),
    sa.ForeignKeyConstraint(['sub_id'], ['Subjects.subject_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('to_tea_sub',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sub_id', sa.Integer(), nullable=True),
    sa.Column('tea_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sub_id'], ['Subjects.subject_id'], ),
    sa.ForeignKeyConstraint(['tea_id'], ['Teachers.teacher_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('to_tea_sub')
    op.drop_table('to_stu_sub')
    op.drop_table('to_role_permission')
    op.drop_table('User')
    op.drop_table('Prices')
    op.drop_table('Teachers')
    op.drop_table('Subjects')
    op.drop_table('Students')
    op.drop_table('Role')
    op.drop_table('PricesWarn')
    op.drop_table('Permission')
    # ### end Alembic commands ###