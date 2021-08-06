from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from os import urandom

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), unique=False, nullable=True)

    first_name = db.Column(db.String(255), nullable=False)
    middle_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)

    avatar_uri = db.Column(db.String(512), default='empty.jpg', nullable=False)

    contacts = db.Column(db.String(512), nullable=True)

    vk_id = db.Column(db.String(255), nullable=True)
    fb_id = db.Column(db.String(255), nullable=True)
    google_id = db.Column(db.String(255), nullable=True)

    department = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)

    def get_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def __repr__(self):
        return f"{self.last_name}, {self.first_name}, {self.middle_name}"

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), default='', nullable=False)
    logo = db.Column(db.String(255), default='empty.png', nullable=False)

class ThesesThemes(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    title_ru = db.Column(db.String(255), default='', nullable=False)
    description = db.Column(db.String(1024), default='', nullable=True)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'), default=1, nullable=False)

    supervisor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    advisor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    supervis = db.Column(db.String(255), default='', nullable=False)
    depart = db.Column(db.String(255), default='', nullable=True)
    worktype = db.Column(db.String(255), default='', nullable=False)

    requirements = db.Column(db.String(512), nullable=True)


class Level(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), default='', nullable=False)

def init_db():

    users = [
        {'email' : 'ilya@hackerdom.ru', 'last_name' : 'Зеленчук', 'first_name' : 'Илья',
         'avatar_uri' : 'zelenchuk.jpg'}
        ]

    themes = [
        {'worktype': 'Учебная практика', 'supervis': 'Сартасов Станислав Юрьевич', 'depart': 'fafaffa', 'title_ru': 'Изучение журналирования для all flash RAID массива',
         'description': 'Журналирование позволяет решить проблему write-hole и порчу данных в случае сложных отказов системы. В рамках задачи предлагается изучить технологию журналирования в Linux dm-log. Исследование включает в себя функциональные возможности, параметры настройки, производительность при различных паттернах. Интегрирование с нашим RAID engine. Возможна исследование и реализация и различных подходов к журналирования внутри RAID engine а не сторонними средствами, для того чтобы получить более производительное решение.',
         'level_id' : '2', 'supervisor_id' : '1', 'advisor_id' : '1', 'requirements': ''},
        {'worktype': 'Учебная практика', 'supervis': 'Сартасов Станислав Юрьевич', 'depart': 'fafaffa', 'title_ru': 'Оптимизация алгоритма адаптивного объединения запросов в RAID',
         'description': 'При последовательной записи объединение запросов позволят решить проблему read-modify-write на RAID с контрольными суммами. Имеющийся алгоритм зависит от нескольких параметров и есть ряд наработок, которые позволяют автоматически подстраивать параметры в зависимости от нагрузки (размер ио, интенсивность, многопоточность), однако не справляется с некоторыми паттернами. В рамках работы необходимо изучить алгоритм адаптивного объединения, улучшить его или предложить альтернативный. Также предполагает изучения объединения запросов не только на искусственных паттернах.',
         'level_id': '2', 'supervisor_id': '1', 'advisor_id': '1', 'requirements': ''},
        {'worktype': 'Учебная практика', 'supervis': 'Сартасов Станислав Юрьевич', 'depart': 'fafaffa', 'title_ru': 'Изучение RAM кэша для RAID массива',
         'description': 'В рамках работы планируется изучить технологии Open Cache Acceleration Software для реализации RAM cache или кэш на быстрых накопителях для нашего RAID engine. Изучение включает в себя функциональные возможности, параметры и настройку, производительность в различных конфигурациях и паттернах нагрузки. Внедрение технологии, ее улучшение и адаптация под наш RAID. Возможно изучение и сравнение с имеющимися технологиями кеширования в Linux такими как dm-cache, bcache. Возможно также углубление в изучение алгоритмов Read-Ahead.',
         'level_id': '2', 'supervisor_id': '1', 'advisor_id': '1', 'requirements': ''},
        {'worktype': 'Учебная практика', 'supervis': 'Сартасов Станислав Юрьевич', 'depart': 'fafaffa', 'title_ru': 'Оптимизация алгоритма упреждающего чтения в RAID',
         'description': 'Для увеличения производительности при последовательном чтении на жесткие диски можно заранее класть области, которые потребуются. Размер области зависит от скорости потока, от размера RAM- кэша, от самого паттерна рабочей нагрузки. В алгоритме, используемом RAIDIX на данный момент есть 3 параметра, автоматически выбирается только один. В работе предполагается автоматизация оставшихся или реализация другого алгоритма(возможно на основе машинного обучения), который покажет лучшие результаты по производительности.',
         'level_id': '2', 'supervisor_id': '1', 'advisor_id': '1', 'requirements': ''},
        {'worktype': 'Учебная практика', 'supervis': 'Сартасов Станислав Юрьевич', 'depart': 'fafaffa', 'title_ru': 'Исследование и разработка алгоритмов тонкого выделения и снэпшотов для RAID.',
         'description': 'В работе предполагается изучение алгоритмов тонкого выделения и снэпшотов, используемых в различных Open Source решениях, и оптимизация данного решения для RAIDIX RAID.',
         'level_id': '2', 'supervisor_id': '1', 'advisor_id': '1', 'requirements': ''},
        {'worktype': 'Учебная практика', 'supervis': 'Сартасов Станислав Юрьевич', 'depart': 'fafaffa', 'title_ru': 'Navitas Framework',
         'description': 'Платформа для замеров потребления энергии многопоточным кодом в Android. Продолжение технических работ над проектом: 1) cоздание методологии для корректировки энергопрофилей смартфона, 2) добавление новых периферийных устройств в профиль.',
         'level_id': '2', 'supervisor_id': '1', 'advisor_id': '1', 'requirements': 'Минимальный опыт разработки под Андроид, рутованный смартфон'},
        {'worktype': 'Учебная практика', 'supervis': 'Сартасов Станислав Юрьевич', 'depart': 'fafaffa', 'title_ru': 'Изучение журналирования для all flash RAID массива',
         'description': 'Журналирование позволяет решить проблему write-hole и порчу данных в случае сложных отказов системы. В рамках задачи предлагается изучить технологию журналирования в Linux dm-log. Исследование включает в себя функциональные возможности, параметры настройки, производительность при различных паттернах. Интегрирование с нашим RAID engine. Возможна исследование и реализация и различных подходов к журналирования внутри RAID engine а не сторонними средствами, для того чтобы получить более производительное решение.',
         'level_id': '2', 'supervisor_id': '1', 'advisor_id': '1', 'requirements': ''},
        {'worktype': 'Учебная практика', 'supervis': 'Сартасов Станислав Юрьевич', 'depart': 'fafaffa', 'title_ru': 'Оптимизация алгоритма адаптивного объединения запросов в RAID',
         'description': 'При последовательной записи объединение запросов позволят решить проблему read-modify-write на RAID с контрольными суммами. Имеющийся алгоритм зависит от нескольких параметров и есть ряд наработок, которые позволяют автоматически подстраивать параметры в зависимости от нагрузки (размер ио, интенсивность, многопоточность), однако не справляется с некоторыми паттернами. В рамках работы необходимо изучить алгоритм адаптивного объединения, улучшить его или предложить альтернативный. Также предполагает изучения объединения запросов не только на искусственных паттернах.',
         'level_id': '2', 'supervisor_id': '1', 'advisor_id': '1', 'requirements': ''},
        {'worktype': 'Бакалаврская ВКР', 'supervis': 'Сартасов Станислав Юрьевич', 'depart': 'fafaffa', 'title_ru': 'Энергоэффективные рефакторинги',
         'description': 'Зонтичная тема - изучение того, какой код на Android ест меньше электричества при той же функциональности',
         'level_id': '2', 'supervisor_id': '1', 'advisor_id': '1',
         'requirements': 'Минимальный опыт разработки под Андроид, рутованный смартфон'},
        {'worktype': 'Учебная практика', 'supervis': 'Сартасов Станислав Юрьевич', 'depart': 'fafaffa', 'title_ru': 'Android Dynamic Voltage Frequency Scaling',
         'description': 'Оптимизация энергопотребления в Android путём управления частотой ядер процессора и подаваемым на них напряжением в условиях многопоточной нагрузки на процессор. Теория - создание алгоритма изменения частоты и напряжения в зависимости от текущей вычислительной нагрузки, systematic literature review по теме. Практика - написание системного frequency governor, реализующего этот алгоритм.',
         'level_id': '2', 'supervisor_id': '1', 'advisor_id': '1',
         'requirements': 'Опыт разработки под Андроид и C/C++, некоторое знание Linux, рутованный смартфон'},
        ]

    levels = [
        {'title': 'Все'},
        {'title': 'Учебная практика'},
        {'title': 'Бакалаврская ВКР'},
        {'title': 'Магистерская ВКР'},
    ]

    departments = [
        {'title': 'Все'},
        {'title': 'Рэйдикс'},
        {'title': 'Диджитал Дизайн'},
        {'title': 'Доксвижн'},
        {'title': 'EmBox'},
        {'title': 'JetBrains Research'},
        {'title': 'ПАО "Газпром нефть"'},
        {'title': 'ООО "Газпромнефть НТЦ"'},
        {'title': 'ООО "Техкомпания Хуавей"'},
        {'title': 'TickVision'},
        {'title': 'Mobile Robotics Lab, Skoltech'},
        {'title': 'Etersof'},
        {'title': 'ООО "КНС Групп"'},
        {'title': 'Научно-образовательный центр "Математическая робототехника и искусственный интеллект"'},
        {'title': 'ООО "Научно-производственное предприятие «Новые Технологии Телекоммуникаций"'},
    ]

    # Init DB
    db.session.commit() # https://stackoverflow.com/questions/24289808/drop-all-freezes-in-flask-with-sqlalchemy
    db.drop_all()
    db.create_all()

    # Create users
    print("Create users")
    for user in users:
        u = Users(email=user['email'], password_hash = generate_password_hash(urandom(16).hex()), first_name = user['first_name'], last_name = user['last_name'],
                 avatar_uri = user['avatar_uri'])

        db.session.add(u)
        db.session.commit()

    # Create levels
    print("Create levels")
    for level in levels:
        lv = Level(title=level['title'])

        db.session.add(lv)
        db.session.commit()

    #Create themes
    print("Create themes")
    for theme in themes:
        t = ThesesThemes(supervis=theme['supervis'], depart=theme['depart'], title_ru=theme['title_ru'], description=theme['description'], level_id=theme['level_id'],
                         supervisor_id=theme['supervisor_id'], advisor_id=theme['advisor_id'], author_id=1, requirements=theme['requirements'], worktype=theme['worktype'])

        db.session.add(t)
        db.session.commit()

    # Create departments
    print("Create departments")
    for d in departments:
        dep = Department(title=d['title'])

        db.session.add(dep)
        db.session.commit()

