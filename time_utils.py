# time_utils.py
import pytz
from datetime import datetime, time
import logging
from typing import Optional

TIMEZONE_MAPPING, DEFAULT_TIMEZONE = range(2)

logger = logging.getLogger(__name__)

# Расширенный словарь часовых поясов
RUSSIAN_TIMEZONES = {
    # Центральный федеральный округ (UTC+3)
    'Белгород': 'Europe/Moscow',
    'Брянск': 'Europe/Moscow',
    'Владимир': 'Europe/Moscow',
    'Воронеж': 'Europe/Moscow',
    'Иваново': 'Europe/Moscow',
    'Калуга': 'Europe/Moscow',
    'Кострома': 'Europe/Moscow',
    'Курск': 'Europe/Moscow',
    'Липецк': 'Europe/Moscow',
    'Москва': 'Europe/Moscow',
    'Орел': 'Europe/Moscow',
    'Рязань': 'Europe/Moscow',
    'Смоленск': 'Europe/Moscow',
    'Тамбов': 'Europe/Moscow',
    'Тверь': 'Europe/Moscow',
    'Тула': 'Europe/Moscow',
    'Ярославль': 'Europe/Moscow',
    
    # Северо-Западный федеральный округ
    'Архангельск': 'Europe/Moscow',
    'Вологда': 'Europe/Moscow',
    'Калининград': 'Europe/Kaliningrad',  # UTC+2
    'Карелия': 'Europe/Moscow',
    'Коми': 'Europe/Moscow',
    'Ленинград': 'Europe/Moscow',
    'Мурманск': 'Europe/Moscow',
    'Ненецкий': 'Europe/Moscow',
    'Новгород': 'Europe/Moscow',
    'Псков': 'Europe/Moscow',
    'Санкт-Петербург': 'Europe/Moscow',
    
    # Южный и Северо-Кавказский федеральные округа
    'Адыгея': 'Europe/Moscow',
    'Астрахань': 'Europe/Samara',  # UTC+4
    'Волгоград': 'Europe/Moscow',
    'Дагестан': 'Europe/Moscow',
    'Ингушетия': 'Europe/Moscow',
    'Кабардино-Балкария': 'Europe/Moscow',
    'Калмыкия': 'Europe/Moscow',
    'Карачаево-Черкесия': 'Europe/Moscow',
    'Краснодар': 'Europe/Moscow',
    'Крым': 'Europe/Moscow',
    'Ростов': 'Europe/Moscow',
    'Северная Осетия': 'Europe/Moscow',
    'Ставрополь': 'Europe/Moscow',
    'Чечня': 'Europe/Moscow',
    
    # Приволжский федеральный округ
    'Башкортостан': 'Asia/Yekaterinburg',  # UTC+5
    'Киров': 'Europe/Moscow',
    'Марий Эл': 'Europe/Moscow',
    'Мордовия': 'Europe/Moscow',
    'Нижний Новгород': 'Europe/Moscow',
    'Оренбург': 'Asia/Yekaterinburg',  # UTC+5
    'Пенза': 'Europe/Moscow',
    'Пермь': 'Asia/Yekaterinburg',  # UTC+5
    'Самара': 'Europe/Samara',  # UTC+4
    'Саратов': 'Europe/Samara',  # UTC+4
    'Татарстан': 'Europe/Moscow',
    'Удмуртия': 'Europe/Samara',  # UTC+4
    'Ульяновск': 'Europe/Samara',  # UTC+4
    'Чувашия': 'Europe/Moscow',
    
    # Уральский федеральный округ
    'Курган': 'Asia/Yekaterinburg',  # UTC+5
    'Свердловск': 'Asia/Yekaterinburg',  # UTC+5
    'Тюмень': 'Asia/Yekaterinburg',  # UTC+5
    'Ханты-Мансийск': 'Asia/Yekaterinburg',  # UTC+5
    'Челябинск': 'Asia/Yekaterinburg',  # UTC+5
    'Ямало-Ненецкий': 'Asia/Yekaterinburg',  # UTC+5
    
    # Сибирский федеральный округ
    'Алтай': 'Asia/Krasnoyarsk',  # UTC+7
    'Бурятия': 'Asia/Irkutsk',  # UTC+8
    'Забайкалье': 'Asia/Yakutsk',  # UTC+9
    'Иркутск': 'Asia/Irkutsk',  # UTC+8
    'Кемерово': 'Asia/Krasnoyarsk',  # UTC+7
    'Красноярск': 'Asia/Krasnoyarsk',  # UTC+7
    'Новосибирск': 'Asia/Krasnoyarsk',  # UTC+7
    'Омск': 'Asia/Omsk',  # UTC+6
    'Томск': 'Asia/Krasnoyarsk',  # UTC+7
    'Тыва': 'Asia/Krasnoyarsk',  # UTC+7
    'Хакасия': 'Asia/Krasnoyarsk',  # UTC+7
    
    # Дальневосточный федеральный округ
    'Амурск': 'Asia/Yakutsk',  # UTC+9
    'Еврейская': 'Asia/Vladivostok',  # UTC+10
    'Камчатка': 'Asia/Kamchatka',  # UTC+12
    'Магадан': 'Asia/Magadan',  # UTC+11
    'Приморье': 'Asia/Vladivostok',  # UTC+10
    'Саха': 'Asia/Yakutsk',  # UTC+9
    'Сахалин': 'Asia/Magadan',  # UTC+11
    'Хабаровск': 'Asia/Vladivostok',  # UTC+10
    'Чукотка': 'Asia/Kamchatka'  # UTC+12
}

def get_timezone_for_location(location: str) -> str:
    """Определяем часовой пояс по названию локации с улучшенным поиском"""
    if not location:
        return DEFAULT_TIMEZONE
    
    location = location.strip().lower()
    
    # Поиск полного совпадения
    for loc_name, tz in TIMEZONE_MAPPING.items():
        if loc_name.lower() == location:
            return tz
    
    # Поиск по частичному совпадению
    for loc_name, tz in TIMEZONE_MAPPING.items():
        if location in loc_name.lower() or loc_name.lower() in location:
            return tz
    
    # Поиск по характерным словам
    location_lower = location.lower()
    if 'москв' in location_lower:
        return 'Europe/Moscow'
    elif 'калин' in location_lower:
        return 'Europe/Kaliningrad'
    # ... остальные условия как в вашем коде
    
    return DEFAULT_TIMEZONE

def get_user_timezone(location: str) -> pytz.timezone:
    """Получаем объект часового пояса для локации"""
    timezone_str = get_timezone_for_location(location)
    try:
        return pytz.timezone(timezone_str)
    except pytz.UnknownTimeZoneError:
        logger.warning(f"Unknown timezone: {timezone_str}. Using default timezone.")
        return pytz.timezone(DEFAULT_TIMEZONE)

def ensure_aware(dt: datetime, location: str) -> datetime:
    """Преобразует наивный datetime в осведомленный с правильным часовым поясом"""
    if dt.tzinfo is None:
        tz = get_user_timezone(location)
        return tz.localize(dt)
    return dt

def get_localized_time(location: str, dt: Optional[datetime] = None) -> datetime:
    """Получаем текущее время с учетом часового пояса локации"""
    tz = get_user_timezone(location)
    if dt is None:
        return datetime.now(tz)
    return ensure_aware(dt, location)

def format_local_time(location: str, dt: Optional[datetime] = None, 
                     fmt: str = '%Y-%m-%d %H:%M:%S (%Z)') -> str:
    """Форматируем время с учетом часового пояса"""
    dt_local = get_localized_time(location, dt)
    return dt_local.strftime(fmt)

def get_deadline_time(location: str) -> datetime:
    """Получаем время дедлайна (14:00 по Москве) в локальном времени"""
    moscow_tz = pytz.timezone('Europe/Moscow')
    user_tz = get_user_timezone(location)
    
    # Получаем текущую дату по Москве
    moscow_now = datetime.now(moscow_tz)
    moscow_deadline = moscow_now.replace(hour=14, minute=0, second=0, microsecond=0)
    
    # Конвертируем в часовой пояс пользователя
    return moscow_deadline.astimezone(user_tz)

def check_if_on_time(location: str) -> bool:
    """Проверяем, успел ли пользователь сдать отчет в срок"""
    try:
        user_tz = get_user_timezone(location)
        now = datetime.now(user_tz)
        
        # Дедлайн - пятница 14:00 по Москве
        deadline = get_deadline_time(location)
        
        # Проверяем, что сейчас еще пятница и время до дедлайна
        return now.weekday() == 4 and now < deadline
    except Exception as e:
        logger.error(f"Error in check_if_on_time: {e}")
        return False