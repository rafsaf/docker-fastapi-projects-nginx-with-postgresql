import tortoise.fields.data as fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(Model):
    """
    The User model
    """

    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=50, unique=True)
    name = fields.CharField(max_length=50, null=True)
    family_name = fields.CharField(max_length=50, null=True)
    password_hash = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)

    def full_name(self) -> str:
        """
        Returns the best name
        """
        if self.name or self.family_name:
            return f"{self.name or ''} {self.family_name or ''}".strip()
        return self.email

    class PydanticMeta:
        computed = ["full_name"]
        exclude = ["password_hash"]


User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)
