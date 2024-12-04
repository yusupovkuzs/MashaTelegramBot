import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import grpc
import chat_pb2
import chat_pb2_grpc

# Замените на ваш токен
API_TOKEN = '5685627676:AAHanunrlGEviVMpaBolDhyseL0cfbkLR98'

# Адрес gRPC сервера
GRPC_SERVER_ADDRESS = 'http://107.173.25.219:50051'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Создание gRPC канала и клиента
channel = grpc.aio.insecure_channel(GRPC_SERVER_ADDRESS)
stub = chat_pb2_grpc.ChatServiceStub(channel)


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, использующий gRPC для обработки запросов. Отправь мне сообщение.")


@dp.message()
async def process_message(message: types.Message):
    try:
        # Отправка запроса через gRPC
        request = chat_pb2.ChatRequest(message=message.text)
        response = await stub.GetResponse(request)

        # Отправка ответа пользователю
        await message.reply(response.message)
    except grpc.RpcError as e:
        await message.reply("Извините, произошла ошибка при обработке вашего запроса.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())