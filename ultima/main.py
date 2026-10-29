from sqlalchemy import create_engine, Column, Integer, Text, func, desc
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import json

engine = create_engine('sqlite:///survey.db')
Session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


class OprosDB(Base):
    __tablename__ = 'opros'
    id = Column(Integer, primary_key=True)
    answers = Column(Text)


Base.metadata.create_all(engine)  # создание таблиц в БД


class Survey:
    def __init__(self):
        self.questions = [
            'Как дела?',
            'Сколько тебе лет?',
            'Который час?',
            'ФИО?',
            'Да или нет?',
            'Мальчик вырос в камышах?',
            'Ультима тест?'
        ]
        self.step = self.read_step()
        self.answer = ''

    def read_step(self):
        try:
            with open('step.txt', encoding='UTF-8') as file:
                step = int(file.read())
                return step
        except FileNotFoundError:
            with open('step.txt', 'w', encoding='UTF-8') as file:
                file.write('0')
                return 0

    def save_step(self):
        with open('step.txt', 'w', encoding='UTF-8') as file:
            file.write(f'{self.step}')

    def polling(self):
        self.answer = input(f'{self.questions[self.step]} -> ')
        add_answer(self.step, self.answer)  # Здесь будет запись ответа
        self.step += 1
        self.save_step()
        if self.step == len(self.questions):
            self.step = 0
            self.save_step()
            exit()
        self.polling()


def add_answer(key: int, value: str):
    s = Session()
    max_id = s.query(func.max(OprosDB.id)).scalar()  # получаем цифру максимального айди.
    field = s.query(OprosDB).order_by(desc(OprosDB.id)).first()  # последнее заполненное поле.
    if not field:
        field = OprosDB(id=1, answers=json.dumps({key: value}, ensure_ascii=False))
        s.add(field)
    else:
        current_answers = json.loads(field.answers)
        if len(current_answers) < 7:
            current_answers[key] = value
            field.answers = json.dumps(current_answers, ensure_ascii=False)
        else:
            field = OprosDB(id=max_id + 1, answers=json.dumps({key: value}, ensure_ascii=False))
            s.add(field)
    s.commit()


survey = Survey()
survey.polling()
