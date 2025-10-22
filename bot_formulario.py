# bot.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ConversationHandler, filters, ContextTypes
)

# Estados de la conversación
NOMBRE, EDAD, EMAIL = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📝 Comenzar formulario", callback_data='formulario')],
        [InlineKeyboardButton("ℹ️ Ver ejemplo", callback_data='ejemplo')],
        [InlineKeyboardButton("❓ Ayuda", callback_data='ayuda')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 ¡Hola! Soy tu asistente automático.\n"
        "Te ayudaré a completar un formulario con solo responder unas preguntas.",
        reply_markup=reply_markup
    )

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "formulario":
        await query.message.reply_text("📝 Empecemos. ¿Cuál es tu nombre?")
        return NOMBRE
    elif query.data == "ejemplo":
        await query.message.reply_text(
            "📄 Ejemplo:\n\nNombre: Juan Pérez\nEdad: 30\nEmail: juan@mail.com"
        )
    elif query.data == "ayuda":
        await query.message.reply_text(
            "💡 Este bot te hace unas preguntas y genera un formulario automáticamente.\n"
            "Solo debes seguir las instrucciones."
        )
    return ConversationHandler.END

async def nombre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['nombre'] = update.message.text
    await update.message.reply_text("Perfecto, ¿cuántos años tienes?")
    return EDAD

async def edad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['edad'] = update.message.text
    await update.message.reply_text("Genial, ¿cuál es tu correo electrónico?")
    return EMAIL

async def email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['email'] = update.message.text
    resumen = (
        f"📋 **Resumen del formulario:**\n\n"
        f"👤 Nombre: {context.user_data['nombre']}\n"
        f"🎂 Edad: {context.user_data['edad']}\n"
        f"📧 Email: {context.user_data['email']}\n\n"
        f"¿Deseas confirmar el envío?"
    )
    keyboard = [
        [InlineKeyboardButton("✅ Confirmar", callback_data='confirmar')],
        [InlineKeyboardButton("✏️ Editar", callback_data='editar')]
    ]
    await update.message.reply_text(
        resumen,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return ConversationHandler.END

# --- Configuración del bot ---
TOKEN = "7396827151:AAHvXooe60JdjM9uVNgPsPYRURnu11lx97g"  # tu token
app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(menu_callback, pattern='formulario')],
    states={
        NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, nombre)],
        EDAD: [MessageHandler(filters.TEXT & ~filters.COMMAND, edad)],
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
    },
    fallbacks=[],
)

app.add_handler(CommandHandler("start", start))
app.add_handler(conv_handler)
app.add_handler(CallbackQueryHandler(menu_callback))

print("🤖 Bot en marcha...")

# Ejecutar polling (Background Worker en Render)
app.run_polling()
