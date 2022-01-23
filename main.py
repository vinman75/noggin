# main.py
import PySimpleGUI as sg
import os.path
import re

sg.theme('DarkBlue4')


def refresh_entries():
    saved_entries = os.listdir('entries')
    return saved_entries


def load_entry(item):
    with open('entries/{}'.format(item[0])) as f:
        text = f.read()
    window['-MULTI-'].update(text)


def new_noggin():
    with open('entries/{}{}.nog'.format('new', 1), mode='a'):
        window['-LIST-'].update(refresh_entries())


def del_noggin(item):
    os.remove('entries/{}'.format(item))
    window['-LIST-'].update(refresh_entries())
    window['-NAME-'].update("")


def update_noggin(old):
    print(old)

    String = values['-NAME-']
    newname = re.findall("\'(.*?)\'", String)
    del_noggin(name[0])
    print(newname[0])

    #os.rename('entries/{}'.format(item), ('entries/{}'.format(newname)))
    # window['-LIST-'].update(refresh_entries())
    # window['-NAME-'].update("")


# window layout of the columns
entries_column = [[sg.Button('New', enable_events=True, key='-NEW-')],

                  [sg.Text('Noggin Entries')], [sg.Listbox(
                      refresh_entries(), size=(40, 20), enable_events=True, key="-LIST-")],
                  [sg.Text('Filter:'), sg.Input(size=(35, 1), enable_events=True, key='-INPUT-')]]

read_column = [[sg.Button('Update', enable_events=True, key='-UPDATE-'), sg.Button('Delete', enable_events=True, key='-DEL-')],
               [sg.Text('Name:'), sg.Input(size=(53, 1),
                                           enable_events=True, key='-NAME-')],
               [sg.Multiline(size=(60, 24), background_color='#ffffff', text_color='black', key="-MULTI-")]]

layout = [[sg.Column(entries_column),
           sg.VSeperator(),
           sg.Column(read_column)]]

window = sg.Window('Noggin', layout)

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
        inputString = values['-NAME-']
        name = re.findall("\'(.*?)\'", inputString)
        del_noggin(name[0])

    if event == '-UPDATE-':
        inputString = values['-NAME-']
        name = re.findall("\'(.*?)\'", inputString)
        update_noggin(name[0])

window.close()
