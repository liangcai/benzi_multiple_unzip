import PySimpleGUI as sg
from bulk_archiver import Extractall, MakeArchiver
from __init__ import logger


# sg.theme('Dark Blue 3')
sg.ChangeLookAndFeel('GreenTan')

task_types = [
    {'text': '批量解压', 'key': '__ExtractAll__', 'tooltip': '批量解压任务'},
    {'text': '批量压缩', 'key': '__MakeArchiver__', 'tooltip': '批量压缩任务'},
]

# radio = [[sg.Radio(task['text'], 1),] for task in task_types]
radio = [sg.Radio(task['text'], 1, key=task['key'], tooltip=task['tooltip']) for task in task_types]

layout = [
    [sg.Text('批量压缩解压工具', size=(20, 1)),],
    # [sg.Text('选择要解压的文件所在的根目录（解压所选择的文件夹下所有的压缩文件）')],
    # [sg.Radio('批量解压', 1, default=True, key='__TASK_UNZIP__', tooltip='批量解压任务'), sg.Radio('批量压缩', group_id=1, default=False, key='__TASK_ZIP__', tooltip='批量压缩任务')]
    radio,
    [sg.Text('选择来源文件夹', size=(16, 1)), sg.FolderBrowse(key='__SOURCE__', size=(16, 1))],
    [sg.Text('选择目标文件夹', size=(16, 1)), sg.FolderBrowse(key='__TARGET__', size=(16, 1))],
    [sg.Text('解压密码(非必须)', size=(16, 1), justification='left'), sg.Input("", key="__PWD__", size=(16, 1))],
    [sg.Frame(layout=[[sg.Submit("Submit"), sg.Cancel("Cancel")]], title='')]
    
]

window = sg.Window('批量解压和批量压缩程序', layout, size=(500, 350), element_justification='center', grab_anywhere=False, resizable=False)

def run_gui():
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):
            break

        if event == 'Submit':
            logger.debug('values: {}'.format(values))
            source = values['__SOURCE__']
            target = values['__TARGET__']
            pwd = values['__PWD__']
            task = 'ExtractAll' if values['__ExtractAll__'] else 'MakeArchiver'
            if task == 'ExtractAll':
                task = Extractall(archivers=source, extracts=target, pwd=pwd)
            elif task == 'MakeArchiver':
                task = MakeArchiver(archivers=target, extracts=source, pwd=pwd)
            else:
                break
            logger.debug('{} gui command run: archivers: {}, extracts: {}, pwd: {}'.format(task, target, source, pwd))
            task.run()

    window.close()


if __name__ == '__main__':
    
    # task = Extractall(archivers='/Users/cail/Downloads/tmp/', extracts='/Users/cail/Downloads/tmp/unzip/')
    # task = MakeArchiver(archivers='/Users/cail/Downloads/tmp/zip/', extracts='/Users/cail/Downloads/tmp/unzip/')
    # task.run()

    run_gui()