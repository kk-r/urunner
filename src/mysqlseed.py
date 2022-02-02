#!/usr/bin/env python3.6
import os
import random
import time
from tokenize import String
from typing import List

import mysql.connector, json
from faker import Faker
from mysql.connector import InterfaceError
from core.security import get_password_hash
import inspect

POSSIBLE_ROLES = []
faker = Faker('en')


class MySqlSeeder:

    def __init__(self):
        config = {
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', 'root'),
            'host': os.getenv('MYSQL_SERVER', '127.0.0.1'),
            'port': os.getenv('MYSQL_PORT', '3306'),
            'database': os.getenv('MYSQL_DB', 'test_db')
        }
        while not hasattr(self, 'connection'):
            try:
                print(config)
                self.connection = mysql.connector.connect(**config)
                self.cursor = self.connection.cursor()
            except InterfaceError:
                print("MySQL Container has not started yet. Sleep and retry...")
                time.sleep(1)

    def seed(self):
        print("Clearing old data...")
        self.truncate_user_jogging_table()
        self.truncate_users_table()
        print("Get avialable Roles")
        self.get_available_role_ids()
        print("Start seeding...")
        user_ids = self.insert_users()
        print("inserted user_ids", user_ids)
        print("insert jogging data..")
        self.insert_jogging_data(user_ids)
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        print("Done")

    def get_available_role_ids(self):
        self.POSSIBLE_ROLES = [1, 2, 3]
        
    def truncate_user_jogging_table(self):
        self.cursor.execute('truncate TABLE user_jogging_data;')
        
    def truncate_users_table(self):
        self.cursor.execute('truncate TABLE users;')

    def insert_users(self):
        user_ids = []
        for _ in range(25):
            sql = '''
            INSERT INTO users (username, email, password, role_id)
            VALUES (%(username)s, %(email)s, %(password)s, %(role_id)s);
            '''
            username = faker.user_name()
            role_id = random.choice(self.POSSIBLE_ROLES)
            user_email = faker.email()
            user_data = {
                'username': username,
                'role_id': role_id,
                'email': user_email,
                'password': get_password_hash("password")
            }
            print('User Created. username - {} | email - {} | password - {} | role_id - {}'.format(username, user_email, "password", role_id))
            self.cursor.execute(sql, user_data)
            user_ids.append(self.cursor.lastrowid)
        return user_ids

    def insert_jogging_data(self, user_ids = []):
        if not user_ids:
            print("user_ids are empty")
            return
        for _ in range(200):
            sql = '''
            INSERT INTO user_jogging_data (user_id, date, distance, location, time, weather_condition)
            VALUES (%(user_id)s, %(date)s, %(distance)s, %(location)s, %(time)s, %(weather_condition)s);
            '''
        
            jogging_data = {
                'date': faker.date(),
                'user_id': random.choice(user_ids),
                'distance': faker.pyint(),
                'location': faker.city(),
                'time': faker.time(),
                'weather_condition': '{"id": 500, "main": "Rain", "description": "light rain", "icon": "10n"}',
            }
            
            self.cursor.execute(sql, jogging_data)


def script_runs_within_container():
    with open('/proc/1/cgroup', 'r') as cgroup_file:
        return 'docker' in cgroup_file.read()


MySqlSeeder().seed()