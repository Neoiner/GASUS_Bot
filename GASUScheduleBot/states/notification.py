from aiogram.dispatcher.filters.state import StatesGroup, State


class Notification(StatesGroup):
    SetupMessage = State()
    SetupSurveyHeader = State()
    SetupSurveyOptions = State()