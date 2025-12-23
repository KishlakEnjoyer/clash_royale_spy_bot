import random
import storage as st
from aiogram.types import FSInputFile
import os
import string


def choice_mode():
    """
    Функция которая рандомно выбирает режим игры
    """
    cur_mode = random.choice(list(st.GAME_MODES))
    cur_mode_name = st.GAME_MODES[cur_mode]
    print(cur_mode_name)
    return [cur_mode, cur_mode_name]


def select_card():
    """
    Выбирает случайную карту из доступных и возвращает её фото и название
    """
    if not st.CARD_FILES:
        return None, None
    
    card_file = random.choice(st.CARD_FILES)
    card_name = card_file.replace('.webp', '')
    photo_path = os.path.join(st.IMAGE_DIR, card_file)
    card_photo = FSInputFile(photo_path)

    return card_photo, card_name

def generate_unique_code():
    """
    Генерация именно уникального кода
    """
    while True:
        code = ''.join(random.choices(string.digits, k=6))
        if code not in st.ACTIVE_ROOMS:
            return code

def generate_room_code(user_id: int):
    """
    Генерация кода для комнаты
    """
    if user_id in st.USER_ROOMS:
        return '❌ Вы уже в комнате!'
    
    room_code = generate_unique_code()
    new_room = {
        'host_id': user_id,
        'players': [user_id],
        'status': 'waiting',
        'round': 0
    }
    st.ACTIVE_ROOMS[room_code] = new_room
    st.USER_ROOMS[user_id] = room_code 
    print(st.ACTIVE_ROOMS)
    return room_code

def game_round(users: list[int]):
    """
    Основная логика вообще, главная функция логики
    Возвращает словарь user_id: {"role":"Spy", "card": "Princess", "photo": "FSInputFile"}
    """
    mode = choice_mode()[1]
    result = {}
    match(mode):
        case "Один шпион":
            spy_id = random.choice(users)
            photo, name = select_card()
            for i in users:
                if(spy_id == i):
                    result[i] = { "role": "Spy", "card": None, "photo": None }
                    continue
                result[i] = { "role": "NoSpy", "card": name, "photo": photo }
            return result
        
        case "Все — шпионы":
            for i in users:
                result[i] = { "role": "Spy", "card": None, "photo": None }                
            return result
        
        case "Один невиновный":
            nospy_id = random.choice(users)
            photo, name = select_card()
            for i in users:
                if(nospy_id == i):
                    result[i] = { "role": "NoSpy", "card": name, "photo": photo }
                    continue
                result[i] = { "role": "Spy", "card": None, "photo": None }
            return result

        case "У всех разные карты":
            for i in users:
                photo, name = select_card()
                result[i] = { "role": "NoSpy", "card": name, "photo": photo }
            return result
            

        case "Никто не шпион":
            photo, name = select_card()
            for i in users:
                result[i] = { "role": "NoSpy", "card": name, "photo": photo }
            return result

        


    







