
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from button import (
    main_buttons,
    bekor_tugmasi,
    kurslar_buttons,
    tasdiqlash_buttons
)


bot = Bot(token="8921325720:AAHixlerpHsBf2_g0IedaQi2qKPnXMVuMHA")
dp = Dispatcher()


KURSLAR = {
    "course_python": {
        "nom": "Python",
        "davomiylik": "4 oy",
        "narx": "800 000 so'm/oy"
    },
    "course_web": {
        "nom": "Web dasturlash",
        "davomiylik": "6 oy",
        "narx": "1 000 000 so'm/oy"
    },
    "course_frontend": {
        "nom": "Frontend",
        "davomiylik": "5 oy",
        "narx": "900 000 so'm/oy"
    },
    "course_design": {
        "nom": "Grafik dizayn",
        "davomiylik": "4 oy",
        "narx": "750 000 so'm/oy"
    }
}


foydalanuvchilar = {}


@dp.message(Command("start"))
async def start(message: Message):
    foydalanuvchilar.pop(message.from_user.id, None)

    await message.answer(
        f"Assalomu alaykum, {message.from_user.full_name}!\n\n"
        "O'quv markazimiz botiga xush kelibsiz!",
        reply_markup=await main_buttons()
    )


@dp.message(F.text == "📚 Kurslar")
async def kurslar(message: Message):
    await message.answer(
        "📚 Kurslardan birini tanlang:",
        reply_markup=await kurslar_buttons()
    )


@dp.callback_query(F.data.in_(KURSLAR.keys()))
async def kurs_tanlash(callback: CallbackQuery):
    user_id = callback.from_user.id
    kurs = KURSLAR[callback.data]

    if user_id in foydalanuvchilar:
        data = foydalanuvchilar[user_id]

        if data.get("holat") == "kurs":
            data["kurs_nomi"] = kurs["nom"]
            data["kurs_davomiyligi"] = kurs["davomiylik"]
            data["kurs_narxi"] = kurs["narx"]
            data["holat"] = "tasdiqlash"

            await callback.message.answer(
                "📝 Ma'lumotlaringiz:\n\n"
                f"👤 Ism-familiya: {data['ism']}\n"
                f"📞 Telefon: {data['telefon']}\n"
                f"📚 Kurs: {kurs['nom']}\n"
                f"⏳ Davomiyligi: {kurs['davomiylik']}\n"
                f"💰 Narxi: {kurs['narx']}\n\n"
                "Ma'lumotlar to'g'rimi?",
                reply_markup=await tasdiqlash_buttons()
            )

            await callback.answer()
            return

    await callback.message.answer(
        f"📘 Kurs: {kurs['nom']}\n"
        f"⏳ Davomiyligi: {kurs['davomiylik']}\n"
        f"💰 Narxi: {kurs['narx']}"
    )

    await callback.answer()


@dp.message(F.text == "📝 Kursga yozilish")
async def yozilish(message: Message):
    foydalanuvchilar[message.from_user.id] = {
        "holat": "ism"
    }

    await message.answer(
        "Ism va familiyangizni kiriting:",
        reply_markup=await bekor_tugmasi()
    )


@dp.message(F.text == "❌ Bekor qilish")
async def bekor_qilish(message: Message):
    foydalanuvchilar.pop(message.from_user.id, None)

    await message.answer(
        "❌ Amal bekor qilindi.",
        reply_markup=await main_buttons()
    )


@dp.message(F.text)
async def malumot_olish(message: Message):
    user_id = message.from_user.id

    if user_id not in foydalanuvchilar:
        return

    data = foydalanuvchilar[user_id]
    matn = message.text.strip()

    if data["holat"] == "ism":
        if len(matn.split()) < 2:
            await message.answer(
                "Ism va familiyangizni kiriting.\n"
                "Masalan: Ali Valiyev"
            )
            return

        data["ism"] = matn
        data["holat"] = "telefon"

        await message.answer(
            "Telefon raqamingizni kiriting.\n"
            "Masalan: +998901234567"
        )

    elif data["holat"] == "telefon":
        telefon = matn.replace(" ", "").replace("-", "")
        raqam = telefon[1:] if telefon.startswith("+") else telefon

        if not raqam.isdigit() or len(raqam) < 7 or len(raqam) > 15:
            await message.answer(
                "Telefon raqami noto'g'ri.\n"
                "Qaytadan kiriting:"
            )
            return

        data["telefon"] = matn
        data["holat"] = "kurs"

        await message.answer(
            "Qaysi kursga yozilmoqchisiz?",
            reply_markup=await kurslar_buttons()
        )


@dp.callback_query(F.data == "confirm_registration")
async def tasdiqlash(callback: CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in foydalanuvchilar:
        await callback.answer("Ma'lumotlar topilmadi.")
        return

    data = foydalanuvchilar[user_id]

    if data.get("holat") != "tasdiqlash":
        await callback.answer("Avval kursni tanlang.")
        return

    await callback.message.answer(
        "✅ Kursga yozilish so'rovingiz qabul qilindi!\n\n"
        f"👤 Ism-familiya: {data['ism']}\n"
        f"📞 Telefon: {data['telefon']}\n"
        f"📚 Kurs: {data['kurs_nomi']}\n\n"
        "Tez orada siz bilan bog'lanamiz.",
        reply_markup=await main_buttons()
    )

    foydalanuvchilar.pop(user_id, None)
    await callback.answer("Tasdiqlandi!")


@dp.callback_query(F.data == "cancel_registration")
async def inline_bekor_qilish(callback: CallbackQuery):
    foydalanuvchilar.pop(callback.from_user.id, None)

    await callback.message.answer(
        "❌ Kursga yozilish bekor qilindi.",
        reply_markup=await main_buttons()
    )

    await callback.answer("Bekor qilindi!")


@dp.message(F.text == "ℹ️ Markaz haqida")
async def markaz_haqida(message: Message):
    await message.answer(
        "ℹ️ O'QUV MARKAZIMIZ HAQIDA\n\n"
        "🎓 Markazimizga xush kelibsiz!\n\n"
        "Markazimizda zamonaviy kasblarni o'rganish "
        "uchun turli xil kurslar mavjud.\n\n"
        "📚 KURSLARIMIZ:\n"
        "🐍 Python dasturlash\n"
        "🌐 Web dasturlash\n"
        "💻 Frontend\n"
        "🎨 Grafik dizayn\n\n"
        "✨ Maqsadimiz — o'quvchilarga sifatli ta'lim "
        "berish va amaliy ko'nikmalarini rivojlantirish.\n\n"
        "📝 Kursga yozilish uchun asosiy menyudan "
        "tegishli tugmani bosing.",
        reply_markup=await main_buttons()
    )


@dp.message(F.text == "📞 Aloqa")
async def aloqa(message: Message):
    await message.answer(
        "📞 ALOQA MA'LUMOTLARI\n\n"
        "☎️ Telefon: +998 91 234 56 78\n"
        "📍 Manzil: manzilingizni shu yerga yozing\n"
        "🕘 Ish vaqti: Dushanba–Shanba, 09:00–18:00\n\n"
        "Savollaringiz bo'lsa, biz bilan bog'laning.",
        reply_markup=await main_buttons()
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
