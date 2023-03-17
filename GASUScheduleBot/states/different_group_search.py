from aiogram.dispatcher.filters.state import StatesGroup, State


class DifferentGroupSearchStates(StatesGroup):

    FindGroup = State()
    GroupFound = State()