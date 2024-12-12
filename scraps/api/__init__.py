# """Scraps REST API."""

from scraps.api.saved_recipes import api_saved_recipes
from scraps.api.user import check_login
from scraps.api.pantry import get_pantry, add_to_pantry
from scraps.api.cuisine import find_size, get_data, peekData, train_model, load_and_prepare_data