from enum import unique
from peewee import *

db = SqliteDatabase('data_base/people.db')
db_1 = SqliteDatabase('data_base/Repka_about_user_and_blok.db')


class BaseModel(Model):
    id = PrimaryKeyField(unique = True)

    class Meta:
        database = db # This model uses the "people.db" database.
        order_by = 'id'

class Names(BaseModel):
    name = CharField()

    class Meta:
        db_table = "names"

class Id(BaseModel):
    id_tl = IntegerField()
    

    class Meta:
        db_table = "id_person_all"    

class Id_c(BaseModel):
    id_tl = IntegerField()
    name = CharField()


    class Meta:
        db_table = "id"    


class All_regist(BaseModel):
    id_tlbot = ForeignKeyField(Id)
    name = ForeignKeyField(Names)
    datetime = DateField()
    day_regist = DateField()
    room = CharField()
    oneORgroup = CharField()
    pay_for_time = FloatField()
    number = CharField()

    class Meta:
       db_table = "All_regist"

class Time(BaseModel):
    time = CharField()
    person = ForeignKeyField(All_regist)

    class Meta:
        db_table = "time"


class All_regist_copy(BaseModel):
    id_tlbot = ForeignKeyField(Id)
    name = ForeignKeyField(Names)
    datetime = DateField()
    day_regist = DateField()
    room = CharField()
    oneORgroup = CharField()
    pay_for_time = FloatField()
    number = CharField()

    class Meta:
        db_table = "All_regist_copy"


# class Write_people(BaseModel):
#     id_user = IntegerField()
#     Yuor_names = CharField()

class Blok_user(BaseModel):
    id_user = IntegerField()
    reason = CharField()
    
    class Meta:
        db_table = "Blok"