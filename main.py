# main.py
import PySimpleGUI as sg
import os.path
import re

sg.theme('DarkGrey9')


def rename(original):
    layout = [[sg.Text('File Name')],
              [sg.Input(original[:-4])],
              [sg.Button('Okay', enable_events=True,
                         key='-REN-', bind_return_key=True)]
              ]
    popWin = sg.Window('Noggin Name', layout, icon="noggin-icon.ico")

    while True:     # Event Loop
        event, values = popWin.read()

        if event == '-REN-' or event == sg.WIN_CLOSED:
            print(values[0])
            break
    popWin.close()
    return values[0]


def confirm():
    filename = clean_str()
    layout = [[sg.Text('Are you sure you want to delete: {} ?'.format(filename))],
              [sg.Button('Yes', enable_events=True, key='-CONFIRM-'),
               sg.Button('No', enable_events=True, key='-CANCEL-')]]

    confirmWin = sg.Window('Noggin Name', layout, icon="noggin-icon.ico")

    while True:     # Event Loop
        event, values = confirmWin.read()

        if event == sg.WIN_CLOSED:
            break

        if event == '-CONFIRM-':
            name = clean_str()
            del_noggin(name)
        else:
            pass
        confirmWin.close()


def clean_str():
    try:
        inputString = values['-NAME-']
        name = re.findall("\'(.*?)\'", inputString)
        return name[0]
    except IndexError:
        pass


def refresh_entries():
    saved_entries = os.listdir('entries')
    return saved_entries


def load_entry(item):
    with open('entries/{}'.format(item[0])) as f:
        text = f.read()
    window['-MULTI-'].update(text)


def new_noggin():
    filename = rename('')
    if filename:
        with open('entries/{}.nog'.format(filename), mode='a'):
            window['-LIST-'].update(refresh_entries())


def rename_old():
    try:
        inputString = values['-NAME-']
        old_name = re.findall("\'(.*?)\'", inputString)

        filename = rename(clean_str())
        if filename:
            os.rename('entries/{}'.format(old_name[0]),
                      'entries/{}.nog'.format(filename))
            window['-NAME-'].update('{}.nog'.format(filename))
            window['-LIST-'].update(refresh_entries())
    except TypeError:
        pass


def del_noggin(item):
    try:
        os.remove('entries/{}'.format(item))
        window['-MULTI-'].update("")
        window['-NAME-'].update("")
        window['-LIST-'].update(refresh_entries())
    except FileNotFoundError:
        pass


def update_noggin(item):
    if values['-NAME-']:
        try:
            with open('entries/{}'.format(item), mode='w') as f:
                content = values['-MULTI-']
                f.write(content)
                window['-LIST-'].update(refresh_entries())
        except TypeError:
            pass


# window layout of the columns
entries_column = [[sg.Button('New', enable_events=True, key='-NEW-')],

                  [sg.Text('Noggin Entries')],
                  [sg.Listbox(refresh_entries(), size=(40, 20),
                              enable_events=True, key="-LIST-")],
                  [sg.Text('Filter:'), sg.Input(size=(35, 1), enable_events=True, key='-INPUT-')]]

read_column = [[sg.Button('Save', enable_events=True, key='-SAVE-'),
                sg.Button('Rename', enable_events=True, key='-REN-'),
                sg.Button('Delete', enable_events=True, key='-DEL-')],
               [sg.Text('Name:'), sg.Input(size=(53, 1), readonly=False,
                                           enable_events=True, key='-NAME-')],
               [sg.Multiline(size=(60, 24),  key="-MULTI-")]]

layout = [[sg.Column(entries_column),
           sg.VSeperator(),
           sg.Column(read_column)]]

window = sg.Window('Noggin', layout, icon="noggin-icon.ico")

# Event loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if values['-INPUT-'] != '':
        search = values['-INPUT-']
        filtered = [x for x in refresh_entries() if search in x]
        window['-LIST-'].update(filtered)
    else:
        window['-LIST-'].update(refresh_entries())
    if event == '-LIST-' and len(values['-LIST-']):
        load_entry(values['-LIST-'])
        window['-NAME-'].update(values['-LIST-'])
    if event == '-NEW-':
        new_noggin()
    if event == '-DEL-':
        confirm()
    if event == '-SAVE-':
        name = clean_str()
        update_noggin(name)
    if event == '-REN-':
        rename_old()
window.close()
