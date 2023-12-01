from create_bot import dp
from aiogram.utils import executor
import other


async def startup(_):
    print("Бот вышел в онлайн")


other.register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=startup)
