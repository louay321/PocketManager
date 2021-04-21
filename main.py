"""This is a university related project that uses python GUI
 and other modules, created by Nahdi Louay.
 uses file manipulation, JSON for data storage,
 PySimpleGUI and YAML for config retrieval.
 """


from datetime import date
import json
import PySimpleGUI as sg
import yaml

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from budget import budget

#      Testing the budget class objects
# test_budget = budget(date.today().strftime("%m/%d/%y"), 2000)
# print(test_budget.view_budget())

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

# get the configuration for the app
yaml_path = 'config.yaml'
with open(yaml_path) as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# set the theme for the application
sg.theme(config['theme-color'])

# write the data to a json file
def writeToJson(path, fileName, data):
    fullPathWname = path + fileName + '.json'
    with open(fullPathWname, 'w') as file:
        json.dump(data, file, indent=4)


def main():
    print("project building..")

# Columns creation.
    first_column = [
        [sg.Text(config['section-label'][0])],
        [sg.Text(config['text-fields-labels'][0]), sg.Input(key='-INPUT_POCKET-')],
        [sg.Text(config['text-fields-labels'][1]), sg.Input(key='-INPUT_SPENT-')],
        [sg.Text(size=(40, 1), key='-RESULT-')],
        [sg.Button(config['button-label'][0]),
         sg.Button(config['button-label'][1]),
         sg.Button(config['button-label'][2])]
    ]

    second_column = [
        [sg.Text(config['section-label'][1])],
        [sg.Canvas(key="-CANVAS-")],
        [sg.Button(config['button-label'][3])],

    ]

    third_column = [
        [sg.Text(config['section-label'][2])],
    ]
# Layout creation.
    layout = [
        [sg.Text(config['title-label'])],
        [
         sg.Column(first_column),
         sg.VSeparator(),
         sg.Column(second_column),
         sg.VSeparator(),
         sg.Column(third_column)
        ]
             ]

# window creation.
    window = sg.Window(config['title-label'], layout)
    result = ''
    while True:
        event, values = window.read()
        if values['-INPUT_POCKET-'] == "" or values['-INPUT_SPENT-'] == "":
            message = 'please enter amounts'
        else:
            result = int(values['-INPUT_POCKET-']) - int(values['-INPUT_SPENT-'])
            if result > 0:
                message = 'Well done! you saved ' + str(result) + 'HUF !!'
            else:
                message = 'you need to start saving!! amount lost: ' + str(result) + 'HUF'
        window['-RESULT-'].update(message)

        if event == 'Save' and result != '':
            # save the data in an object
            current_budget = budget(date.today().strftime("%m/%d/%y"), result)

        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Quit':
            path = config['file_path']
            filename = config['file_name']
            extension = config['file_extension']
            fullPathWname = path + filename + extension
            with open(fullPathWname) as json_file:
                data = json.load(json_file)
                temp = data["records"]
                # use the budget.date and budget.amount to save in a JSON file
                y = {"date": current_budget.date, "amount": current_budget.amount}
                temp.append(y)
            writeToJson(path, filename, data)
            break
        if event == 'View':
            x = []
            y = []
            # setting up figure plotting
            path = config['file_path'] + config['file_name'] + config['file_extension']
            with open(path) as json_file:
                data = json.load(json_file)
            for item in data["records"]:
                x.append(item["amount"])
                y.append(item["date"])
            # plot the figure using the data in JSON
            fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
            fig.add_subplot().plot(y, x)
            matplotlib.use("TkAgg")
            draw_figure(window["-CANVAS-"].TKCanvas, fig)
    window.close()


if __name__ == '__main__':
    main()