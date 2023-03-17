from aiogram.dispatcher.filters.state import StatesGroup, State

class SubscriptionSetupStates(StatesGroup):

    SelectType = State()
    SelectSubType = State()
    SelectTime = State()
    