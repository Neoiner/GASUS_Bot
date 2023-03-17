from aiogram.dispatcher.filters.state import StatesGroup, State

class NotifyFaculty_Group(StatesGroup):

    Faculty = State()
    Group = State()
    Continue = State()
    ChangeFaculty = State()
    ChangeYear = State()
    StartNotifyGroup = State()
    DeleteGroup = State()