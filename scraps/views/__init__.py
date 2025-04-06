"""Scraps package initializer."""

from scraps.views.index import index
from scraps.views.saved_recipes import saved_recipes
from scraps.views.recipe import recipe
from scraps.views.user import show_user
from scraps.views.accounts import show_accounts_login, show_accounts_sign_up, login, create
from scraps.views.logout import logout
from scraps.views.calendar import calendar
from scraps.views.frontend_test import frontend_test
from scraps.views.select_ingredients import show_select_ingredients
from scraps.views.pantry import pantry
from scraps.views.test import test
from scraps.views.edit_profile import edit
