from starlette_admin import HasMany, StringField

from starlette_admin.contrib.sqla.ext.pydantic import ModelView


class RoleView(ModelView):
    """Модель для отображения ролей."""

    row_actions  = ['view']
    identity = "role"
    fields = [
        StringField("name", label="Название роли"),
        HasMany("administrations", label="Администраторы", identity="administration")
    ]
    label = "Роли"
    sortable_fields = ["name"]
    fields_default_sort = ["name"]
