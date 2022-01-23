import PySimpleGUI as sg


left_side = [
    [sg.Text('left_side')],
    [sg.Text(size=(40, 1), key="-LTOUT-")],
]

right_side = [
    [sg.Text('left_side')],
    [sg.Text(size=(40, 1), key="-RTOUT-")],
]


layout = [
    [
        sg.Column(left_side),
        sg.VSeperator(),
        sg.Column(right_side)
    ]
]


window = sg.Window('Noggin', layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
window.close()
