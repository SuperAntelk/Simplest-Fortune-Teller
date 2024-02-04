import flet as ft
from services.predictor import PredictorService
from datetime import date

def main(page):

    first_name = ft.TextField(label="Введите ФИО", autofocus=True)
    predict = ft.Column()
    get_predict = PredictorService().predict
    def btn_click(e):
        prediction = get_predict(first_name.value, date.today())
        print('button!')
        print(*prediction.as_list(),sep='\n')
        predict.controls.append(ft.Text('\n'.join(prediction.as_list())))
        page.update()

    page.add(
        first_name,
        ft.ElevatedButton("Получить прогноз", on_click=btn_click),
        predict,
    )

ft.app(target=main)