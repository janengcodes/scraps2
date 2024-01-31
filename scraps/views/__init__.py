"""Scraps package initializer."""

from scraps.views.index import index
from scraps.views.index2 import index2
from scraps.views.pantry import pantry
from scraps.views.saved_recipes import saved_recipes
from scraps.views.recipe import recipe
from scraps.views.results import results
from scraps.views.user import show_user
from scraps.views.pantry_main import pantry_main
from scraps.views.accounts import show_accounts_login, show_accounts_sign_up, login, create
# from scraps.views.sign_in import sign_in
from scraps.views.accounts import show_accounts_login
from scraps.views.recipes import get_recipes
from scraps.views.logout import logout
from scraps.views.calendar import calendar
from scraps.views.frontend_test import frontend_test
from scraps.views.proteins import proteins
from scraps.views.produce import produce
from scraps.views.dairy import dairy
from scraps.views.grains import grains
from scraps.views.dietarypreferences import dietarypreferences
from scraps.views.buildrecipes import buildrecipes
from scraps.views.allergens import allergens
