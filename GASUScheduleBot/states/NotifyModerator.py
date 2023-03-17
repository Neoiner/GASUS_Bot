from aiogram.dispatcher.filters.state import StatesGroup, State

class NotifyModeratorStates(StatesGroup):

    Faculty = State()
    Group = State()
    ModeratorNotify = State()
    ModeratorNotifyFaculty = State()
    NotifyForFaculty = State()