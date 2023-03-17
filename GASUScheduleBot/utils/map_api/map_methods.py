import json
import requests
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo #test web app


async def get_path_classes(schedule):
    response1 = requests.get("https://map.spbgasu.ru/locations.json")
    response2 = requests.get("https://map.spbgasu.ru/map2/locations.json")
    response3 = requests.get("https://map.spbgasu.ru/map3/locations.json")
    response4 = requests.get("https://map.spbgasu.ru/map4/locations.json")
    response1.encoding = 'utf-8-sig'
    response2.encoding = 'utf-8-sig'
    response3.encoding = 'utf-8-sig'
    response4.encoding = 'utf-8-sig'

    empty_lecture_aliases = ["Нет занятий.", None]
    all_class = []
    is_day_off = True
    if schedule.first_lecture not in empty_lecture_aliases:
        for i, c in enumerate(schedule.first_lecture):
            if c.isdigit():
                dump = schedule.first_lecture[i:len(schedule.first_lecture)]
                all_class.append(dump)
                break
        is_day_off = False
    if schedule.second_lecture not in empty_lecture_aliases:
        for i, c in enumerate(schedule.second_lecture):
            if c.isdigit():
                dump = schedule.second_lecture[i:len(schedule.second_lecture)]
                all_class.append(dump)
                break
        is_day_off = False
    if schedule.third_lecture not in empty_lecture_aliases:
        for i, c in enumerate(schedule.third_lecture):
            if c.isdigit():
                dump = schedule.third_lecture[i:len(schedule.third_lecture)]
                all_class.append(dump)
                break
        is_day_off = False
    if schedule.fourth_lecture not in empty_lecture_aliases:
        for i, c in enumerate(schedule.fourth_lecture):
            if c.isdigit():
                dump = schedule.fourth_lecture[i:len(schedule.fourth_lecture)]
                all_class.append(dump)
                break
        is_day_off = False
    if schedule.fifth_lecture not in empty_lecture_aliases:
        for i, c in enumerate(schedule.fifth_lecture):
            if c.isdigit():
                dump = schedule.fifth_lecture[i:len(schedule.fifth_lecture)]
                all_class.append(dump)
                break
        is_day_off = False
    if schedule.sixth_lecture not in empty_lecture_aliases:
        for i, c in enumerate(schedule.sixth_lecture):
            if c.isdigit():
                dump = schedule.sixth_lecture[i:len(schedule.sixth_lecture)]
                all_class.append(dump)
                break
        is_day_off = False
    if schedule.seventh_lecture not in empty_lecture_aliases:
        for i, c in enumerate(schedule.sixth_lecture):
            if c.isdigit():
                dump = schedule.sixth_lecture[i:len(schedule.sixth_lecture)]
                all_class.append(dump)
                break
        is_day_off = False
    if (len(all_class) == 0):
        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton(text="Карта СПбГАСУ", web_app=WebAppInfo(url=f"https://map.spbgasu.ru/")))
        return markup
    if (is_day_off):
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Карта СПбГАСУ", web_app=WebAppInfo(url=f"https://map.spbgasu.ru/")))
        return markup

    all_location = []


    location_main = json.loads(response1.text)
    location_egorova = json.loads(response2.text)
    location_kurlyadskaya = json.loads(response3.text)
    location_korpusFive = json.loads(response4.text)

    markup = InlineKeyboardMarkup()

    #Вот тут начинается определение корпуса
    #Да, просто сопоставление

    for clas in all_class:
        for level in location_main['levels']:
            for classes in level['locations']:
                classString = classes['title']
                index = classString.find(clas)
                if classString.find(clas) != -1:
                    if classString[index:len(classString)] != clas:
                        break
                    markup.add(InlineKeyboardButton(clas, web_app=WebAppInfo(url=f"https://map.spbgasu.ru/?location={classes['id']}")))
        for level in location_egorova['levels']:
            for classes in level['locations']:
                classString = classes['title']
                index = classString.find(clas)
                if classString.find(clas) != -1:
                    if classString[index:len(classString)] != clas:
                        break
                    markup.add(InlineKeyboardButton(clas, web_app=WebAppInfo(url=f"https://map.spbgasu.ru/map2/?location={classes['id']}")))
        for level in location_kurlyadskaya['levels']:
            for classes in level['locations']:
                classString = classes['title']
                index = classString.find(clas)
                if classString.find(clas) != -1:
                    if classString[index:len(classString)] != clas:
                        break
                    markup.add(InlineKeyboardButton(clas, web_app=WebAppInfo(url=f"https://map.spbgasu.ru/map3/?location={classes['id']}")))
        for level in location_korpusFive['levels']:
            for classes in level['locations']:
                classString = classes['title']
                index = classString.find(clas)
                if classString.find(clas) != -1:
                    if classString[index:len(classString)] != clas:
                        break
                    markup.add(InlineKeyboardButton(clas, web_app=WebAppInfo(url=f"https://map.spbgasu.ru/map4/?location={classes['id']}")))
    return markup