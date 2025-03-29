import asyncio
from fastapi import APIRouter, Depends, status, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from telethon.errors import SessionPasswordNeededError
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends, HTTPException
from telethon import TelegramClient
from telethon.types import User

from app.core import logger
from app.core.config import get_session_path
from .schemas import PhoneRequest, CodeRequest, PasswordRequest

router = APIRouter(tags=["Liker"])

# Очередь задач для работы с Telethon
loop = asyncio.get_event_loop()
lock = asyncio.Lock()

# Хранение данных авторизации
auth_sessions = {}


async def get_client(phone: str, api_id: str, api_hash: str) -> TelegramClient:
    """Создает или возвращает существующий клиент Telethon для пользователя"""
    session_path = get_session_path(phone)
    logger.info(f"Path session name tg dir: {session_path}")
    async with lock:
        if phone in auth_sessions and "client" in auth_sessions[phone]:
            client: TelegramClient = auth_sessions[phone]["client"]
            if not client.is_connected():
                logger.info(f"Повторное подключение клиента для номера {phone}")
                await client.connect()
            logger.debug(f"Возвращен существующий клиент для номера {phone}")
            return client

        logger.info(f"Создание нового клиента для номера {phone}")
        client = TelegramClient(session_path, api_id, api_hash)
        try:
            await client.connect()
            logger.debug(f"Клиент успешно создан и подключен для номера {phone}")
        except Exception as e:
            logger.error(f"Ошибка при создании клиента для номера {phone}: {e}")
            raise
        return client


@router.post("/send_code")
async def send_code(request: PhoneRequest):
    """Отправляет код подтверждения на телефон"""
    phone = request.phone
    api_id = request.api_id
    api_hash = request.api_hash

    logger.info(f"Получен запрос на отправку кода для номера {phone}")

    try:
        client = await get_client(phone, api_id, api_hash)

        if await client.is_user_authorized():
            logger.info(f"Пользователь с номером {phone} уже авторизован")
            return {"message": "Уже авторизован"}
        logger.debug(f"Отправка кода подтверждения для номера {phone}")
        sent = await client.send_code_request(phone)
        auth_sessions[phone] = {
            "client": client,
            "phone_code_hash": sent.phone_code_hash,
        }
        logger.info(f"Код успешно отправлен для номера {phone}")
        return {"message": "Код отправлен", "phone_code_hash": sent.phone_code_hash}
    except Exception as e:
        logger.error(f"Ошибка при отправке кода для номера {phone}: {e}")
        return {"error": "Произошла ошибка при отправке кода"}


@router.post("/verify_code")
async def verify_code(request: CodeRequest):
    """Проверяет введенный код и завершает авторизацию"""
    phone = request.phone
    code = request.code

    if phone not in auth_sessions:
        raise HTTPException(status_code=400, detail="Сначала запросите код")

    client: TelegramClient = auth_sessions[phone]["client"]
    phone_code_hash = auth_sessions[phone]["phone_code_hash"]

    try:
        login = await client.sign_in(phone, code, phone_code_hash=phone_code_hash)
        del auth_sessions[phone]  # Очищаем сессию
        logger.info(f"Check del session {auth_sessions}")
        return {"message": "Успешная авторизация"}

    except SessionPasswordNeededError:
        auth_sessions[phone]["needs_2fa"] = True
        return {"message": "Требуется облачный пароль (2FA)", "needs_2fa": True}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/verify_password")
async def verify_password(request: PasswordRequest):
    """Проверяет пароль 2FA и завершает авторизацию"""
    phone = request.phone
    password = request.password

    if phone not in auth_sessions or not auth_sessions[phone].get("needs_2fa"):
        raise HTTPException(
            status_code=400,
            detail="2FA не требуется или нет активной сессии",
        )

    client: TelegramClient = auth_sessions[phone]["client"]

    try:
        login_user: User = await client.sign_in(password=password)
        logger.info(f"Login User {login_user.first_name}")
        logger.info(f"Login User {login_user.last_name}")
        logger.info(f"Login User {login_user.username}")
        del auth_sessions[phone]  # Очищаем сессию
        logger.info(f"Check auth_sessions{auth_sessions}")
        return {"message": "Успешная авторизация"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# @router.get("/status")
# async def auth_status(phone: str, api_id: str, api_hash: str):
#     """Проверяет статус авторизации"""
#     client = await get_client(phone, api_id, api_hash)
#     is_auth = await client.is_user_authorized()
#     return {"authorized": is_auth}


# @router.post("/logout")
# async def logout(phone: str, api_id: str, api_hash: str):
#     """Выход из аккаунта Telegram"""
#     client = await get_client(phone, api_id, api_hash)
#     await client.log_out()
#     return {"message": "Вы вышли из Telegram"}


# async def update_user_tg(db: AsyncSession, user):
#     user_phone = f"+{user.phone}"

#     try:
#         # Ищем пользователя по телефону
#         result = await db.execute(
#             select(TgAuthAccount).where(TgAuthAccount.phone == user_phone)
#         )
#         account = result.scalars().first()  # Получаем список объектов

#         if not account:
#             print(f"Пользователь с номером {user_phone} не найден в БД.")
#             return None

#         # Обновляем данные найденных пользователей

#         account.user_tg_id = str(user.id)
#         account.first_name = user.first_name
#         account.last_name = user.last_name if user.last_name else None
#         account.username = user.username if user.username else None

#         # Сохраняем изменения
#         await db.commit()
#         print(f"Обновлен Telegram-аккаунт для номера {user_phone}.")
#         return True

#     except SQLAlchemyError as e:
#         print(f"Ошибка БД при обновлении Tg-аккаунтов для {user_phone}: {str(e)}")
#         return None
#     except Exception as e:
#         print(
#             f"Неизвестная ошибка при обновлении Tg-аккаунтов для {user_phone}: {str(e)}"
#         )
#         return None
