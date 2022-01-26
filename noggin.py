# noggin.py

import PySimpleGUI as sg
import os.path
from re import findall

sg.theme('DarkGrey13')
sg.set_options(element_padding=(1, 1))
ic = "nog.ico"


def rename(original):
    layout = [[sg.T('File Name:')],
              [sg.I(original[:-4])],
              [sg.Ok(size=(39, 1), bind_return_key=True)]]
    window = sg.Window('Noggin Name', layout, icon=ic)
    event, values = window.read(close=True)
    return values[0]


def delete_noggin():
    filename = str_name()
    layout = [[sg.T('Are you sure?')],
              [sg.Ok(size=(20, 1)),
               sg.Cancel(size=(20, 1))]]
    window = sg.Window(f'Delete: {filename}', layout, icon=ic)
    event, values = window.read()
    if event == 'Ok':
        name = str_name()
        del_noggin(name)
        window.close()
    else:
        window.close()


def str_name():
    try:
        inputString = values['-NAME-']
        name = findall("\'(.*?)\'", inputString)
        return name[0]
    except IndexError:
        pass


def refresh_entries():
    saved_entries = os.listdir('entries')
    return saved_entries


def load_entry(item):
    with open(f'entries/{item[0]}') as f:
        text = f.read()
    window['-MULTI-'].update(text)


def new_noggin():
    filename = rename('')
    if filename:
        with open(f'entries/{filename}.nog', mode='a'):
            window['-LIST-'].update(refresh_entries())
            window['-NAME-'].update([f'{filename}.nog'])
            load_entry([f'{filename}.nog'])


def rename_old(old_name):
    try:
        filename = rename(str_name())
        if filename:
            os.rename(f'entries/{old_name}', f'entries/{filename}.nog')
            window['-NAME-'].update(f'{filename}.nog')
            window['-LIST-'].update(refresh_entries())
            window['-NAME-'].update([f'{filename}.nog'])
            load_entry([f'{filename}.nog'])

    except TypeError:
        pass


def del_noggin(item):
    try:
        os.remove(f'entries/{item}')
        window['-MULTI-'].update("")
        window['-NAME-'].update("")
        window['-LIST-'].update(refresh_entries())
    except FileNotFoundError:
        pass


def update_noggin(item):
    if values['-NAME-']:
        try:
            with open(f'entries/{item}', mode='w') as f:
                content = values['-MULTI-']
                f.write(content)
                window['-LIST-'].update(refresh_entries())
        except TypeError:
            pass


# window layout of the columns
entries_column = [[sg.Button('New', size=(6, 1), key='-NEW-'), sg.Text('Noggin Entries:')],
                  [sg.Listbox(refresh_entries(), size=(33, 23),
                              enable_events=True, key="-LIST-")],
                  [sg.Text('Filter:'), sg.Input(size=(30, 1), enable_events=True, key='-FILTER-')]]

read_column = [[sg.Button('Save', size=(16, 1), key='-SAVE-'),
                sg.Button('Rename', size=(17, 1), key='-REN-'),
                sg.Button('Delete', size=(17, 1), key='-DEL-')],
               [sg.Text('Viewing:'), sg.Input(size=(53, 1), key='-NAME-')],
               [sg.Multiline(size=(60, 24),  key="-MULTI-")]]

layout = [[sg.Column(entries_column),
           sg.VSeperator(),
           sg.Column(read_column)]]

window = sg.Window('Noggin v1.0 - V.Rossini', layout, icon=ic)

# Event loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if values['-FILTER-'] != '':
        search = values['-FILTER-']
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
        delete_noggin()
    if event == '-SAVE-':
        update_noggin(str_name())
    if event == '-REN-':
        rename_old(str_name())
window.close()