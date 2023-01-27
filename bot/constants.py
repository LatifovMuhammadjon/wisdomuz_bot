# init data start

TOKEN = '1696068501:AAF2v3BwwEdmfxAEmnqpHa8ksckKqEwqxXc'
# BASE_URL = "https://wisdom.jamgirov.uz"
BASE_URL = "https://wisdomuzbot-production.up.railway.app"
BOT_USERNAME = "wisdom_uzb_bot"

HOW_TO_USE_LINK = "https://telegra.ph/Wisdom-edubot-Qollanmasi-02-05"

CHAT_ID_WISDOM = -1001672195679
CHAT_ID_FOR_NOTIFIER = -1001351409192

BONUS_FOR_NEW_USER = 3
BONUS_FOR_MEMBERSHIP_TO_CHANNEL = 5

PRICE_OF_ENERGY = 500

ENERGY_FOR_MONEY = {
    5000: 10,
    10000: 25,
    15000: 40,
    20000: 55,
    25000: 75,
    30000: 100,
    35000: 120,
    40000: 150,
    45000: 175,
    50000: 200
}

CHANNEL_NAME = "Wisdom English"
WISDOM_LINK = "https://t.me/wisdomeng"
OPERATOR = "@wisd0man"

BOT_COMMANDS = [
    {
        "command": 'start',
        "description": "Foydalanishni boshlash"
    },
    {
        "command": 'books',
        "description": "Kitoblar"
    },
    {
        "command": 'exercises',
        "description": "Mashqlar"
    },
    {
        "command": 'battle',
        "description": "Bellashuv"
    },
    {
        "command": 'rating',
        "description": "Reyting"
    },
    {
        "command": 'vocabulary',
        "description": "Qancha so'z bilasiz ?"
    },
    {
        "command": 'info',
        "description": "Ma'lumotlar"
    },
    {
        "command": 'guide',
        "description": "Foydalanish bo'yicha qo'llanma"
    },
]

# init data end


# languages start

LANGUAGE_UZ = 'uz'

# languages end


# status info start

STATUS_INACTIVE = 0
STATUS_ACTIVE = 1

# status info end


# user step start

STEP_START = 0
STEP_MAIN_MENU = 1
STEP_TESTING_BY_QUIZ = 2
STEP_START_BATTLE = 3
STEP_ANSWERING_VOCABULARY_TEST = 4

# user step end


# callback step start

CALLBACK_BACK_TO_SENDING = -1
CALLBACK_CONFIRM_MEMBERSHIP = 0
CALLBACK_SELECT_BOOK_FOR_INFO = 1
CALLBACK_SELECT_PERIOD_FOR_RATING = 2
CALLBACK_SELECT_BOOK_FOR_EXERCISE = 3
CALLBACK_SELECT_THOUSAND_FOR_EXERCISE = 4
CALLBACK_SELECT_HUNDRED_FOR_EXERCISE = 5
CALLBACK_NEXT_EXERCISE = 6
CALLBACK_SELECT_BOOK_FOR_BATTLE = 7
CALLBACK_SELECT_THOUSAND_FOR_BATTLE = 8
CALLBACK_START_BATTLE_WITH_RANDOM_OPPONENT = 9
CALLBACK_NEXT_WORD = 10
CALLBACK_REQUEST_FOR_REVENGE = 11
CALLBACK_PROCESS_REQUEST_FOR_BATTLE = 12
CALLBACK_JOINING_TO_CHANNELS = 13
CALLBACK_PAYING_FOR_ENERGY = 14
CALLBACK_SELECT_CHANNEL_TO_JOINING = 15
CALLBACK_SELECT_PROVIDER = 16
CALLBACK_SELECT_AMOUNT = 17

# callback step end


# back to first message start

BACK_TO_EARN_HANDLER = -2
BACK_TO_BOOK_HANDLER = -1
BACK_TO_WORDS_HANDLER = 0
BACK_TO_SETTINGS_HANDLER = 1
BACK_TO_EXERCISES_HANDLER = 2
BACK_TO_BATTLE_HANDLER = 3

# back to first message end


class MESSAGE:

    class TYPE:
        TEXT = '0'
        PHOTO = '1'
        AUDIO = '2'
        VOICE = '3'
        VIDEO = '4'

        DICT = {
            TEXT: "Text message",
            PHOTO: "Photo message",
            AUDIO: "Audio message",
            VOICE: "Voice message",
            VIDEO: "Video message"
        }

        CHOICE = DICT.items()
