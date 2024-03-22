import inquirer
from termcolor import colored
from inquirer.themes import load_theme_from_dict as loadth


def get_action() -> str:
    """ Пользователь выбирает действие через меню"""

    choise_dict = {
        '   1) Import wallets from the spreadsheet to the DB': 1,
        '   2) Export wallets from the DB to the spreadsheet': 2,
        '   3) Start the script': 3,
    }

    # Тема
    theme = {
        'Question': {
            'brackets_color': 'bright_yellow'
        },
        'List': {
            'selection_color': 'bright_blue'
        },
    }

    # Варианты для выбора
    question = [
        inquirer.List(
            "action",
            message=colored('Выберете ваше действие', 'light_yellow'),
            choices=[key for key in choise_dict.keys()]
        )
    ]

    return choise_dict[inquirer.prompt(question, theme=loadth(theme))['action']]
