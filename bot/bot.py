from django.db.models import Q
from telebot import TeleBot
from telebot.apihelper import ApiException
from telebot.types import Message, CallbackQuery, BotCommand, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery, InlineQueryResultCachedPhoto, InlineQueryResultArticle, InputTextMessageContent, LabeledPrice

from django.utils import timezone

from .models import User, Pocket, Book, Word, Exercise, Battle, Participant, Channel, Provider, Payment, Training
from .constants import *
from .texts import Text

import random


bot = TeleBot(TOKEN, parse_mode='html')

bot.set_webhook(f"{BASE_URL}/bot/{TOKEN}/")

bot.set_my_commands(
    commands=[BotCommand(command['command'], command['description']) for command in BOT_COMMANDS]
)

bot.text = Text(LANGUAGE_UZ)


def auth(handler):
    def wrapper(message: Message):
        if message.chat.type == 'private':
            user: User = User.get(user_id=message.from_user.id)
            if user and user.is_member and not user.is_banned:
                handler(message, user)
            else:
                start_handler(message)
    return wrapper


def go_to_main(user: User):
    user.set_step()
    bot.send_message(
        user.user_id,
        bot.text.main_text,
        reply_markup=get_keyboard_markup(bot.text.main_markup, False)
    )


def get_keyboard_markup(buttons, on_time=True):
    keyboard_markup = ReplyKeyboardMarkup(True, on_time)
    for row in buttons:
        if type(row) is list:
            keyboard_markup.add(*[KeyboardButton(button) for button in row])
        else:
            keyboard_markup.add(KeyboardButton(row))
    return keyboard_markup


def check_user_membership(user_id, channels=None):
    if not channels:
        channels = Channel.filter(required=True, is_active=True)
    for channel in channels:
        try:
            chat_member = bot.get_chat_member(
                channel.channel_id,
                user_id
            )
            if chat_member.status not in ['creator', 'administrator', 'member']:
                return False
        except ApiException as e:
            print(f"Checking membership for {user_id}: {e.args}")
            return False
    return True


@bot.message_handler(commands=['start'])
def start_handler(message: Message):
    user: User = User.get(user_id=message.from_user.id)
    if user and user.is_banned:
        bot.reply_to(
            message,
            bot.text.you_are_banned.format(
                operator=OPERATOR
            ),
        )
        return
    if check_user_membership(message.from_user.id):
        if not user:
            inviter = None
            full_name = f"{message.from_user.first_name}{f' {message.from_user.last_name}' if message.from_user.last_name else ''}".replace('<', '').replace('>', '')
            data = message.text.split()
            if len(data) == 2:
                inviter: User = User.get(user_id=data[1])
                if inviter:
                    inviter.give_bonus(BONUS_FOR_NEW_USER)
                    try:
                        bot.send_message(
                            inviter.user_id,
                            bot.text.bonus_for_new_referral.format(
                                user_id=message.from_user.id,
                                full_name=full_name,
                                bonus=BONUS_FOR_NEW_USER
                            )
                        )
                    except ApiException:
                        pass
            user: User = User.create(
                user_id=message.from_user.id,
                inviter=inviter,
                full_name=full_name,
            )
        else:
            user.activate()
        go_to_main(user)
    else:
        inviter_id = 0
        if user:
            user.deactivate()
        else:
            data = message.text.split()
            if len(data) == 2:
                inviter_id = data[1]
        inline_markup = InlineKeyboardMarkup(row_width=1)
        inline_markup.add(
            *[
                InlineKeyboardButton(
                    channel.name,
                    url=channel.link
                ) for channel in Channel.filter(required=True, is_active=True)
            ],
            InlineKeyboardButton(
                bot.text.confirm,
                callback_data=f"{CALLBACK_CONFIRM_MEMBERSHIP} {inviter_id}"
            )
        )
        bot.reply_to(
            message,
            bot.text.join_this_channels,
            reply_markup=inline_markup,
        )


@bot.message_handler(commands=['earn'])
@bot.message_handler(regexp='^🟡 ')
@auth
def earn_handler(message: Message, user: User):
    if user.step == STEP_MAIN_MENU:
        inline_markup = InlineKeyboardMarkup(row_width=1)
        inline_markup.add(
            InlineKeyboardButton(
                bot.text.sharing_with_friends,
                switch_inline_query=""
            ),
            InlineKeyboardButton(
                bot.text.joining_to_channels,
                callback_data=f"{CALLBACK_JOINING_TO_CHANNELS}"
            ),
            InlineKeyboardButton(
                bot.text.pay_for_energy,
                callback_data=f"{CALLBACK_PAYING_FOR_ENERGY}"
            ),
            InlineKeyboardButton(
                bot.text.back,
                callback_data=f"{CALLBACK_BACK_TO_SENDING} -111"
            )
        )
        bot.reply_to(
            message,
            bot.text.earn_info.format(
                bonus_for_referral=BONUS_FOR_NEW_USER,
                bonus_for_joining_to_channel=BONUS_FOR_MEMBERSHIP_TO_CHANNEL,
                price_of_energy=PRICE_OF_ENERGY
            ),
            reply_markup=inline_markup
        )


@bot.message_handler(commands=['books'])
@bot.message_handler(regexp='^📚 ')
@auth
def books_handler(message: Message, user: User):
    if user.step == STEP_MAIN_MENU:
        books = Book.filter(is_active=True).order_by('order')
        if books.count():
            inline_markup = InlineKeyboardMarkup(row_width=1)
            inline_markup.add(
                *[
                    InlineKeyboardButton(
                        book.name,
                        callback_data=f"{CALLBACK_SELECT_BOOK_FOR_INFO} {book.id}"
                    ) for book in books
                ]
            )
            bot.send_message(
                user.user_id,
                bot.text.select_book_for_info,
                reply_markup=inline_markup,

            )
        else:
            bot.reply_to(
                message,
                bot.text.books_not_found,

            )


@bot.message_handler(commands=['exercises'])
@bot.message_handler(regexp='^🤓 ')
@auth
def exercises_handler(message: Message, user: User):
    if user.step == STEP_MAIN_MENU:
        inline_markup = InlineKeyboardMarkup(row_width=1)
        inline_markup.add(
            *[
                InlineKeyboardButton(
                    book.name,
                    callback_data=f"{CALLBACK_SELECT_BOOK_FOR_EXERCISE} {book.id}"
                ) for book in Book.filter(is_active=True)
            ]
        )
        bot.send_message(
            message.chat.id,
            bot.text.select_book_for_exercise,
            reply_markup=inline_markup,
        )


@bot.message_handler(commands=['battle'])
@bot.message_handler(regexp='^⚔️ ')
@auth
def battle_handler(message: Message, user: User):
    if user.step == STEP_MAIN_MENU:
        inline_markup = InlineKeyboardMarkup(row_width=1)
        inline_markup.add(
            *[
                InlineKeyboardButton(
                    book.name,
                    callback_data=f"{CALLBACK_SELECT_BOOK_FOR_BATTLE} {book.id}"
                ) for book in Book.filter(is_active=True)
            ]
        )
        bot.send_message(
            message.chat.id,
            bot.text.select_book_for_battle,
            reply_markup=inline_markup,
        )


@bot.message_handler(commands=['rating'])
@bot.message_handler(regexp='^📊 ')
@auth
def rating_handler(message: Message, user: User):
    if user.step == STEP_MAIN_MENU:
        inline_markup = InlineKeyboardMarkup()
        inline_markup.add(
            *[
                InlineKeyboardButton(
                    period,
                    callback_data=f"{CALLBACK_SELECT_PERIOD_FOR_RATING} {index}"
                ) for index, period in enumerate(bot.text.stat_filter_by_time)
            ]
        )
        top = sorted(User.filter(is_banned=False, is_member=True), key=lambda u: u.daily, reverse=True)
        place = top.index(user)




        bot.send_message(
            user.user_id,
            bot.text.rating.format(
                period=bot.text.stat_filter_by_time[0],
                top="\n".join([f"{bot.text.places[index]} {us.level} <b>{us}</b> - {us.daily} 💎" for index, us in enumerate(top[:10])]),
                me=f"\n\n{place + 1}) {user.level} <b>{user}</b> - {user.daily} 💎" if place >= 10 else ''
            ),
            reply_markup=inline_markup,
        )


@bot.message_handler(commands=['vocabulary'])
@bot.message_handler(regexp='^🎯 ')
@auth
def vocabulary_handler(message: Message, user: User):
    if user.step == STEP_MAIN_MENU:
        bot.send_message(
            user.user_id,
            bot.text.vocabulary_info,
            reply_markup=get_keyboard_markup([bot.text.start_vocabulary_test, bot.text.back])
        )


@bot.message_handler(commands=['info'])
@bot.message_handler(regexp='^ℹ️ ')
@auth
def guide_handler(message: Message, user: User):
    if user.step == STEP_MAIN_MENU:
        bot.send_message(
            user.user_id,
            bot.text.info.format(
                level=user.level,
                full_name=user.full_name,
                energy=user.energy,
                diamonds=user.diamonds
            ),
        )


@bot.message_handler(commands=['guide'])
@bot.message_handler(regexp='^❓ ')
@auth
def guide_handler(message: Message, user: User):
    if user.step == STEP_MAIN_MENU:
        bot.send_message(
            user.user_id,
            bot.text.guide.format(
                link=HOW_TO_USE_LINK
            ),
        )


@bot.message_handler(regexp="^🏁 ")
@auth
def start_vocabulary_test_handler(message: Message, user: User):
    if user.step == STEP_MAIN_MENU:
        if user.energy > 0:
            user.energy -= 1
            word = random.choice(list(Word.filter(id__gte=1, id__lte=1000)))
            user.set_step(STEP_ANSWERING_VOCABULARY_TEST, f"{word.id} 0 0 1000")
            bot.send_message(
                message.chat.id,
                f"1) {word.translation}",
                reply_markup=get_keyboard_markup(word.options)
            )
        else:
            bot.send_message(
                message.chat.id,
                bot.text.energy_is_not_enough_for_vocabulary_test,
                reply_markup=get_keyboard_markup(bot.text.main_markup)
            )


@bot.message_handler(regexp="^🔙 ")
@auth
def back_handler(message: Message, user: User):
    if user.step == STEP_MAIN_MENU:
        go_to_main(user)


@bot.message_handler(func=lambda message: True)
@auth
def all_message_handler(message: Message, user: User):
    if user.step == STEP_MAIN_MENU:
        bot.reply_to(
            message,
            message.text
        )
    elif user.step == STEP_ANSWERING_VOCABULARY_TEST:
        word_id, answered_count, true_answers_count, thousand = map(int, user.data.split())
        word = Word.get(id=word_id)
        if message.text == word.word:
            true_answers_count += 1
            if thousand < 18000:
                thousand += 1000
        else:
            if thousand > 1000:
                thousand -= 1000
        answered_count += 1
        if answered_count == 20:
            user.set_step()
            bot.send_message(
                message.chat.id,
                bot.text.vocabulary_test_result.format(
                    count_of_words=answered_count,
                    true_answers_count=true_answers_count,
                    thousand=thousand if thousand == 18000 and true_answers_count >= 18 else thousand - 1000 if thousand > 1000 else thousand
                ),
                reply_markup=get_keyboard_markup([bot.text.start_vocabulary_test, bot.text.back])
            )
        else:
            word = random.choice(list(Word.filter(id__gte=thousand - 999, id__lte=thousand)))
            user.set_step(STEP_ANSWERING_VOCABULARY_TEST, f"{word.id} {answered_count} {true_answers_count} {thousand}")
            bot.send_message(
                message.chat.id,
                f"{answered_count + 1}) {word.translation}",
                reply_markup=get_keyboard_markup(word.options)
            )


@bot.channel_post_handler(regexp="^#notify")
def channel_post_handler(message: Message):
    if message.chat.id == CHAT_ID_FOR_NOTIFIER:
        now = timezone.now()
        if now.hour == 0 and 0 <= now.minute < 15:
            yesterday = now - timezone.timedelta(hours=1)
            top = sorted(Pocket.filter(date=yesterday), key=lambda pocket: pocket.diamonds, reverse=True)[:10]
            bot.send_message(
                CHAT_ID_WISDOM,
                bot.text.daily_result.format(
                    date=yesterday.strftime("%d-%m%-%Y"),
                    top="\n".join([f"{bot.text.places[index]}) <b>{pocket.user.level} {pocket.user.full_name}</b> - {pocket.diamonds} 💎" for index, pocket in enumerate(top)]),
                    battles=Battle.filter(created_time__date=yesterday).count(),
                    bot_username=BOT_USERNAME
                ),

            )
        for participant in Participant.filter(end_time__lt=now - timezone.timedelta(minutes=15), battle__finished=False, battle__with_friend=False):
            opponent: Participant = participant.battle.participants.filter(~Q(id=participant.id)).first()
            if opponent and not opponent.started_time:
                participant.participant.pocket.increase(participant.battle.thousand//1000 + 1)
                try:
                    bot.send_message(
                        opponent.participant.user_id,
                        bot.text.you_are_late,
                    )
                    bot.send_message(
                        participant.participant.user_id,
                        bot.text.opponent_are_late,
                        parse_mode="html"
                    )
                except ApiException as e:
                    print(e.args)
            participant.battle.finished = True
            participant.battle.save()
        for user in User.filter(is_member=True):
            if not check_user_membership(user.user_id):
                user.deactivate()


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(
        pre_checkout_query.id,
        True
    )


@bot.message_handler(content_types=['successful_payment'])
@auth
def got_payment(message: Message, user: User):
    amount = message.successful_payment.total_amount//100
    provider: Provider = Provider.get(id=message.successful_payment.invoice_payload)
    if provider:
        payment: Payment = Payment.create(
            user=user,
            provider=provider,
            amount=amount
        )
        user.give_bonus(ENERGY_FOR_MONEY.get(amount))
        bot.reply_to(
            message,
            bot.text.successful_payment_info.format(
                amount=amount,
                payment_id=payment.id,
                provider_payment_charge_id=message.successful_payment.provider_payment_charge_id,
                provider_name=provider.name,
                payed_time=timezone.now().strftime("%d.%m.%Y %H:%M:%S"),
                energy=ENERGY_FOR_MONEY.get(amount)
            ),
            parse_mode='html'
        )


@bot.inline_handler(func=lambda query: True)
def inline_query_handler(query: InlineQuery):
    user: User = User.get(user_id=query.from_user.id)
    results = list()
    if user:
        if user.is_member:
            if query.query and len(query.query.split()) == 2:
                book_id, thousand = query.query.split()
                if book_id.isdigit() and thousand.isdigit():
                    thousand = int(thousand)
                    book: Book = Book.get(id=book_id)
                    if book and book.first <= thousand <= book.last:
                        inline_markup = InlineKeyboardMarkup(row_width=1)
                        inline_markup.add(
                            InlineKeyboardButton(
                                bot.text.accept_battle,
                                callback_data=f"{CALLBACK_PROCESS_REQUEST_FOR_BATTLE} 1 {user.id} {book_id} {thousand}"
                            ),
                            InlineKeyboardButton(
                                bot.text.reject_battle,
                                callback_data=f"{CALLBACK_PROCESS_REQUEST_FOR_BATTLE} 0 {user.id} {book_id} {thousand}"
                            )
                        )
                        results.append(
                            InlineQueryResultArticle(
                                random.randint(100000000, 999999999),
                                bot.text.share_with_friend_title,
                                InputTextMessageContent(
                                    bot.text.share_with_friend_info.format(
                                        user_id=user.user_id,
                                        full_name=user.full_name,
                                        book_name=book.name,
                                        first=thousand - 999,
                                        last=thousand
                                    ),
                                    parse_mode='html'
                                ),
                                reply_markup=inline_markup,
                                description=bot.text.share_with_friend_description
                            )
                        )
            else:
                results.append(
                    InlineQueryResultArticle(
                        random.randint(100000000, 999999999),
                        bot.text.sharing_with_friends,
                        InputTextMessageContent(
                            bot.text.sharing_text.format(
                                bot_username=BOT_USERNAME,
                                user_id=user.user_id
                            ),
                            parse_mode='html'
                        ),
                        description=bot.text.sharing_with_friends_description
                    )
                )
        else:
            results.append(
                InlineQueryResultArticle(
                    random.randint(100000000, 999999999),
                    bot.text.left_title,
                    InputTextMessageContent(
                        bot.text.join_this_channels,
                        parse_mode='html'
                    ),
                    description=bot.text.left_description
                )
            )
    else:
        results.append(
            InlineQueryResultArticle(
                random.randint(100000000, 999999999),
                bot.text.not_member_title,
                InputTextMessageContent(
                    bot.text.for_not_registered_member.format(
                        bot_username=BOT_USERNAME
                    ),

                ),
                description=bot.text.not_member_description.format(
                    bot_username=BOT_USERNAME
                )
            )
        )
    bot.answer_inline_query(query.id, results, 1)


@bot.callback_query_handler(func=lambda query: True)
def callback_query_handler(query: CallbackQuery):
    step, *data = map(int, query.data.split())
    if step == CALLBACK_CONFIRM_MEMBERSHIP:
        if check_user_membership(query.from_user.id):
            user: User = User.get(user_id=query.from_user.id)
            if user:
                user.activate()
            else:
                inviter = None
                full_name = f"{query.from_user.first_name}{f' {query.from_user.last_name}' if query.from_user.last_name else ''}".replace(
                        '<', '').replace('>', '')
                if data[0]:
                    inviter: User = User.get(user_id=data[0])
                    if inviter:
                        inviter.give_bonus(BONUS_FOR_NEW_USER)
                        try:
                            bot.send_message(
                                inviter.user_id,
                                bot.text.bonus_for_new_referral.format(
                                    user_id=query.from_user.id,
                                    full_name=full_name,
                                    bonus=BONUS_FOR_NEW_USER
                                )
                            )
                        except ApiException:
                            pass
                user: User = User.create(
                    user_id=query.from_user.id,
                    inviter=inviter,
                    full_name=full_name,
                )
            bot.delete_message(
                query.message.chat.id,
                query.message.message_id
            )
            go_to_main(user)
        else:
            bot.answer_callback_query(
                query.id,
                bot.text.not_yet,
                show_alert=True
            )
    else:
        user: User = User.get(user_id=query.from_user.id)
        if user:
            try:
                {
                    CALLBACK_SELECT_BOOK_FOR_INFO: select_book_for_info,
                    CALLBACK_SELECT_BOOK_FOR_EXERCISE: select_book_for_exercise,
                    CALLBACK_SELECT_THOUSAND_FOR_EXERCISE: select_thousand_for_exercise,
                    CALLBACK_SELECT_HUNDRED_FOR_EXERCISE: select_hundred_for_exercise,
                    CALLBACK_NEXT_EXERCISE: next_exercise,
                    CALLBACK_SELECT_BOOK_FOR_BATTLE: select_book_for_battle,
                    CALLBACK_SELECT_THOUSAND_FOR_BATTLE: select_thousand_for_battle,
                    CALLBACK_PROCESS_REQUEST_FOR_BATTLE: process_request_for_battle,
                    CALLBACK_START_BATTLE_WITH_RANDOM_OPPONENT: start_battle_with_random_opponent,
                    CALLBACK_NEXT_WORD: next_word,
                    CALLBACK_REQUEST_FOR_REVENGE: request_for_revenge,
                    CALLBACK_SELECT_PERIOD_FOR_RATING: select_period_for_rating,
                    CALLBACK_JOINING_TO_CHANNELS: joining_to_channels,
                    CALLBACK_SELECT_CHANNEL_TO_JOINING: select_channel_to_joining,
                    CALLBACK_PAYING_FOR_ENERGY: paying_for_energy,
                    CALLBACK_SELECT_PROVIDER: select_provider,
                    CALLBACK_SELECT_AMOUNT: select_amount,
                    CALLBACK_BACK_TO_SENDING: back_to_sending
                }[step](user, query, query.message, *data)
                bot.answer_callback_query(query.id)
            except ApiException as e:
                print(f"ApiException: {e.args}")
                bot.answer_callback_query(query.id)
            except KeyError as e:
                print(f"KeyError: {e.args}")
                bot.answer_callback_query(
                    query.id,
                    bot.text.soon,
                    show_alert=True
                )
        else:
            bot.answer_callback_query(
                query.id,
                f"{bot.text.not_member_title}\n\n{bot.text.not_member_description.format(bot_username=BOT_USERNAME)}",
                show_alert=True
            )


def select_book_for_info(user: User, query: CallbackQuery, message: Message, book_id):
    book: Book = Book.get(id=book_id)
    if book:
        inline_markup = InlineKeyboardMarkup()
        inline_markup.add(
            InlineKeyboardButton(
                bot.text.back,
                callback_data=f"{CALLBACK_BACK_TO_SENDING} {BACK_TO_BOOK_HANDLER}"
            )
        )
        bot.edit_message_text(
            bot.text.book_full_info.format(
                name=book.name,
                price=book.price,
                description=book.description
            ),
            message.chat.id,
            message.message_id,
            reply_markup=inline_markup,
        )


def select_book_for_exercise(user: User, query: CallbackQuery, message: Message, book_id):
    book: Book = Book.get(id=book_id)
    if book:
        inline_markup = InlineKeyboardMarkup(row_width=3)
        inline_markup.add(
            *[
                InlineKeyboardButton(
                    f"{thousand - 999} - {thousand}",
                    callback_data=f"{CALLBACK_SELECT_THOUSAND_FOR_EXERCISE} {book_id} {thousand}"
                ) for thousand in book.thousand
            ],
            InlineKeyboardButton(
                bot.text.back,
                callback_data=f"{CALLBACK_BACK_TO_SENDING} {BACK_TO_EXERCISES_HANDLER}"
            )
        )
        bot.edit_message_text(
            bot.text.select_thousand_for_exercise.format(
                name=book.name
            ),
            message.chat.id,
            message.message_id,
            reply_markup=inline_markup,
        )


def select_thousand_for_exercise(user: User, query: CallbackQuery, message: Message, book_id: int, thousand: int):
    book: Book = Book.get(id=book_id)
    if book:
        if not user.data:
            user.set_step()
        inline_markup = InlineKeyboardMarkup(row_width=3)
        inline_markup.add(
            *[
                InlineKeyboardButton(
                    f"{hundred - 99} - {hundred}",
                    callback_data=f"{CALLBACK_SELECT_HUNDRED_FOR_EXERCISE} {book_id} {thousand} {hundred}"
                ) for hundred in range(thousand - 900, thousand + 1, 100)
            ],
            InlineKeyboardButton(
                bot.text.back,
                callback_data=f"{CALLBACK_SELECT_BOOK_FOR_EXERCISE} {book_id}"
            )
        )
        bot.edit_message_text(
            bot.text.select_hundred_for_exercise.format(
                name=book.name
            ),
            message.chat.id,
            message.message_id,
            reply_markup=inline_markup,
        )


def select_hundred_for_exercise(user: User, query: CallbackQuery, message: Message, book_id: int, thousand: int, hundred: int):
    book: Book = Book.get(id=book_id)
    if book:
        exercises = book.get_random_ten_exercises(hundred)
        if exercises:
            user.set_step(STEP_TESTING_BY_QUIZ, f"{','.join([str(exercise.id) for exercise in exercises])}#")
            inline_markup = InlineKeyboardMarkup()
            inline_markup.add(
                InlineKeyboardButton(
                    bot.text.start_testing,
                    callback_data=f"{CALLBACK_NEXT_EXERCISE} {book_id} {thousand} {hundred}"
                ),
                InlineKeyboardButton(
                    bot.text.back,
                    callback_data=f"{CALLBACK_SELECT_THOUSAND_FOR_EXERCISE} {book_id} {thousand}"
                )
            )
            bot.edit_message_text(
                bot.text.do_you_start_exercise.format(
                    name=book.name,
                    first=hundred - 99,
                    last=hundred,
                    diamond=thousand//1000
                ),
                message.chat.id,
                message.message_id,
                reply_markup=inline_markup,
            )
        else:
            bot.answer_callback_query(
                query.id,
                bot.text.exercises_not_enough,
                show_alert=True
            )


def next_exercise(user: User, query: CallbackQuery, message: Message, book_id: int, thousand: int, hundred: int, answer=None, started_time=None, *args):
    if user.energy < 1:
        user.step = STEP_MAIN_MENU
        user.data = None
        user.save()
        inline_markup = InlineKeyboardMarkup()
        inline_markup.add(
            InlineKeyboardButton(
                bot.text.restart_testing,
                callback_data=f"{CALLBACK_SELECT_HUNDRED_FOR_EXERCISE} {book_id} {thousand} {hundred}"
            )
        )
        bot.edit_message_text(
            bot.text.energy_is_not_enough_for_exercise,
            message.chat.id,
            message.message_id,
            reply_markup=inline_markup
        )
        return
    if user.step == STEP_TESTING_BY_QUIZ and user.data:
        exercise_ids, answers = [string.split(',') if string != '' else [] for string in user.data.split('#')]
        if exercise_ids:
            if answer is not None:
                answers.append(str(answer))
                if len(exercise_ids) == len(answers):
                    exercises = [Exercise.get(id=exercise_id) for exercise_id in exercise_ids]
                    answers = list(map(int, answers))
                    energy = sum(answers)
                    exercise: Exercise = Exercise.get(id=exercise_ids[-1])
                    inline_markup = InlineKeyboardMarkup()
                    inline_markup.add(
                        InlineKeyboardButton(
                            bot.text.restart_testing,
                            callback_data=f"{CALLBACK_SELECT_HUNDRED_FOR_EXERCISE} {book_id} {thousand} {hundred}"
                        )
                    )
                    text = bot.text.exercise_end.format(
                        name=exercises[0].word.book.name,
                        answers="\n\n".join([f"{'✅' if answers[ind] else '❌'} <b>{exercise.question}</b>\nTo'gri javob: <i>{exercise.true_answer}</i>" for ind, exercise in enumerate(exercises)]),
                    )
                    if energy == len(exercises):
                        text += f"\n\nSizga ushbu mashq uchun <b>{thousand//1000 + 1} 💎</b> taqdim etildi."
                    text += f"\n\nTo'g'ri javoblar: <b>{energy} ta</b>"
                    bot.edit_message_text(
                        text,
                        message.chat.id,
                        message.message_id,
                        reply_markup=inline_markup,
                    )
                    if energy == 10:
                        exercise_time = (timezone.now() - timezone.datetime.fromtimestamp(started_time)).total_seconds()
                        if exercise_time <= 60:
                            training: Training = Training.get(user=user, book__id=book_id, thousand=thousand, hundred=hundred)
                            if not training:
                                Training.create(
                                    user=user,
                                    book=Book.get(id=book_id),
                                    thousand=thousand,
                                    hundred=hundred
                                )
                                user.pocket.increase(thousand//1000 + 1)
                    user.step = STEP_MAIN_MENU
                    user.data = None
                    user.save()
                    return
                user.set_step(STEP_TESTING_BY_QUIZ, f"{','.join(exercise_ids)}#{','.join(answers)}")
            else:
                started_time = int(timezone.now().timestamp())
                user.energy -= 1
                user.save()
            current_exercise_id = exercise_ids[len(answers)]
            index = len(answers) + 1
            exercise: Exercise = Exercise.get(id=current_exercise_id)
            inline_markup = InlineKeyboardMarkup(row_width=2)
            inline_markup.add(
                *[
                    InlineKeyboardButton(
                        option,
                        callback_data=f"{CALLBACK_NEXT_EXERCISE} {book_id} {thousand} {hundred} {1 if option == exercise.true_answer else 0} {started_time} {ind}"
                    ) for ind, option in enumerate(exercise.options)
                ]
            )
            bot.edit_message_text(
                f"{index}) <b>{exercise.question}</b>",
                message.chat.id,
                message.message_id,
                reply_markup=inline_markup,

            )
            return
    bot.delete_message(
        message.chat.id,
        message.message_id
    )
    bot.answer_callback_query(
        query.id,
        bot.text.you_broke_process,
        show_alert=True
    )


def select_book_for_battle(user: User, query: CallbackQuery, message: Message, book_id):
    book: Book = Book.get(id=book_id)
    if book:
        inline_markup = InlineKeyboardMarkup(row_width=1)
        inline_markup.add(
            *[
                InlineKeyboardButton(
                    f"{thousand - 999} - {thousand}",
                    callback_data=f"{CALLBACK_SELECT_THOUSAND_FOR_BATTLE} {book_id} {thousand}"
                ) for thousand in book.thousand
            ],
            InlineKeyboardButton(
                bot.text.back,
                callback_data=f"{CALLBACK_BACK_TO_SENDING} {BACK_TO_BATTLE_HANDLER}"
            )
        )
        bot.edit_message_text(
            bot.text.select_thousand_for_battle.format(
                name=book.name
            ),
            message.chat.id,
            message.message_id,
            reply_markup=inline_markup,
        )


def select_thousand_for_battle(user: User, query: CallbackQuery, message: Message, book_id: int, thousand: int):
    book: Book = Book.get(id=book_id)
    if book:
        inline_markup = InlineKeyboardMarkup(row_width=1)
        inline_markup.add(
            InlineKeyboardButton(
                bot.text.share_with_friend,
                switch_inline_query=f"{book_id} {thousand}"
            ),
            InlineKeyboardButton(
                bot.text.with_random_opponent,
                callback_data=f"{CALLBACK_START_BATTLE_WITH_RANDOM_OPPONENT} {book_id} {thousand}"
            ),
            InlineKeyboardButton(
                bot.text.back,
                callback_data=f"{CALLBACK_SELECT_BOOK_FOR_BATTLE} {book_id}"
            )
        )
        bot.edit_message_text(
            bot.text.start_battle_with_friend_or_random_opponent.format(
                name=book.name,
                first=thousand-999,
                last=thousand
            ),
            message.chat.id,
            message.message_id,
            reply_markup=inline_markup,
        )


def process_request_for_battle(user: User, query: CallbackQuery, message: Message, answer: int, opponent_id: int, book_id: int, thousand: int, revenge=None):
    if user.id != opponent_id:
        book: Book = Book.get(id=book_id)
        opponent: User = User.get(id=opponent_id)
        if book:
            ids = {}
            if query.inline_message_id:
                ids['inline_message_id'] = query.inline_message_id
            else:
                ids['chat_id'] = message.chat.id
                ids['message_id'] = message.message_id
            if answer:
                bot.edit_message_text(
                    bot.text.request_accepted.format(
                        user_id=user.user_id,
                        full_name=user.full_name,
                        bot_username=BOT_USERNAME,
                    ),
                    **ids
                )
                battle = Battle.create(
                    book=book,
                    thousand=thousand,
                    with_friend=True if not revenge else False,
                    quizzes=','.join(str(word.id) for word in book.get_random_ten_words(thousand))
                )
                participant: Participant = Participant.create(
                    battle=battle,
                    participant=user
                )
                opponent: Participant = Participant.create(
                    battle=battle,
                    participant=opponent
                )
                for participant in battle.participants.all():
                    text = bot.text.start_battle_now.format(
                        name=book.name,
                        first=thousand - 999,
                        last=thousand
                    )
                    inline_markup = InlineKeyboardMarkup()
                    inline_markup.add(
                        InlineKeyboardButton(
                            bot.text.start_battle,
                            callback_data=f"{CALLBACK_NEXT_WORD} {participant.id}"
                        )
                    )
                    bot.send_message(
                        participant.participant.user_id,
                        text,
                        reply_markup=inline_markup,

                    )
            else:
                bot.edit_message_text(
                    bot.text.request_rejected.format(
                        user_id=user.user_id,
                        full_name=user.full_name
                    ),
                    **ids
                )
                try:
                    bot.send_message(
                        opponent.user_id,
                        bot.text.your_request_rejected.format(
                            user_id=user.user_id,
                            full_name=user.full_name,
                            name=book.name,
                            first=thousand - 999,
                            last=thousand
                        ),

                    )
                except ApiException as e:
                    print(f"{opponent_id}: {e.args}")


def start_battle_with_random_opponent(user: User, query: CallbackQuery, message: Message, book_id: int, thousand: int):
    book: Book = Book.get(id=book_id)
    if book:
        if user.energy >= 1:
            user.give_bonus(-1)
            battle: Battle = Battle.filter(~Q(participants__participant=user), book__id=book_id, thousand=thousand, found=False, with_friend=False, finished=False).first()
            if battle:
                battle.found = True
                battle.save()
            else:
                battle = Battle.create(
                    book=book,
                    thousand=thousand,
                    quizzes=','.join(str(word.id) for word in book.get_random_ten_words(thousand))
                )
            participant: Participant = Participant.create(
                battle=battle,
                participant=user
            )
            if battle.found:
                for participant in battle.participants.all():
                    text = bot.text.start_battle_now.format(
                        name=book.name,
                        first=thousand - 999,
                        last=thousand
                    )
                    inline_markup = InlineKeyboardMarkup()
                    inline_markup.add(
                        InlineKeyboardButton(
                            bot.text.start_battle,
                            callback_data=f"{CALLBACK_NEXT_WORD} {participant.id}"
                        )
                    )
                    if participant.participant == user:
                        bot.edit_message_text(
                            text,
                            message.chat.id,
                            message.message_id,
                            reply_markup=inline_markup,
                            parse_mode="html"
                        )
                    else:
                        bot.send_message(
                            participant.participant.user_id,
                            text,
                            reply_markup=inline_markup,
                        )
            else:
                bot.edit_message_text(
                    bot.text.finding_opponent.format(
                        name=book.name,
                        first=thousand - 999,
                        last=thousand
                    ),
                    message.chat.id,
                    message.message_id,

                )
        else:
            bot.answer_callback_query(
                query.id,
                bot.text.energy_is_not_enough.format(
                    energy=user.energy
                ),
                show_alert=True
            )


def next_word(user: User, query: CallbackQuery, message: Message, participant_id, answer=None, *args):
    participant: Participant = Participant.get(id=participant_id)
    if participant and not participant.battle.finished:
        word_ids = participant.battle.quizzes.split(',')
        answers = participant.answers.split(',') if participant.answers else []
        if answer is not None:
            answers.append(str(answer))
            participant.answers = ','.join(answers)
            participant.save()
            if len(word_ids) == len(answers):
                participant.end_time = timezone.now()
                participant.save()
                opponent: Participant = Participant.get(~Q(id=participant_id), battle=participant.battle)
                if opponent and opponent.end_time:
                    participant.battle.finished = True
                    participant.battle.save()
                    winner = participant
                    loser = opponent
                    if participant.true_answers < opponent.true_answers or (
                            participant.true_answers == opponent.true_answers and participant.battle_time > opponent.battle_time):
                        winner, loser = loser, winner
                    if not participant.battle.with_friend:
                        winner.participant.pocket.increase((int(word_ids[0])//1000) + 1)
                    text = bot.text.battle_result.format(
                        name=participant.battle.book.name,
                        first=participant.battle.thousand - 999,
                        last=participant.battle.thousand,
                        winner=winner.participant,
                        winner_answers=winner.true_answers,
                        winner_time=winner.battle_time,
                        loser=loser.participant,
                        loser_answers=loser.true_answers,
                        loser_time=loser.battle_time,
                        answers_and_words=participant.battle.answers_and_words,
                        result_time=timezone.now().strftime("%d.%m.%Y %H:%M:%S")
                    )
                    for participant in participant.battle.participants.all():
                        inline_markup = InlineKeyboardMarkup()
                        inline_markup.add(
                            InlineKeyboardButton(
                                bot.text.revenge,
                                callback_data=f"{CALLBACK_REQUEST_FOR_REVENGE} {participant.battle.id}"
                            )
                        )
                        try:
                            if participant.participant == user:
                                bot.edit_message_text(
                                    text,
                                    message.chat.id,
                                    message.message_id,
                                    reply_markup=inline_markup,
                                )
                            else:
                                bot.send_message(
                                    participant.participant.user_id,
                                    text,
                                    reply_markup=inline_markup,

                                )
                        except ApiException as e:
                            print(f"{participant.id}) {participant.participant}: {e.args}")
                else:
                    bot.edit_message_text(
                        bot.text.opponent_have_not_finish_yet,
                        message.chat.id,
                        message.message_id,
                    )
                return
        else:
            participant.started_time = timezone.now()
            participant.save()
        index = len(answers) + 1
        word: Word = Word.get(id=word_ids[len(answers)])
        if word:
            inline_markup = InlineKeyboardMarkup(row_width=1)
            inline_markup.add(
                *[
                    InlineKeyboardButton(
                        option,
                        callback_data=f"{CALLBACK_NEXT_WORD} {participant_id} {1 if option == word.word else 0} {ind}"
                    ) for ind, option in enumerate(word.options)
                ]
            )
            bot.edit_message_text(
                f"<b>{index}) {word.translation}</b>",
                message.chat.id,
                message.message_id,
                reply_markup=inline_markup,

            )
    else:
        participant.battle.finished = True
        participant.battle.save()
        if participant and not participant.answers:
            bot.edit_message_text(
                bot.text.you_are_late,
                message.chat.id,
                message.message_id,

            )
        else:
            bot.delete_message(
                message.chat.id,
                message.message_id
            )


def request_for_revenge(user: User, query: CallbackQuery, message: Message, battle_id: int):
    battle: Battle = Battle.get(id=battle_id)
    if battle:
        participant: Participant = battle.participants.filter(~Q(participant__id=user.id)).first()
        if participant:
            bot.edit_message_text(
                message.html_text,
                message.chat.id,
                message.message_id,

            )
            try:
                inline_markup = InlineKeyboardMarkup(row_width=1)
                inline_markup.add(
                    InlineKeyboardButton(
                        bot.text.accept_battle,
                        callback_data=f"{CALLBACK_PROCESS_REQUEST_FOR_BATTLE} 1 {user.id} {battle.book.id} {battle.thousand} 1"
                    ),
                    InlineKeyboardButton(
                        bot.text.reject_battle,
                        callback_data=f"{CALLBACK_PROCESS_REQUEST_FOR_BATTLE} 0 {user.id} {battle.book.id} {battle.thousand} 1"
                    )
                )
                bot.send_message(
                    participant.participant.user_id,
                    bot.text.revenge_request.format(
                        user_id=user.user_id,
                        full_name=user.full_name,
                        name=battle.book.name,
                        first=battle.thousand - 999,
                        last=battle.thousand
                    ),
                    reply_markup=inline_markup,

                )
                bot.answer_callback_query(
                    query.id,
                    bot.text.request_sent,
                    show_alert=True
                )
            except ApiException as e:
                print(f"{user.user_id}) {user}: {e.args}")


def select_period_for_rating(user: User, query: CallbackQuery, message: Message, period_id: int):
    key = lambda u: u.daily
    if period_id == 1:
        key = lambda u: u.weakly
    elif period_id == 2:
        key = lambda u: u.monthly
    elif period_id == 3:
        key = lambda u: u.yearly
    elif period_id == 4:
        key = lambda u: u.diamonds
    inline_markup = InlineKeyboardMarkup()
    inline_markup.add(
        *[
            InlineKeyboardButton(
                period,
                callback_data=f"{CALLBACK_SELECT_PERIOD_FOR_RATING} {index}"
            ) for index, period in enumerate(bot.text.stat_filter_by_time)
        ]
    )
    top = sorted(User.filter(is_banned=False, is_member=True), key=key, reverse=True)
    place = top.index(user)
    try:
        bot.edit_message_text(
            bot.text.rating.format(
                period=bot.text.stat_filter_by_time[period_id],
                top="\n".join(
                    [f"{bot.text.places[index]} {us.level} <b>{us}</b> - {[us.daily, us.weakly, us.monthly, us.yearly, us.diamonds][period_id]} 💎" for index, us in enumerate(top[:10])]),
                me=f"\n\n{place + 1}) {user.level} <b>{user}</b> - {[user.daily, user.weakly, user.monthly, user.yearly, user.diamonds][period_id]} 💎" if place >= 10 else ''
            ),
            message.chat.id,
            message.message_id,
            reply_markup=inline_markup,
        )
    except ApiException:
        pass


def joining_to_channels(user: User, query: CallbackQuery, message: Message):
    channels = Channel.filter(required=False, is_active=True)
    if channels:
        users_channels = list(user.channels.all())
        inline_markup = InlineKeyboardMarkup(row_width=1)
        inline_markup.add(
            *[
                InlineKeyboardButton(
                    f"✅ {channel.name} ✅" if channel in users_channels else channel.name,
                    callback_data=f"{CALLBACK_SELECT_CHANNEL_TO_JOINING} {channel.id} {1 if channel in users_channels else 0}"
                ) for channel in channels
            ],
            InlineKeyboardButton(
                bot.text.back,
                callback_data=f"{CALLBACK_BACK_TO_SENDING} {BACK_TO_EARN_HANDLER}"
            )
        )
        bot.edit_message_text(
            bot.text.joining_to_channels_info.format(
                bonus_for_joining_to_channel=BONUS_FOR_MEMBERSHIP_TO_CHANNEL,
                channels='\n'.join([f"{index + 1}) <a href='{channel.link}'>{channel.name}</a>" for index, channel in enumerate(channels)])
            ),
            message.chat.id,
            message.message_id,
            reply_markup=inline_markup,
            disable_web_page_preview=True
        )
    else:
        bot.answer_callback_query(
            query.id,
            bot.text.channels_not_found,
            show_alert=True
        )


def select_channel_to_joining(user: User, query: CallbackQuery, message: Message, channel_id: int, joined: int):
    if joined:
        bot.answer_callback_query(
            query.id,
            bot.text.already_joined,
            show_alert=True
        )
    else:
        channel: Channel = Channel.get(id=channel_id)
        if check_user_membership(user.user_id, [channel]):
            channel.members.add(user)
            channel.save()
            user.give_bonus(BONUS_FOR_MEMBERSHIP_TO_CHANNEL)
            bot.answer_callback_query(
                query.id,
                bot.text.you_are_get_bonus_for_joining_to_channel.format(
                    channel=channel.name,
                    bonus=BONUS_FOR_MEMBERSHIP_TO_CHANNEL
                ),
                show_alert=True
            )
            joining_to_channels(user, query, message)
        else:
            bot.answer_callback_query(
                query.id,
                bot.text.you_are_not_joined,
                show_alert=True
            )


def paying_for_energy(user: User, query: CallbackQuery, message: Message):
    inline_markup = InlineKeyboardMarkup()
    inline_markup.add(
        *[
            InlineKeyboardButton(
                provider.name,
                callback_data=f"{CALLBACK_SELECT_PROVIDER} {provider.id}"
            ) for provider in Provider.filter(is_active=True)
        ]
    )
    inline_markup.add(
        InlineKeyboardButton(
            bot.text.back,
            callback_data=f"{CALLBACK_BACK_TO_SENDING} {BACK_TO_EARN_HANDLER}"
        )
    )
    bot.edit_message_text(
        bot.text.select_provider,
        message.chat.id,
        message.message_id,
        reply_markup=inline_markup
    )


def select_provider(user: User, query: CallbackQuery, message: Message, provider_id: int):
    amounts = ENERGY_FOR_MONEY.keys()
    inline_markup = InlineKeyboardMarkup(row_width=2)
    inline_markup.add(
        *[
            InlineKeyboardButton(
                f"{amount:,} so'm",
                callback_data=f"{CALLBACK_SELECT_AMOUNT} {provider_id} {amount}"
            ) for amount in amounts
        ]
    )
    inline_markup.add(
        InlineKeyboardButton(
            bot.text.back,
            callback_data=f"{CALLBACK_PAYING_FOR_ENERGY}"
        )
    )
    bot.edit_message_text(
        bot.text.select_amount.format(
            tariffs='\n'.join([f"<b>{amount:,} so'm</b> - {energy} 🟡" for amount, energy in ENERGY_FOR_MONEY.items()])
        ),
        message.chat.id,
        message.message_id,
        reply_markup=inline_markup
    )


def select_amount(user: User, query: CallbackQuery, message: Message, provider_id: int, amount: int):
    provider: Provider = Provider.get(id=provider_id)
    bot.delete_message(
        message.chat.id,
        message.message_id
    )
    bot.send_invoice(
        message.chat.id,
        bot.text.pay_for_energy,
        bot.text.pay_for_energy_description.format(
            count=ENERGY_FOR_MONEY.get(amount),
            amount=amount,
        ),
        f"{provider.id}",
        provider.token,
        'uzs',
        [LabeledPrice(f"{ENERGY_FOR_MONEY.get(amount)} 🟡 uchun ", amount*100)],
        'nothing'
    )


def back_to_sending(user: User, query: CallbackQuery, message: Message, back_to: int):
    if back_to == BACK_TO_BOOK_HANDLER:
        inline_markup = InlineKeyboardMarkup(row_width=1)
        inline_markup.add(
            *[
                InlineKeyboardButton(
                    book.name,
                    callback_data=f"{CALLBACK_SELECT_BOOK_FOR_INFO} {book.id}"
                ) for book in Book.filter(is_active=True).order_by('order')
            ]
        )
        bot.edit_message_text(
            bot.text.select_book_for_info,
            message.chat.id,
            message.message_id,
            reply_markup=inline_markup,
        )
    elif back_to == BACK_TO_EXERCISES_HANDLER:
        inline_markup = InlineKeyboardMarkup(row_width=1)
        inline_markup.add(
            *[
                InlineKeyboardButton(
                    book.name,
                    callback_data=f"{CALLBACK_SELECT_BOOK_FOR_EXERCISE} {book.id}"
                ) for book in Book.filter(is_active=True)
            ]
        )
        bot.edit_message_text(
            bot.text.select_book_for_exercise,
            message.chat.id,
            message.message_id,
            reply_markup=inline_markup,
        )
    elif back_to == BACK_TO_BATTLE_HANDLER:
        inline_markup = InlineKeyboardMarkup(row_width=1)
        inline_markup.add(
            *[
                InlineKeyboardButton(
                    book.name,
                    callback_data=f"{CALLBACK_SELECT_BOOK_FOR_BATTLE} {book.id}"
                ) for book in Book.filter(is_active=True)
            ]
        )
        bot.edit_message_text(
            bot.text.select_book_for_battle,
            message.chat.id,
            message.message_id,
            reply_markup=inline_markup,
        )
    elif back_to == BACK_TO_EARN_HANDLER:
        inline_markup = InlineKeyboardMarkup(row_width=1)
        inline_markup.add(
            InlineKeyboardButton(
                bot.text.sharing_with_friends,
                switch_inline_query=""
            ),
            InlineKeyboardButton(
                bot.text.joining_to_channels,
                callback_data=f"{CALLBACK_JOINING_TO_CHANNELS}"
            ),
            InlineKeyboardButton(
                bot.text.pay_for_energy,
                callback_data=f"{CALLBACK_PAYING_FOR_ENERGY}"
            ),
            InlineKeyboardButton(
                bot.text.back,
                callback_data=f"{CALLBACK_BACK_TO_SENDING} -111"
            )
        )
        bot.edit_message_text(
            bot.text.earn_info.format(
                bonus_for_referral=BONUS_FOR_NEW_USER,
                bonus_for_joining_to_channel=BONUS_FOR_MEMBERSHIP_TO_CHANNEL,
                price_of_energy=PRICE_OF_ENERGY
            ),
            message.chat.id,
            message.message_id,
            reply_markup=inline_markup
        )
    else:
        bot.delete_message(
            message.chat.id,
            message.message_id,
        )
        go_to_main(user)
