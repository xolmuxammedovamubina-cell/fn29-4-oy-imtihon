```

import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery

from buttons import (
     asosiy_menyu,
     kurs_tugmalari,
     bekor_tugmasi,
     tasdiqlash_tugmalari,
)

TOKEN = "8263056378:AAEvwDEumpiaHhVPJoS6b_MeaEMnXGPqL2c"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class KursState(StatesGroup):
     ism = State()
     telefon = State()
     kurs = State()
     tasdiqlash = State()

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
     await state.clear()
     await message.answer(
     "botga xuw kelibsan endi tur yoqal😁",
     reply_markup=await asosiy_menyu(),
     )

@dp.message(F.text == "📚 Kurslar")
async def kurslar(message: Message):
     await message.answer(
     "📚 Bizning kurslarimiz:",
     reply_markup=kurs_tugmalari(),
     )

@dp.callback_query(F.data.in_(["python", "web", "bot"]))
async def kurs_haqida(callback: CallbackQuery):
     kurslar = {
     "python": "🐍 Python",
     "web": "🌐 Web dasturlash",
     "bot": "🤖 Telegram bot",
     }

     await callback.message.answer(
     f" {kurslar[callback.data]} kursini tanladingiz."
     )
     await callback.answer()

@dp.message(F.text == "📝 Kursga yozilish")
async def yozilishni_boshlash(
     message: Message,
     state: FSMContext,
):
     await state.clear()
     await state.set_state(KursState.ism)

     await message.answer(
     "ism familyani kiriting",
     reply_markup=bekor_tugmasi(),
     )

@dp.message(KursState.ism, F.text)
async def ism_olish(message: Message, state: FSMContext):
     ism = message.text.strip()

     if len(ism) < 3:
     await message.answer("ism familyani topliw kiritin")
     return

     await state.update_data(ism=ism)
     await state.set_state(KursState.telefon)

     await message.answer(" tel raqamni kiriting")



@dp.message(KursState.telefon, F.text)
async def telefon_olish(message: Message, state: FSMContext):
     telefon = message.text.strip()
     raqamlar = "".join(x for x in telefon if x.isdigit())

     if len(raqamlar) < 7:
     await message.answer("telefon raqamni toliq kiriting")
     return

     await state.update_data(telefon=telefon)
     await state.set_state(KursState.kurs)

     await message.answer(
     "qaysi kurti kiritasn",
     reply_markup=kurs_tugmalari(),
     )

@dp.callback_query(KursState.kurs, F.data.in_(["python", "web", "bot"]))
async def kurs_tanlash(
     callback: CallbackQuery,
     state: FSMContext,
):
     kurslar = {
     "python": "Python",
     "web": "Web dasturlash",
     "bot": "Telegram bot",
     }

     await state.update_data(kurs=kurslar[callback.data])
     data = await state.get_data()
     await state.set_state(KursState.tasdiqlash)

     await callback.message.answer(
     "📋 malumotlaringiz:\n\n"
     f"👤ism: {data['ism']}\n"
     f"📱 Telefon: {data['telefon']}\n"
     f"🎓 Kurs: {data['kurs']}\n\n"
     "Tasdiqlaysizmi?",
     reply_markup=tasdiqlash_tugmalari(),
     )

     await callback.answer()

@dp.callback_query(
     KursState.tasdiqlash,
     F.data == "tasdiq",
)
async def tasdiqlash(
     callback: CallbackQuery,
     state: FSMContext,
):
     data = await state.get_data()

     await callback.message.answer(
     "✅ Kursga yozilish muvaffaqiyatli!\n\n"
     f"🗿 Ism: {data['ism']}\n"
     f"🖋 telefon: {data['telefon']}\n"
     f"🛎 kurs: {data['kurs']}",
     reply_markup=await asosiy_menyu(),
     )

     await state.clear()
     await callback.answer("tasdiqlndi")

@dp.callback_query(F.data == "bekor")
async def bekor_inline(
     callback: CallbackQuery,
     state: FSMContext,
):
     await state.clear()

     await callback.message.answer(
     "🎃 Jarayon bekor qilindi.",
     reply_markup=await asosiy_menyu(),
     )

     await callback.answer("bekor qilindi!")