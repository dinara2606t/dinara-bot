"""
AI-стилист бренда — Telegram-бот для Динары
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, ContextTypes, filters
)

"BOT_TOKEN   = "8886794256:AAFEZANMN6HAPsY6LqDXaOKYTXDiKJZZxN8"
ADMIN_ID    = 168956595
DINARA_TG   = "https://t.me/photoadventurekazan"
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

(
    Q1_NISHA, Q2_PROMOTE, Q3_PLATFORM,
    Q4_STYLE, Q5_FORMAT, Q6_DEADLINE,
    Q7_CONTACT_LINK, Q7_CONTACT_NAME, Q7_CONTACT_TG
) = range(9)

QUESTIONS = [
    {
        "text": "Шаг 1 из 7 ✦\n\n*Какая у вас ниша?*",
        "opts": [
            "💄 Бьюти / beauty-эксперт",
            "🍽 Ресторан / еда / кофе",
            "👗 Одежда / аксессуары",
            "📦 Маркетплейс / WB / Ozon",
            "🏛 Интерьер / дизайн",
            "🎓 Эксперт / коучинг / инфобиз",
            "✦ Другое",
        ]
    },
    {
        "text": "Шаг 2 из 7 ✦\n\n*Что хотите продвигать?*",
        "opts": [
            "🛍 Товар или продукт",
            "💼 Услугу",
            "🧑 Себя как эксперта",
            "🚀 Запуск / мероприятие",
            "🌐 Бренд / компанию",
        ]
    },
    {
        "text": "Шаг 3 из 7 ✦\n\n*Где нужен визуал?*",
        "opts": [
            "📸 Instagram / TikTok",
            "✈️ Telegram-канал",
            "🌐 Сайт / лендинг",
            "📦 Wildberries / маркетплейс",
            "📣 Реклама / таргет",
            "🗂 Презентация / pitch",
        ]
    },
    {
        "text": "Шаг 4 из 7 ✦\n\n*Какая эстетика вам ближе?*",
        "opts": [
            "⬜ Минимализм / clean",
            "✨ Премиум / люкс",
            "👠 Fashion / editorial",
            "🌸 Clean beauty / нежность",
            "🎨 Яркий креатив",
            "🎬 Cinematic / кино",
        ]
    },
    {
        "text": "Шаг 5 из 7 ✦\n\n*Что нужно на выходе?*",
        "opts": [
            "🖼 Фото / нейроизображения",
            "🎬 Видео / reels",
            "📐 Баннеры / карточки",
            "🎯 Всё вместе — пакет",
            "🤔 Пока не знаю",
        ]
    },
    {
        "text": "Шаг 6 из 7 ✦\n\n*Когда нужен результат?*",
        "opts": [
            "⚡ Срочно — прямо сейчас",
            "📅 На этой неделе",
            "🗓 В течение месяца",
            "💭 Просто хочу понять стоимость",
        ]
    },
]

NISHA_IDEAS = {
    "💄 Бьюти / beauty-эксперт": [
        "Макросъёмка пигмента на премиальном фоне",
        "AI-видео с эффектом сияния кожи и деталями процедуры",
        "Баннер «до/после» в clean beauty стиле с мягким светом",
    ],
    "🍽 Ресторан / еда / кофе": [
        "Атмосферная предметка блюда с паром и живым светом",
        "AI-видео с укрупнением текстуры — «кадр из ресторана»",
        "Серия Stories-баннеров в тёплой палитре для меню",
    ],
    "👗 Одежда / аксессуары": [
        "Fashion-лук в мягком студийном свете с нейромоделью",
        "Flat-lay образов с фирменным акцентом бренда",
        "AI Reels — «примерка» в разных локациях за 10 секунд",
    ],
    "📦 Маркетплейс / WB / Ozon": [
        "Белый фон + тень — чистая карточка WB в два клика",
        "Lifestyle-фото товара в сцене использования",
        "Инфографика-баннер с главными преимуществами",
    ],
    "🏛 Интерьер / дизайн": [
        "Архитектурная нейрофотография интерьера в golden hour",
        "Moodboard проекта для презентации клиенту",
        "AI-видео — 3D-тур по пространству за 15 секунд",
    ],
    "🎓 Эксперт / коучинг / инфобиз": [
        "Профессиональный нейропортрет в нейтральной локации",
        "Карусель «экспертность» — цитата + лицо + результат",
        "AI Reels — «один день эксперта» в кинематографичном стиле",
    ],
    "✦ Другое": [
        "Нейрофото продукта с персонализированной атмосферой",
        "Видеоролик с динамикой и музыкой под ваш бренд",
        "Полный визуальный пакет под любую площадку",
    ],
}

PACKAGES = {
    "🖼 Фото / нейроизображения": {
        "name": "AI Нейрофото пакет",
        "items": ["10 нейроизображений в едином стиле", "Адаптация под форматы ленты и Stories", "Визуальная концепция под бренд", "Срок — от 2–3 дней"],
        "note": "Идеально для обновления профиля и рекламы без съёмки."
    },
    "🎬 Видео / reels": {
        "name": "AI Reels пакет",
        "items": ["3 коротких видео (7–15 сек) под Reels/TikTok", "Монтаж с музыкой и текстом", "Адаптация под Stories и рекламу", "Срок — от 3–5 дней"],
        "note": "Максимальный охват в Instagram и TikTok без съёмочного дня."
    },
    "📐 Баннеры / карточки": {
        "name": "AI Баннеры и карточки",
        "items": ["8 карточек товара на белом / lifestyle фоне", "5 баннеров для рекламы и витрины", "Инфографика с преимуществами", "Срок — от 2 дней"],
        "note": "Чистый, конвертирующий визуал для маркетплейсов и таргета."
    },
    "🎯 Всё вместе — пакет": {
        "name": "AI Визуальный пакет для бренда",
        "items": ["5 нейроизображений для ленты", "3 сторис-баннера", "1 короткий reels 7–10 сек", "Визуальная концепция под стиль бренда"],
        "note": "Всё, что нужно для сильного запуска или обновления бренда."
    },
    "🤔 Пока не знаю": {
        "name": "AI Диагностика + подбор пакета",
        "items": ["Разбор вашей ниши и задачи", "Мудборд в вашем стиле", "Рекомендация форматов под бюджет", "Бесплатная консультация с Динарой"],
        "note": "Не знаете что нужно — это нормально. Динара разберётся и предложит лучший вариант."
    },
}

DEFAULT_PACKAGE = PACKAGES["🎯 Всё вместе — пакет"]

def make_keyboard(options):
    buttons = [[InlineKeyboardButton(opt, callback_data=opt)] for opt in options]
    return InlineKeyboardMarkup(buttons)

def user_summary(data):
    lines = [
        f"*Ниша:* {data.get('q1', '—')}",
        f"*Продвигает:* {data.get('q2', '—')}",
        f"*Площадка:* {data.get('q3', '—')}",
        f"*Стиль:* {data.get('q4', '—')}",
        f"*Формат:* {data.get('q5', '—')}",
        f"*Срок:* {data.get('q6', '—')}",
        f"*Профиль:* {data.get('link', 'не указан')}",
        f"*Имя:* {data.get('name', '—')}",
        f"*Контакт:* {data.get('contact', '—')}",
    ]
    return "\n".join(lines)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✦ Подобрать визуал", callback_data="start_quiz")],
        [InlineKeyboardButton("Посмотреть услуги", callback_data="services")],
        [InlineKeyboardButton("Связаться с Динарой", url=DINARA_TG)],
    ])
    await update.message.reply_text(
        "Привет! Я *AI-стилист бренда* от Динары 👋\n\n"
        "За 2 минуты помогу понять, какой визуал нужен вашему проекту:\n"
        "нейрофото, предметка, reels, баннеры или визуальный пакет.\n\n"
        "Начнём?",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def show_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✦ Пройти диагностику", callback_data="start_quiz")],
        [InlineKeyboardButton("Написать Динаре", url=DINARA_TG)],
    ])
    await query.edit_message_text(
        "✦ *Что делает Динара*\n\n"
        "🖼 *Нейрофото для бренда*\n"
        "До 10 изображений в едином стиле — лица, предметы, атмосфера. Срок от 2 дней.\n\n"
        "📦 *Предметная съёмка AI*\n"
        "Товарные карточки для WB, Ozon, витрины — любой фон и сцена.\n\n"
        "🎬 *AI Reels + баннеры*\n"
        "Короткие видео 7–15 сек + Stories и баннеры под рекламу.\n\n"
        "🎯 *Полный визуальный пакет*\n"
        "Фото + видео + концепция — всё для сильного запуска или обновления бренда.",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        QUESTIONS[0]["text"],
        parse_mode="Markdown",
        reply_markup=make_keyboard(QUESTIONS[0]["opts"])
    )
    return Q1_NISHA

async def q1_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    nisha = query.data
    context.user_data["q1"] = nisha
    ideas = NISHA_IDEAS.get(nisha, NISHA_IDEAS["✦ Другое"])
    ideas_text = "\n".join(f"— {i}" for i in ideas)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Хочу такой визуал →", callback_data="continue_q2")]
    ])
    await query.edit_message_text(
        f"✦ Для вашей ниши подойдут:\n\n"
        f"*{nisha}*\n\n"
        f"{ideas_text}\n\n"
        f"Продолжим диагностику?",
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    return Q2_PROMOTE

async def q2_show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        QUESTIONS[1]["text"],
        parse_mode="Markdown",
        reply_markup=make_keyboard(QUESTIONS[1]["opts"])
    )
    return Q2_PROMOTE

async def q2_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["q2"] = query.data
    await query.edit_message_text(
        QUESTIONS[2]["text"],
        parse_mode="Markdown",
        reply_markup=make_keyboard(QUESTIONS[2]["opts"])
    )
    return Q3_PLATFORM

async def q3_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["q3"] = query.data
    await query.edit_message_text(
        QUESTIONS[3]["text"],
        parse_mode="Markdown",
        reply_markup=make_keyboard(QUESTIONS[3]["opts"])
    )
    return Q4_STYLE

async def q4_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["q4"] = query.data
    await query.edit_message_text(
        QUESTIONS[4]["text"],
        parse_mode="Markdown",
        reply_markup=make_keyboard(QUESTIONS[4]["opts"])
    )
    return Q5_FORMAT

async def q5_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["q5"] = query.data
    await query.edit_message_text(
        QUESTIONS[5]["text"],
        parse_mode="Markdown",
        reply_markup=make_keyboard(QUESTIONS[5]["opts"])
    )
    return Q6_DEADLINE

async def q6_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["q6"] = query.data
    await query.edit_message_text(
        "Шаг 7 из 7 ✦\n\n"
        "*Оставьте ссылку на профиль или сайт*\n\n"
        "Если есть — пришлите. Если нет — напишите «нет»",
        parse_mode="Markdown"
    )
    return Q7_CONTACT_LINK

async def q7_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["link"] = update.message.text.strip()
    await update.message.reply_text("Как вас зовут? 👤")
    return Q7_CONTACT_NAME

async def q7_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text.strip()
    await update.message.reply_text("И последнее — ваш Telegram @username или номер телефона 📲")
    return Q7_CONTACT_TG

async def q7_tg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contact"] = update.message.text.strip()
    await show_result(update, context)
    return ConversationHandler.END

async def show_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = context.user_data
    name = data.get("name", "")
    format_ans = data.get("q5", "")
    pkg = PACKAGES.get(format_ans, DEFAULT_PACKAGE)
    items_text = "\n".join(f"— {i}" for i in pkg["items"])
    result_text = (
        f"✦ *По вашим ответам — пакет подобран*\n\n"
        f"Ниша: {data.get('q1', '—')} · Стиль: {data.get('q4', '—')}\n\n"
        f"📦 *{pkg['name']}*\n\n"
        f"{items_text}\n\n"
        f"_{pkg['note']}_\n\n"
        f"{'Рада помочь, ' + name + '!' if name else 'Давайте обсудим!'} "
        f"Динара разберёт вашу задачу и пришлёт пример визуала под ваш бренд."
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✦ Написать Динаре", url=DINARA_TG)],
        [InlineKeyboardButton("Получить пример пакета", url=DINARA_TG)],
        [InlineKeyboardButton("Узнать стоимость", url=DINARA_TG)],
    ])
    await update.message.reply_text(result_text, parse_mode="Markdown", reply_markup=keyboard)
    await notify_admin(update, context)

async def notify_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = context.user_data
    tg_user = update.message.from_user
    tg_link = f"@{tg_user.username}" if tg_user.username else f"id:{tg_user.id}"
    admin_text = (
        f"🔔 *Новая заявка из бота!*\n\n"
        f"{user_summary(data)}\n\n"
        f"*Telegram:* {tg_link}"
    )
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="Markdown")
    except Exception as e:
        logger.warning(f"Ошибка уведомления: {e}")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Диагностика прервана. Напишите /start чтобы начать заново.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_quiz, pattern="^start_quiz$")],
        states={
            Q1_NISHA:        [CallbackQueryHandler(q1_answer)],
            Q2_PROMOTE:      [
                CallbackQueryHandler(q2_show, pattern="^continue_q2$"),
                CallbackQueryHandler(q2_answer),
            ],
            Q3_PLATFORM:     [CallbackQueryHandler(q3_answer)],
            Q4_STYLE:        [CallbackQueryHandler(q4_answer)],
            Q5_FORMAT:       [CallbackQueryHandler(q5_answer)],
            Q6_DEADLINE:     [CallbackQueryHandler(q6_answer)],
            Q7_CONTACT_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, q7_link)],
            Q7_CONTACT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, q7_name)],
            Q7_CONTACT_TG:   [MessageHandler(filters.TEXT & ~filters.COMMAND, q7_tg)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_user=True,
        per_chat=True,
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(show_services, pattern="^services$"))
    app.add_handler(conv)
    logger.info("Бот запущен ✦")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
