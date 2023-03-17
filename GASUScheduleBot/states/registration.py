from aiogram.dispatcher.filters.state import StatesGroup, State

class RegistrationStates(StatesGroup):

    RegisterGroup = State()
    RegisterGroupFromInline = State()
    RegistrationComplete = State()
    ChangeGroup = State()