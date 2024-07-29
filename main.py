import flet as ft
from Cliente import Client
from DataType import DataType
import threading
import queue
import time

def main(page: ft.Page):
    subscriberList = []
    dataList = []
    containerList = []
    dataList.extend([None] * 150)
    containerList.extend([None] * 150)
    input_text = ft.TextField( label="ID", hint_text="Digite o ID do sensor que quer observar")
    page.title = "Subscriber"
    page.horizontal_alignment = "CENTER"
    page.snack_bar = ft.SnackBar(
        content=ft.Text("O Sensor " + str(input_text.value) + " está sendo observado!"),
        action="Ok!",
    )
    page.window.width = 500
    page.window.resizable = False
    page.theme = ft.Theme(color_scheme_seed=ft.colors.PURPLE_ACCENT_700)
    column = ft.Column(controls=[])
    def generateContainer(data, obj: Client):
        dataList[obj.position] = data
        if data['alarm'] == 'True':
            containerList[obj.position] = ft.Text(color=ft.colors.AMBER_400, value=('ID: ' + str(data['id']) + ' valor: ' + str(round(float(data['data']), 2)) + ' unidade: ' + str(DataType(str(data['type'])).value) + ' alarme: ' + str(data['alarm'])))
        else:
            containerList[obj.position] = ft.Text(color=ft.colors.GREEN_400, value=('ID: ' + str(data['id']) + ' valor: ' + str(round(float(data['data']), 2)) + ' unidade: ' + str(DataType(str(data['type'])).value) + ' alarme: ' + str(data['alarm'])))
    def submit(e):
        if input_text.value in subscriberList:
            page.snack_bar.content = ft.Text("Já existe um sensor com esse ID")
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar.content = ft.Text("O Sensor " + str(input_text.value) + " está sendo observado!")
            page.snack_bar.open = True
            page.update()
            if not subscriberList:
                subscriberList.append(input_text.value)
                Client(input_text.value, generateContainer, 0)
                
            else:
                subscriberList.append(input_text.value)
                Client(input_text.value, generateContainer, (subscriberList.__len__() -1))
                

    button = ft.ElevatedButton(text="Observar!", on_click=submit)
    
    page.add(input_text, button, column)
    while True:
        listItem = []
        for item in containerList:
            if item is not None:
                listItem.append(item)
        column.controls = listItem
        page.update()


ft.app(main)
