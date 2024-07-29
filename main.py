import flet as ft
from Cliente import Client
from UnityType import UnityType

def main(page: ft.Page):
    subscribers = []
    values = []
    containers = []
    values.extend([None] * 100)
    containers.extend([None] * 100)
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
    page.theme = ft.Theme(color_scheme_seed=ft.colors.GREEN_200)
    page.bgcolor = ft.colors.BROWN_400

    column = ft.Column(controls=[])

    def generateContainer(data, obj: Client):
        values[obj.position] = data
        containers[obj.position] = ft.Card(color=ft.colors.RED_400, content=ft.Container(content=ft.Row(alignment="CENTER", controls=[
            ft.Text(value='ID: ' + str(data['id'])), ft.Text(value=('value: ' + str(round(float(data['data']), 2)))),
            ft.Text(value=('unidade: ' + str(UnityType(data['type']).value)))
            ]), padding=10))
        
    def submit(e):
        if input_text.value in subscribers:
            page.snack_bar.content = ft.Text("Já existe um sensor com esse ID")
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar.content = ft.Text("O Sensor " + str(input_text.value) + " está sendo observado!")
            page.snack_bar.open = True
            page.update()
            if not subscribers:
                subscribers.append(input_text.value)
                Client(input_text.value, generateContainer, 0)
                
            else:
                subscribers.append(input_text.value)
                Client(input_text.value, generateContainer, (subscribers.__len__() -1))
                

    submitButton = ft.ElevatedButton(text="Acompanhar sensor", on_click=submit, style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(10)))
    
    page.add(input_text, submitButton, column)
    while True:
        listItem = []
        for item in containers:
            if item is not None:
                listItem.append(item)
        column.controls = listItem
        page.update()


ft.app(main)
