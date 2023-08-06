from src import api
from src.resources.film import FilmList
from src.resources.actor import ActorList
from src.resources.auth import AuthRegister
from src.resources.auth import AuthLogin

api.add_resource(FilmList, '/films', '/films/<uuid>', strict_slashes=False)
api.add_resource(ActorList, '/actors', '/actors/<uuid>', strict_slashes=False)
api.add_resource(AuthRegister, '/register', strict_slashes=False)
api.add_resource(AuthLogin, '/login', strict_slashes=False)
