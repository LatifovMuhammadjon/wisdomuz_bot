from .constants import LANGUAGE_UZ


class Text:
    def __init__(self, lang):
        self.lang = lang

        self.join_this_channels = {
            LANGUAGE_UZ: "Bizning botdan foydalanish uchun <b>Ko'rsatilgan kanallarimizga</b> a'zo bo'ling.\n\n<i>Sizni"
                         " ajoyib imkoniyatlar kutayapti 🤗</i> "
        }[self.lang]

        self.you_are_banned = {
            LANGUAGE_UZ: "Sizning ba'zi harakatlaringiz <b>tizim ma'murlari</b>ga yoqmagan ko'rinadi, siz <b>BAN</b> "
                         "holatidasiz.\n\n<i>Ko'proq ma'lumot uchun: {operator}</i>"
        }[self.lang]

        self.main_text = {
            LANGUAGE_UZ: "Kerakli bo'limni tanlang"
        }[self.lang]

        self.soon = {
            LANGUAGE_UZ: "Ushbu imkoniyat tayyor emas, biz uning ustida ishlayapmiz 🥵😓"
        }[self.lang]

        self.exercises_not_enough = {
            LANGUAGE_UZ: "Ushbu oraliqdagi so'zlar uchun yetarlicha mashqlar qo'shilmagan\n\nKeltirilgan noqulaylik "
                         "uchun uzr so'raymiz :( "
        }[self.lang]

        self.not_yet = {
            LANGUAGE_UZ: "Botdan to'liq foydalanish uchun Wisdom English kanaliga a'zo bo'lishingiz kerak."
        }[self.lang]

        self.select_book_for_info = {
            LANGUAGE_UZ: "Ma'lumot olish uchun quyida keltirilgan, kerakli <b>kitob</b>ni tanlang."
        }[self.lang]

        self.books_not_found = {
            LANGUAGE_UZ: "Hozirda tizimda bironta ham <b>kitob</b> topilmadi 😓"
        }[self.lang]

        self.book_full_info = {
            LANGUAGE_UZ: "Nomi: <b>{name}</b>\nNarxi: <b>{price:,} so'm</b>\n\n<i>{description}</i>"
        }[self.lang]

        self.select_book_for_exercise = {
            LANGUAGE_UZ: "<b>Mashq qilmoqchimisiz ?</b>\n\nQuyida keltirilgan <b>kitob</b>lardan o'zingizga "
                         "keraklisini tanlang. "
        }[self.lang]

        self.select_thousand_for_exercise = {
            LANGUAGE_UZ: "Siz tanlagan <b>{name}</b> kitobidagi mavjud so'zlarning qaysi <b>minglik</b> oralig'i "
                         "bo'yicha mashq ishlamoqchisiz ? "
        }[self.lang]

        self.select_hundred_for_exercise = {
            LANGUAGE_UZ: "Siz tanlagan <b>{name}</b> kitobidagi mavjud so'zlarning qaysi <b>yuzlik</b> oralig'i "
                         "bo'yicha mashq ishlamoqchisiz ? "
        }[self.lang]

        self.do_you_start_exercise = {
            LANGUAGE_UZ: "Sizga <b>{name}</b> kitobining <b>{first}-{last}</b> oralig'idan tasodifiy 10 ta savol "
                         "tanlab olindi.\n\nSiz ushbu savollarga 60 soniya ichida to'liq javob bersangiz <b>faqat bir "
                         "marta</b> sizga <b>{diamond} 💎</b> taqdim etiladi.\n\n<i>Savollarga aniq javob berish "
                         "uchun kitoblarni yaxshilab o'qib o'rganing</i>\n\n<b>Mashqni boshlaysizmi ?</b> "
        }[self.lang]

        self.you_broke_process = {
            LANGUAGE_UZ: "Siz mashq boshlash jarayonida boshqa amalni boshlagansiz bu esa ketma-ketlikning "
                         "buzilishiga olib kelgan, qaytadan boshlashga urinib ko'ring. "
        }[self.lang]

        self.exercise_end = {
            LANGUAGE_UZ: "<b>{name}</b> kitobi yuzasidan o'tkazilgan mashq yakunlandi.\n\n{answers}"
        }[self.lang]

        self.select_book_for_battle = {
            LANGUAGE_UZ: "<b>Juda yaxshi, bellashishni istaysizmi ?</b>\n\nQuyida bellashuvni qaysi <b>kitob</b> "
                         "bo'yicha amalga oshirishni tanlang. "
        }[self.lang]

        self.select_thousand_for_battle = {
            LANGUAGE_UZ: "Siz tanlagan <b>{name}</b> kitobidagi mavjud so'zlarning qaysi minglik oralig'i bo'yicha "
                         "bellashishni istaysiz ? "
        }[self.lang]

        self.start_battle_with_friend_or_random_opponent = {
            LANGUAGE_UZ: "<b>{name}</b> kitobiga tegishli <b>{first} - {last}</b> oraliqdagi so'zlar bo'yicha "
                         "bellashuvni kim bilan olib bormoqchisiz ? "
        }[self.lang]

        self.energy_is_not_enough = {
            LANGUAGE_UZ: "Bellashuvni boshlash uchun sizda kamida <b>1 🟡</b> bo'lishi kerak, hozirda sizda {energy} 🟡 "
                         "mavjud, 🟡 larni yangi do'stlarni chaqirib, homiy kanallarga a'zo bo'llib va to'lov orqali "
                         "qo'lga kiritishingiz mumkin."
        }[self.lang]

        self.energy_is_not_enough_for_exercise = {
            LANGUAGE_UZ: "Mashq qilish uchun sizda kamida <b>1 🟡</b> bo'lishi kerak, 🟡 larni yangi do'stlarni "
                         "chaqirib, homiy kanallarga a'zo bo'llib va to'lov orqali qo'lga kiritishingiz mumkin."
        }[self.lang]

        self.energy_is_not_enough_for_vocabulary_test = {
            LANGUAGE_UZ: "Qancha so'z bilishingizni tekshirish uchun sizda kamida <b>1 🟡</b> bo'lishi kerak, "
                         "🟡 larni yangi do'stlarni chaqirib, homiy kanallarga a'zo bo'llib va to'lov orqali qo'lga "
                         "kiritishingiz mumkin. "
        }[self.lang]

        self.finding_opponent = {
            LANGUAGE_UZ: "<b>{name}</b> kitobining <b>{first} - {last}</b> oralig'idagi so'zlar bo'yicha bellashuv "
                         "uchun raqib qidirilyapti...\n\n<i>Eng birinchi talabgor bilan bellashasiz</i>"
        }[self.lang]

        self.start_battle_now = {
            LANGUAGE_UZ: "<b>{name}</b> kitobining <b>{first} - {last}</b> oralig'idagi so'zlar bo'yicha bellashuv "
                         "uchun raqib topildi.\n\n<i>Raqibingizni 15 daqiqadan ko'p kuttirmang aks holda tizim uni "
                         "avtomatik g'olib deb e'lon qiladi.</i>\n\n<b>Bellashuvni boshlash uchun quyidagi tugmadan "
                         "foydalaning</b>"
        }[self.lang]

        self.you_are_late = {
            LANGUAGE_UZ: "Sizni ogohlantirgan edim, bellashuvni boshlab qo'yib uni <b>15 daqiqa</b> ichida "
                         "tugatmaganingiz sababli sizni bellashuvda mag'lub bo'ldi deb hisoblaymiz.\n\n<i>Ko'ngilni "
                         "cho'ktirmang va hamma narsani o'z vaqtida bajarishga harakt qiling.</i>"
        }[self.lang]

        self.opponent_are_late = {
            LANGUAGE_UZ: "Raqibingiz belgilangan vaqtda bellashuvni yakunlamaganligi sababli sizni <b>bellashuv "
                         "g'olibi</b> deb e'lon qilamiz va sizga <b>1 💎</b> taqdim "
                         "etamiz.\n\nBilim olishda charchamang. "
        }[self.lang]

        self.opponent_have_not_finish_yet = {
            LANGUAGE_UZ: "Hozircha raqibingiz bellashuvni <b>yakunlagani yo'q</b>, u barcha savollarga javob berishi "
                         "bilan natijalarni hisoblab sizga xabar beraman.\n\n<i>Ozroq sabr qiling, boshqa bellashuvda "
                         "qatnashishingiz ham mumkin.</i> "
        }[self.lang]

        self.battle_result = {
            LANGUAGE_UZ: "<b>{name}</b> <u>{first}-{last}</u> bo'yicha o'tkazilgan bellashuv yakunlandi, natijalar "
                         "quyidagicha\n\n👑 {winner}: {winner_answers}/10 <b>{winner_time} sekund</b>\n😭 {loser}: {"
                         "loser_answers}/10 <b>{loser_time} sekund</b>\n\n👑 | 😭 | so'zlar\n{"
                         "answers_and_words}\n\n<i>⏰ {result_time}</i> "
        }[self.lang]

        self.revenge_request = {
            LANGUAGE_UZ: "Sizni <a href='tg://user?id={user_id}'>{full_name}</a> foydalanuvchi <b>{name}</b> kitobi "
                         "<b>{first}-{last}</b> oralig'idagi so'zlar bo'yicha o'tkazilgan bellashuvdan so'ng "
                         "<b>revansh bahsiga</b> chaqiryapti. "
        }[self.lang]

        self.request_sent = {
            LANGUAGE_UZ: "Raqibga revansh bellashuvi uchun so'rov yuborildi\n\nU taklifni qabul qilsa yoki rad etsa "
                         "biz sizga bu haqida xabar beramiz. "
        }[self.lang]

        self.daily_result = {
            LANGUAGE_UZ: "<b>{date} | Bugungi bellashuvlar natijalari</b>\n\n{top}\n\nUyushtirilgan barcha "
                         "bellashuvlar: <b>{battles} ta</b>\n\n🤖 @{bot_username} "
        }[self.lang]

        self.bonus_for_new_referral = {
            LANGUAGE_UZ: "Sizga <a href='tg://user?id={user_id}'>{full_name}</a> do'stingizni taklif qilganingiz "
                         "uchun <b>{bonus} 🟡</b> taqdim etildi. "
        }[self.lang]

        self.successful_payment_info = {
            LANGUAGE_UZ: "Sizning hisobingiz <b>{amount:,} so'm</b>ga to'ldirildi.\n\nTo'lov ma'lumotlari:\n🔸 ID: "
            "<b>{payment_id}</b>\n🔸 PID: <b>{provider_payment_charge_id}</b>\n🔹 To'lov provayderi: "
            "<b>{provider_name}</b>\n🔹 Miqdori: <b>{amount:,} so'm</b>\n⏰ To'lov vaqti: <i>{"
            "payed_time}</i>\n\n<b>Sizga ushbu to'lovingiz uchun {energy} 🟡 taqdim etildi</b>"
        }[self.lang]

        self.earn_info = {
            LANGUAGE_UZ: "<b>Mashq bajarish va bellashuvlarda qatnashish uchun 🟡 qolmadimi ?\nSiz 🟡 olish uchun "
                         "quyidagi 3 amaldan birini bajarishingiz mumkin.</b>\n\n<b>📣 Do'stlarni chaqirish</b> - "
                         "har bir chaqirgan do'stingiz uchun <b>{bonus_for_referral} 🟡</b> qo'lga kiriting.\n"
                         "<b>📢 Kanallarga a'zo bo'lish</b> - homiy kanallarga a'zo bo'ling va har bir a'zolik uchun "
                         "<b>{bonus_for_joining_to_channel} 🟡</b> oling.\n<b>🟡 sotib olish</b> - bitta 🟡ni <b>{"
                         "price_of_energy} so'm</b> dan sotib oling.\n\n<i>Kerakli amalni tanlang</i> "
        }[self.lang]

        self.channels_not_found = {
            LANGUAGE_UZ: "Hozircha bironta ham homiy kanal mavjud emas, homiy bo'lmoqchimisiz? biz bilan bog'laning."
        }[self.lang]

        self.joining_to_channels_info = {
            LANGUAGE_UZ: "Quyida keltirilgan kanallarga a'zo bo'ling va har bir a'zolik uchun <b>{"
                         "bonus_for_joining_to_channel} 🟡</b>ni qo'lga kiriting.\n\n{channels}"
        }[self.lang]

        self.already_joined = {
            LANGUAGE_UZ: "Siz ushbu kanalga allaqachon a'zo bo'lgansiz"
        }[self.lang]

        self.you_are_not_joined = {
            LANGUAGE_UZ: "Siz kanalga a'zo emassiz, iltimos kanalga a'zo bo'lib qayta urinib ko'ring"
        }[self.lang]

        self.you_are_get_bonus_for_joining_to_channel = {
            LANGUAGE_UZ: "Sizga {channel} kanaliga a'zo bo'lganingiz uchun {bonus} 🟡 taqdim etildi, tabriklaymiz."
        }[self.lang]

        self.select_provider = {
            LANGUAGE_UZ: "Quyida keltirilgan <b>to'lov operatorlari</b>dan birini tanlang."
        }[self.lang]

        self.select_amount = {
            LANGUAGE_UZ: "Qancha to'lov qilmoqchisiz?\n\n{tariffs}\n\n<i>Quyidagi miqdorlardan birini tanlang</i>"
        }[self.lang]

        self.pay_for_energy_description = {
            LANGUAGE_UZ: "{count} 🟡ni {amount:,} so'mga sotib olish uchun to'lovni amalga oshiring."
        }[self.lang]

        # self. = {
        #     LANGUAGE_UZ: ""
        # }[self.lang]

        self.share_with_friend_title = {
            LANGUAGE_UZ: "Bellashuvga taklif"
        }[self.lang]

        self.share_with_friend_description = {
            LANGUAGE_UZ: "Ushbu do'stingizni bellashuvga taklif qilish uchun unga ushbu xabarni yuboring."
        }[self.lang]

        self.share_with_friend_info = {
            LANGUAGE_UZ: "Salom, sizga <a href='tg://user?id={user_id}'>{full_name}</a> do'stingiz <b>{book_name}</b> "
                         "kitobi <i>{first}-{last}</i> oralig'idagi so'zlar bo'yicha bellashuv taklifini "
                         "yubordi.\n\n<i>Bellashuvni qabul qilish uchun quyidagi tugmani bosing</i> "
        }[self.lang]

        self.request_accepted = {
            LANGUAGE_UZ: "✅ <a href='tg://user?id={user_id}'>{full_name}</a> bellashuvga taklifni qabul "
                         "qildi.\n\n<i>Bellashuvni boshlash uchun @{bot_username} ga oʻting.</i> "
        }[self.lang]

        self.request_rejected = {
            LANGUAGE_UZ: "❌ <a href='tg://user?id={user_id}'>{full_name}</a> bellashuvga taklifni rad qildi."
        }[self.lang]

        self.sharing_with_friends = {
            LANGUAGE_UZ: "📣 Do'stlarni chaqirish"
        }[self.lang]

        self.sharing_with_friends_description = {
            LANGUAGE_UZ: "Do'stlaringizni chaqiring va bonus oling"
        }[self.lang]

        self.sharing_text = {
            LANGUAGE_UZ: "Salom do'stim, men so'z yodlash uchun juda ajoyib yordamchi topdim. Kel birga ko'proq so'z "
                         "o'rganamiz. Bu juda ham qiziqarli bo'ladi.\n\n<i>Bu yerda mashqlar va bellashuvlar bilan "
                         "umuman zerikmaysan.</i>\n\n<b>Qani ketdik <a href='https://t.me/{bot_username}?start={"
                         "user_id}'>@{bot_username}</a></b> "
        }[self.lang]

        self.left_title = {
            LANGUAGE_UZ: "Unaqa emasda endi :("
        }[self.lang]

        self.left_description = {
            LANGUAGE_UZ: "Siz bizning kanallardan chiqib ketibsiz"
        }[self.lang]

        self.not_member_title = {
            LANGUAGE_UZ: "Yangi so'zlarni o'rganishni istaysizmi ?"
        }[self.lang]

        self.not_member_description = {
            LANGUAGE_UZ: "Unda @{bot_username}ga kirib /start buyrug'ini yuboring"
        }[self.lang]

        self.for_not_registered_member = {
            LANGUAGE_UZ: "<b>Biz bilan o'rganish oson.</b>\n\nYangi so'zlar bo'yicha <b>mashqlar ishlang</b> yoki "
                         "<b>do'stlaringiz bilan bellashing</b> bularning barchasi bizda.\n\n<b>{bot_username}</b> "
        }[self.lang]

        self.your_request_rejected = {
            LANGUAGE_UZ: "<a href='tg://user?id={user_id}'>{full_name}</a> <b>{name}</b> kitobi <i>{first}-{last}</i> "
                         "oraliqdagi so'zlar bo'yicha bellashuv uchun yuborgan so'rovingizni rad etdi."
        }[self.lang]

        self.rating = {
            LANGUAGE_UZ: "<b>{period}</b> reyting\n\n{top}{me}"
        }[self.lang]

        self.info = {
            LANGUAGE_UZ: "Taxallus: <b>{level} {full_name}</b>\n\nHisobingizda jami <b>{energy} 🟡</b> va <b>{"
                         "diamonds} 💎</b> bor. "
        }[self.lang]

        self.guide = {
            LANGUAGE_UZ: "Botdan <b>foydalanish</b> va biz haqimizda <b>to'liq ma'lumot</b> olish uchun <a href='{"
                         "link}'>ushbu maqola</a>ni o'qib chiqishni tavsiya qilamiz. "
        }[self.lang]

        self.vocabulary_info = {
            LANGUAGE_UZ: "Nechta so'z bilishingizni aniqlamoqchimisiz ?\n\n<b>Sizga bizning kitoblaramizdagi "
                         "so'zlardan 20 ta savol taqdim etiladi, siz ushbu savollarga qanchalik to'g'ri javob "
                         "berishingizga qarab nechta so'z bilishingizni aniqlab beramiz.</b>\n\n<b>Bir marta "
                         "urinish uchun 1 🟡 talab etiladi.</b>\n\n<i>Savollarga javob "
                         "berishni boshlash uchun quyidagi tugmadan foydalaning.</i> "
        }[self.lang]

        self.vocabulary_test_result = {
            LANGUAGE_UZ: "Siz berilgan <b>{count_of_words} ta</b> so'zdan <b>{true_answers_count} ta</b>siga to'g'ri "
                         "javob berdingiz, siz hozirda <b>{thousand}</b> ga yaqin so'z bilasiz.\n\n<b>Bu natijani "
                         "yaxshilamoqchi bo'lsangiz quyidagi tugmadan foydalanib javob berishni qayta boshlashingiz "
                         "mumkin.</b>\n\n<b>Bir marta urinish uchun 1 🟡 talab etiladi.</b>"
        }[self.lang]

        self.stat_filter_by_time = {
            LANGUAGE_UZ: [
                "Kunlik",
                "Haftalik",
                "Oylik",
                "Yillik",
                "Umumiy"
            ]
        }[self.lang]

        self.main_markup = {
            LANGUAGE_UZ: [
                [
                    "🤓 Mashqlar",
                    "⚔️ Bellashuv",
                ],
                [
                    "🟡 Tanga olish",
                    "📚 Kitoblar",
                ],
                [
                    "📊 Reyting",
                    "🎯 Nechta so'z bilasiz ?"
                ],
                [
                    "ℹ️ Ma'lumotlarim",
                    "❓ Qo'llanma"
                ]
            ]
        }[self.lang]

        self.back = {
            LANGUAGE_UZ: "🔙 Orqaga"
        }[self.lang]

        self.next = {
            LANGUAGE_UZ: "🔜 Keyingi"
        }[self.lang]

        self.finish = {
            LANGUAGE_UZ: "🥳 Yakunlash"
        }[self.lang]

        self.confirm = {
            LANGUAGE_UZ: "✅ a'zo bo'ldim"
        }[self.lang]

        self.repeat = {
            LANGUAGE_UZ: "🔄 Takrorlash"
        }[self.lang]

        self.start_learning = {
            LANGUAGE_UZ: "🏁 Yodlash"
        }[self.lang]

        self.start_testing = {
            LANGUAGE_UZ: "🤓 Mashqni boshlash"
        }[self.lang]

        self.restart_testing = {
            LANGUAGE_UZ: "🔄 Mashqni qayta boshlash"
        }[self.lang]

        self.listen_pronunciation = {
            LANGUAGE_UZ: "🙉 Eshitish"
        }[self.lang]

        self.see_info = {
            LANGUAGE_UZ: "🙈 Qarab olish"
        }[self.lang]

        self.delete_this_message = {
            LANGUAGE_UZ: "🗑 Xabarni o'chirish"
        }[self.lang]

        self.change_first_name = {
            LANGUAGE_UZ: "🔂 Taxallus"
        }[self.lang]

        self.change_region = {
            LANGUAGE_UZ: "🗺 Hudud"
        }[self.lang]

        self.yes = {
            LANGUAGE_UZ: "✅ Ha"
        }[self.lang]

        self.later = {
            LANGUAGE_UZ: "😐 Keyinroq"
        }[self.lang]

        self.new_battle = {
            LANGUAGE_UZ: "⚔️ Yangi bellashuv"
        }[self.lang]

        self.history_of_battles = {
            LANGUAGE_UZ: "📜 Bellashuvlar tarixi"
        }[self.lang]

        self.share_with_friend = {
            LANGUAGE_UZ: "✊ Do'stim bilan"
        }[self.lang]

        self.with_random_opponent = {
            LANGUAGE_UZ: "😑 Tasodifiy raqib bilan"
        }[self.lang]

        self.start_using_bot = {
            LANGUAGE_UZ: "🏁 Foydalanishni boshlash"
        }[self.lang]

        self.accept_battle = {
            LANGUAGE_UZ: "🤝 Bellashuvga rozi bo'lish"
        }[self.lang]

        self.reject_battle = {
            LANGUAGE_UZ: "🙅‍♂️ Bellashuvni rad qilish"
        }[self.lang]

        self.start_battle = {
            LANGUAGE_UZ: "👊 Bellashuvni boshlash"
        }[self.lang]

        self.other_exercises = {
            LANGUAGE_UZ: "🌐 Boshqa mashqlar"
        }[self.lang]

        self.revenge = {
            LANGUAGE_UZ: "👊 Revansh"
        }[self.lang]

        self.places = {
            LANGUAGE_UZ: ['🥇)', '🥈)', '🥉)', ' 4 )', ' 5 )', ' 6 )', ' 7 )', ' 8 )', ' 9 )', ' 10)']
        }[self.lang]

        self.do_pro = {
            LANGUAGE_UZ: "👑 PRO darajasini berish"
        }[self.lang]

        self.report_about_incorrect_info = {
            LANGUAGE_UZ: "❓ Xatolik haqida xabar berish"
        }[self.lang]

        self.invite_friend = {
            LANGUAGE_UZ: "👥 Do'stni taklif qilish"
        }[self.lang]

        self.joining_to_channels = {
            LANGUAGE_UZ: "📢 Kanallarga a'zo bo'lish"
        }[self.lang]

        self.pay_for_energy = {
            LANGUAGE_UZ: "🟡 sotib olish"
        }[self.lang]

        self.start_vocabulary_test = {
            LANGUAGE_UZ: "🏁 Javob berishni boshlash"
        }[self.lang]

        # self. = {
        #     LANGUAGE_UZ: ""
        # }[self.lang]
