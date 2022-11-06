import csv
import vk_api
from random import randint
from tqdm import tqdm
from datetime import date, datetime

vk_session = vk_api.VkApi(token="")


def get_profile_info(user_id):
    users_info = vk_session.method('users.get', {"user_ids": user_id, "fields": "bdate, counters, status, relation"})

    return users_info


def get_name(user_info):
    return f"{user_info['first_name']} {user_info['last_name']}"


def get_age(user_info):
    try:
        b_data = datetime.strptime(user_info['bdate'], '%d.%m.%Y')
        current_year = date.today()
        age = current_year.year - b_data.year

        return age

    except:
        return None


def get_status(user_info):
    return user_info['status']


def get_group(user_id):
    groups_info = vk_session.method('groups.get', {"user_id": user_id, 'extended': 1})['items']
    groups_name = [elem['name'] for elem in groups_info]
    groups_link = [f"https://vk.com/{elem['screen_name']}" for elem in groups_info]

    return groups_name, groups_link


def get_friends_count(user_info):
    return user_info['counters']['friends']


def get_followers_count(user_info):
    return user_info['counters']['followers']


def get_average_likes(user_id):
    posts = vk_session.method('wall.get', {"owner_id": user_id})
    posts_count = posts['count']
    likes_count = sum([elem['likes']['count'] for elem in posts['items']])
    average_likes = round(likes_count/posts_count)

    return average_likes


def get_relation(user_info):
    relation_num = user_info['relation']
    relation = ''
    if relation_num == 0:
        relation = 'не указано'
    elif relation_num == 1:
        relation = 'не женат/не замужем'
    elif relation_num == 2:
        relation = 'есть друг/есть подруга'
    elif relation_num == 3:
        relation = 'помолвлен/помолвлена'
    elif relation_num == 4:
        relation = 'женат/замужем'
    elif relation_num == 5:
        relation = 'всё сложно'
    elif relation_num == 6:
        relation = 'в активном поиске'
    elif relation_num == 7:
        relation = 'влюблён/влюблена'
    elif relation_num == 8:
        relation = 'в гражданском браке'

    return relation


file_writer = csv.writer(open('data.csv', 'w', encoding='UTF-8'), delimiter = ";")

counter = 0
while counter < 2:
    try:
        info = get_profile_info(randint(100000000, 999999999))[0]
        new_user_data = [info['id'],
                         get_name(info),
                         get_age(info),
                         get_status(info),
                         get_group(info['id']),
                         get_friends_count(info),
                         get_followers_count(info),
                         get_average_likes(info['id']),
                         get_relation(info)]
        print(new_user_data)
        file_writer.writerow(new_user_data)
        counter +=1

    except:
        pass
