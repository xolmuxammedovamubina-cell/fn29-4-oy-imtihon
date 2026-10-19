import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery

from buttons import (
    asosiy_menyu,
    bekor_tugmasi,
    kurslar_tugmasi,
    tasdiqlash_tugmasi,
)

bot = Bot(token="8921325720:AAHixlerpHsBf2_g0IedaQi2qKPnXMVuMHA")

dp = Dispatcher(storage=MemoryStorage())


class RoyxatdanOtish(StatesGroup):
    ism = State()
    telefon = State()
    kurs = State()
    tasdiqlash = State()


KURSLAR = {
    "course_python": {
        "nom": "Python",
        "davomiylik": "4 oy",
        "narx": "800 000 so'm/oy",
    },
    "course_web": {
        "nom": "Web dasturlash",
        "davomiylik": "6 oy",
        "narx": "1 000 000 so'm/oy",
    },
    "course_frontend": {
        "nom": "Frontend",
        "davomiylik": "5 oy",
        "narx": "900 000 so'm/oy",
    },
    "course_design": {
        "nom": "Grafik dizayn",
        "davomiylik": "4 oy",
        "narx": "750 000 so'm/oy",
    },
}


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Assalomu alaykum! 👋\n"
        "O'quv markazimiz botiga xush kelibsiz!",
        reply_markup=asosiy_menyu(),
    )


@dp.message(F.text == "📚 Kurslar")
async def kurslar(message: Message):
    await message.answer(
        "📚 Kurslardan birini tanlang:",
        reply_markup=kurslar_tugmasi(),
    )


@dp.callback_query(
    StateFilter(None),
    F.data.in_(KURSLAR.keys()),
)
async def kurs_haqida(callback: CallbackQuery):
    kurs = KURSLAR[callback.data]

    await callback.message.answer(
        f"📘 Kurs: {kurs['nom']}\n"
        f"⏳ Davomiyligi: {kurs['davomiylik']}\n"
        f"💰 Narxi: {kurs['narx']}"
    )
    await callback.answer()


@dp.message(F.text == "📝 Kursga yozilish")
async def yozilish(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(RoyxatdanOtish.ism)

    await message.answer(
        "Ism va familiyangizni kiriting:",
        reply_markup=bekor_tugmasi(),
    )


@dp.message(RoyxatdanOtish.ism, F.text)
async def ism_olish(message: Message, state: FSMContext):
    ism = message.text.strip()

    if len(ism) < 3:
        await message.answer("Ism va familiyangizni to'liq kiriting.")
        return

    await state.update_data(ism=ism)
    await state.set_state(RoyxatdanOtish.telefon)

    await message.answer("Telefon raqamingizni kiriting:")


@dp.message(RoyxatdanOtish.telefon, F.text)
async def telefon_olish(message: Message, state: FSMContext):
    telefon = message.text.strip()

    if len(telefon) < 7:
        await message.answer(
            "Telefon raqami noto'g'ri. Qaytadan kiriting:"
        )
        return

    await state.update_data(telefon=telefon)
    await state.set_state(RoyxatdanOtish.kurs)

    await message.answer(
        "Qaysi kursga yozilmoqchisiz?",
        reply_markup=kurslar_tugmasi(),
    )


@dp.callback_query(
    RoyxatdanOtish.kurs,
    F.data.in_(KURSLAR.keys()),
)
async def kurs_tanlash(
    callback: CallbackQuery,
    state: FSMContext,
):
    kurs = KURSLAR[callback.data]

    await state.update_data(
        kurs_nomi=kurs["nom"],
        kurs_narxi=kurs["narx"],
        kurs_davomiyligi=kurs["davomiylik"],
    )

    await state.set_state(RoyxatdanOtish.tasdiqlash)
    data = await state.get_data()

    await callback.message.answer(
        "📝 Ma'lumotlaringiz:\n\n"
        f"👤 Ism-familiya: {data['ism']}\n"
        f"📞 Telefon: {data['telefon']}\n"
        f"📚 Kurs: {data['kurs_nomi']}\n"
        f"⏳ Davomiyligi: {data['kurs_davomiyligi']}\n"
        f"💰 Narxi: {data['kurs_narxi']}\n\n"
        "Ma'lumotlar to'g'rimi?",
        reply_markup=tasdiqlash_tugmasi(),
    )

    await callback.answer()

@dp.callback_query(
    RoyxatdanOtish.tasdiqlash,
    F.data == "confirm_registration",
)
async def tasdiqlash(
    callback: CallbackQuery,
    state: FSMContext,
):
    data = await state.get_data()

    await callback.message.answer(
        "✅ Kursga yozilish so'rovingiz qabul qilindi!\n\n"
        f"👤 Ism-familiya: {data['ism']}\n"
        f"📞 Telefon: {data['telefon']}\n"
        f"📚 Kurs: {data['kurs_nomi']}\n\n"
        "Tez orada siz bilan bog'lanamiz.",
        reply_markup=asosiy_menyu(),
    )

    await state.clear()
    await callback.answer("Tasdiqlandi!")


@dp.message(
    StateFilter("*"),
    F.text == "❌ Bekor qilish",
)
async def bekor_qilish(
    message: Message,
    state: FSMContext,
):
    await state.clear()

    await message.answer(
        "❌ Kursga yozilish bekor qilindi.",
        reply_markup=asosiy_menyu(),
    )


@dp.callback_query(F.data == "cancel_registration")
async def inline_bekor_qilish(
    callback: CallbackQuery,
    state: FSMContext,
):
    await state.clear()

    await callback.message.answer(
        "❌ Kursga yozilish bekor qilindi.",
        reply_markup=asosiy_menyu(),
    )

    await callback.answer("Bekor qilindi!")


@dp.message(F.text == "ℹ️ Markaz haqida")
async def markaz_haqida(message: Message):
    await message.answer(
        "ℹ️ O'quv markazimiz haqida\n\n"
        "Markazimizda zamonaviy IT kurslari o'qitiladi. "
        "Darslar nazariya va amaliy mashg'ulotlardan iborat."
    )


@dp.message(F.text == "📞 Aloqa")
async def aloqa(message: Message):
    await message.answer(
        "📞 Aloqa ma'lumotlari\n\n"
        "Telefon: +998 XX XXX XX XX\n"
        "Manzil: manzilingizni shu yerga yozing\n"
        "Ish vaqti: Dushanba-Shanba, 09:00-18:00"
    )

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())