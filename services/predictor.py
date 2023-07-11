import time
from datetime import date
from collections import Counter
from functools import reduce
from dataclasses import dataclass, asdict


KEYS=['Д-дорога',
    'Н-неожиданность',
    'У-удача',
    'В-встреча',
    'Р-радость',
    'О-обида']
DAY_LIST = ['первое', 'второе', 'третье', 'четвёртое',
        'пятое', 'шестое', 'седьмое', 'восьмое',
        'девятое', 'десятое', 'одиннадцатое', 'двенадцатое',
        'тринадцатое', 'четырнадцатое', 'пятнадцатое', 'шестнадцатое',
        'семнадцатое', 'восемнадцатое', 'девятнадцатое', 'двадцатое',
        'двадцать первое', 'двадцать второе', 'двадцать третье',
        'двадацать четвёртое', 'двадцать пятое', 'двадцать шестое',
        'двадцать седьмое', 'двадцать восьмое', 'двадцать девятое',
        'тридцатое', 'тридцать первое']
MONTH_LIST = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
           'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']




@dataclass
class Time_prediction:
    predict:dict
    key_len:int
    key:str

@dataclass
class Day_predicition:
    name:str
    date:str
    code:str
    keys:list[str]
    predictions:dict[str,Time_prediction]
    def __init__(self):
        pass

class PredictorService:
    def date_to_words(self,date):    
        return f'{DAY_LIST[date.day-1]} {MONTH_LIST[date.month-1]}'

    def predict_for_time(self,time_code,code):
        new_code=code.copy()
        for ch in time_code:
            if ch in new_code:
                new_code[ch]+=1
            else:
                new_code[ch]=1 
    
        return self.delete_odds(new_code)
    def delete_odds(self,code):
        new_code={k:v for k,v in code.items() if v%2!=0}
        return new_code
    def predict(self,name,date):
        output=Day_predicition()
        name=name.lower()
        print(name)
        output.name=name
        date=self.date_to_words(date)
        print(date)
        output.date=date
        raw_code=(name+date).replace(" ","")
        
        code=dict(Counter(raw_code))
        print(code)
        output.code=code
        code=self.delete_odds(code)
        print(code)
        
        print(*code.keys())
        output.keys=list(code.keys())

        predictions={}
        for time_code in 'утро','день','вечер':
            print(time_code)
            print(predict:=self.predict_for_time(time_code,code))
            print(key_len:=len(predict))
            
            print(KEYS[key_len%6])
            predictions[time_code]=Time_prediction(**{'predict':predict,'key_len':key_len,'key':KEYS[key_len%6]})
        output.predictions=predictions
        #return name,date,code,code.keys(),predictions
        return output