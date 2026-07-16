from starlette_admin.contrib.sqlmodel import ModelView

from app.modules.favourites.models import Favourite
from app.modules.spots.models import Spot
from app.modules.users.models import User

def register_admin_views(admin) -> None:
    admin.add_view(
        ModelView(
            User, name="Users",
            icon="fa fa-users"
        )
    )
    admin.add_view(
        ModelView(
            Favourite, name="Favourites",
            icon="fa fa-heart"
        )
    )
    admin.add_view(
        ModelView(
            Spot, name="Spots",
            icon="fa fa-map-marker"
        )
    )
