#!/usr/bin/python
# -*- coding: utf-8 -*-

import os 
import shutil 
import urllib 
import re 
import sys

url_feed = "http://www.radio-t.com/atom.xml"
podcast_path = "/home/mak/Музыка/podcasts/"
player_path = "/media/disk/music/podcast/"

def get_list_urls(url):
    """ возвращает список доступных подкастов
    Arguments:
    - `url`: урл rss - ленты
    """
    rss_page = urllib.urlopen(url).read()
    podcast_list_url = re.compile(r'http:\/\/[a-z\-\.]+\.radio-t\.com\/rt_podcast[0-9]+\.mp3').findall(rss_page)
    return podcast_list_url

def download_podcast(url, download_file):
    """ загружается подкаст
    Arguments:
    - `url`: ссылка для скачивания
    """
    def progress_show(count, block_size, size):
        """ показывает прогресс скачивания файа """
        percent = int(count*block_size*100/size)
        sys.stdout.write("\r" + "Идет скачивание скачивание " + download_file + "......%d%%" % percent)
        sys.stdout.flush()
    urllib.urlretrieve(url, download_file, progress_show)
    print '\n'

def download_on_pc(url_feed, podcast_path):
    """ по желанию пользователя загружает нужные подкасты
    """
    print "Доступные для скачивания подкасты: "
    list_urls = list(set(get_list_urls(url_feed)))
    list_urls = sorted(list_urls)
    for i in list_urls:
        print i.split("/")[-1]
    try:
        for_download_string = raw_input("Введите номера подкастов, через запятую: ")
        if for_download_string == '':
            print "Вы не указали подкастов для скачивания!"
        else:
            for_download = for_download_string.split("/")
            for i in list_urls:
                for p in for_download:
                    if (p in i) and os.path.exists(podcast_path):
                        download_podcast(i, podcast_path + i.split("/")[-1])
                        print "Файл сохранен как %s" % podcast_path + i.split("/")[-1]
    except:
        print "Что-то пошло не так"
        
def delete_podcast_on_player(player_path):
    """ с помощью этой функции можно удалить ненужные подкасты на плеере
    
    Arguments:
    - `player_path`: путь до каталога плеера
    """
    if os.path.exists(player_path):
        print "На плеере имеются следующие подкасты: "
        list_podcast = os.listdir(player_path)
        for i in list_podcast: print i
        delete_string = raw_input("Введите через запятую подкасты, что надо удалить: ")
        if delete_string == '':
            print "Вы не указали подкастов для удаления!"
        else:
            delete_list = delete_string.split(",")
            for i in delete_list:
                for p in list_podcast:
                    if i in p:
                        os.remove(player_path + p)
            list_podcast = os.listdir(player_path)             
            print "Оставшиеся подкасты: "
            for i in list_podcast: print i
    else:
        print "Плеер же не подключен, не буду ничего удалять!"

def upload_podcast_on_player(podcast_path, player_path):
    """ копируется выбранные пользователем подкасты на плеер
    podcast_path: - путь до каталога с подкастами на компе
    player_path: - путь до плеера
    """
    if os.path.exists(player_path):
        os.system("df -h")
        list_podcast = os.listdir(podcast_path)
        print "Список подкастов, доступных для копирования: "
        for i in list_podcast: print i
        copy_string = raw_input("Введите через запятую подкасты, что надо скопировать: ")
        if copy_string == '':
            print "Вы не указали подкастов для копирования!"
        else:
            copy_list = copy_string.split(",")
            for i in copy_list:
                for p in list_podcast:
                    if i in p:
                        shutil.copy(podcast_path + p, player_path + p)
                        print "Подкасть %s скопирован на плеер." % p
        print "Список подкастов на плеере сейчас: "
        for i in os.listdir(player_path): print i
    else:
        print "Плеер же не подключен, не буду ничего удалять!"

def user_request():
    """ возвращает выбранный пункт пользователем
    """
    message = """    Приветствую тебя, мой белый господин.
    Пожалуйста, скажите мне, что именно Вы желаете сделать сейчас:
    [1] Скачать подкасты
    [2] Очистить место на плеере
    [3] Загрузить подкасты на плеер
    [0] Выход
    ============================================================="""
    print message
    try:
        answer = int(raw_input("Введите нужный Вам вариант: "))
        return answer
    except:
        print "Что-то я не раслышал, скажите еще раз!"
        print message

def user_dialog(url_feed, player_path, podcast_path):
    """ интерактивная часть программы
    """
    answer = user_request()
    n = True
    while n:
        if answer == 0:
            print "До свидания, мой Повелитель!"
            n = False
        elif answer == 1:
            download_on_pc(url_feed, podcast_path)
            answer = user_request()
        elif answer == 2:
            delete_podcast_on_player(player_path)
            answer = user_request()
        elif answer == 3:
            upload_podcast_on_player(podcast_path, player_path)
            answer = user_request()
        else:
            print "Что-то я не раслышал, скажите еще раз!"
            answer = user_request()

user_dialog(url_feed, player_path, podcast_path)
