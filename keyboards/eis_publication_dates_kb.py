from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def kb_creator(documents):
    buttons = [
        InlineKeyboardButton(text=document[1].strftime('%Y-%m-%d %H:%M'),
                             callback_data=f'document_{document[0]}') for document in documents
    ]
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(width=3, *buttons)
    return kb_builder.as_markup()
