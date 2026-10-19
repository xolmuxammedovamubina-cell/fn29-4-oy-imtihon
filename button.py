from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def asosiy_menyu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📚 Kurslar")],
            [KeyboardButton(text="📝 Kursga yozilish")],
            [KeyboardButton(text="ℹ️ Markaz haqida")],
            [KeyboardButton(text="📞 Aloqa")],
        ],
        resize_keyboard=True,
    )


def bekor_tugmasi():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True,
    )


def kurslar_tugmasi():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🐍 Python",
                    callback_data="course_python",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌐 Web dasturlash",
                    callback_data="course_web",
                )
            ],
            [
                InlineKeyboardButton(
                    text="💻 Frontend",
                    callback_data="course_frontend",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎨 Grafik dizayn",
                    callback_data="course_design",
                )
            ],
        ]
    )


def tasdiqlash_tugmasi():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Tasdiqlash",
                    callback_data="confirm_registration",
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="cancel_registration",
                )
            ],
        ]
    )
