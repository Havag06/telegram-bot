import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def save_to_google_sheets(user_id: int, username: str, first_name: str):
    """Сохраняет данные пользователя в Google Таблицу"""
    try:
        scope = ['https://www.googleapis.com/auth/spreadsheets']
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        
        spreadsheet = client.open_by_key("1aqtaYNbsnK8_yicmWcXCR25i3iHk5BR1gMo2J05blm4")
        sheet = spreadsheet.sheet1
        
        sheet.append_row([
            str(user_id),
            username or "N/A",
            first_name or "",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])
        return True
        
    except Exception as e:
        logger.error(f"Ошибка Google Sheets: {str(e)}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    try:
        await update.message.reply_text(f"Привет, {user.first_name}! Ваш ID: {user.id}")
        
        if save_to_google_sheets(user.id, user.username, user.first_name):
            logger.info(f"Данные пользователя {user.id} сохранены")
        else:
            logger.warning("Не удалось сохранить данные в Google Sheets")
            
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        await update.message.reply_text("Произошла ошибка. Попробуйте позже.")

def main():
    """Запуск бота"""
    try:
        application = Application.builder().token("8126121798:AAF1Nz3ZqfqrnO2Al5dc9MwECKWdwyOfwpo").build()
        
        application.add_handler(CommandHandler("start", start))
        
        logger.info("Бот запущен")
        application.run_polling()
        
    except Exception as e:
        logger.critical(f"Ошибка при запуске бота: {str(e)}")

if __name__ == '__main__':
    main()