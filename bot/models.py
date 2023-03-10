from django.db.models import Model, PositiveIntegerField, CharField, PositiveSmallIntegerField, DateTimeField, DateField, \
    ForeignKey, ManyToManyField, TextField, BooleanField, IntegerField, CASCADE, SET_NULL, Count,BigIntegerField
from django.utils import timezone
from django.db.models import Sum
from random import shuffle, randint, choice

from .constants import TOKEN, STEP_MAIN_MENU, BONUS_FOR_MEMBERSHIP_TO_CHANNEL, BONUS_FOR_NEW_USER, MESSAGE


class AbstractModel(Model):
    created_time = DateTimeField(default=timezone.now)

    @classmethod
    def create(cls, **kwargs):
        try:
            obj = cls(
                **kwargs
            )
            obj.save()
            return obj
        except Exception as e:
            print(e.args)
            return None

    @classmethod
    def filter(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs)

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            return cls.objects.get(*args, **kwargs)
        except Exception:
            return cls.filter(*args, **kwargs).first()

    @classmethod
    def all(cls):
        return cls.objects.all()

    def get_created_time(self):
        return self.created_time.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        abstract = True


class User(AbstractModel):
    user_id = BigIntegerField(
        unique=True,
        verbose_name="Foydalanuvchi IDsi"
    )
    inviter = ForeignKey(
        'self',
        SET_NULL,
        related_name="friends",
        verbose_name="Taklif etuvchi",
        null=True,
        blank=True
    )
    full_name = CharField(
        max_length=255,
        verbose_name="To'liq ismi"
    )
    energy = IntegerField(
        verbose_name="🟡",
        default=6
    )
    step = PositiveSmallIntegerField(
        null=True
    )
    data = TextField(
        null=True
    )
    is_member = BooleanField(
        verbose_name="Kanalga a'zo",
        default=True
    )
    is_banned = BooleanField(
        verbose_name="Bloklangan",
        default=False
    )

    def __str__(self):
        return self.full_name

    def set_step(self, step=STEP_MAIN_MENU, data=None):
        self.step = step
        self.data = data
        self.save()

    def activate(self):
        self.is_member = True
        self.save()

    def deactivate(self):
        self.is_member = False
        self.save()

    def give_bonus(self, amount):
        self.energy += amount
        self.save()

    @classmethod
    def get_rating(cls,period_id=0):
        now = timezone.now()
        top = []
        if period_id == 4:
            result = Pocket.objects.values("user_id").annotate(dcount=Sum("diamonds")).order_by("-dcount")[:10]
        elif period_id == 1:
            result=Pocket.objects.values("user_id").filter(date__gte=now-timezone.timedelta(days=now.weekday())).annotate(dcount=Sum("diamonds")).order_by("-dcount")[:10]
        elif period_id == 2:
            result=Pocket.objects.values("user_id").filter(date__year=now.year, date__month=now.month).annotate(dcount=Sum("diamonds")).order_by("-dcount")[:10]
        elif period_id == 3:
            result=Pocket.objects.values("user_id").filter(date__year=timezone.now().year).annotate(dcount=Sum("diamonds")).order_by("-dcount")[:10]
        else:
            result=Pocket.objects.values("user_id").filter(date__lte=now, date__gte=now).annotate(dcount=Sum("diamonds")).order_by("-dcount")[:10]

        result = [ i for i in result ]
        # if len(result) < 10:
        #     users = User.objects.all()[:10]
        #     while len(result) < 10:
        #         result.
        return result[:10]

        
        
    @property
    def pocket(self):
        pocket: Pocket = Pocket.get(user=self, date=timezone.now())
        if not pocket:
            pocket: Pocket = Pocket.create(
                user=self
            )
        return pocket

    @property
    def diamonds(self):
        return sum([pocket.diamonds for pocket in self.pockets.all()])

    @property
    def daily(self):
        return self.pocket.diamonds

    @property
    def weakly(self):
        now = timezone.now()
        return sum([pocket.diamonds for pocket in self.pockets.filter(date__gte=now-timezone.timedelta(days=now.weekday()))])

    @property
    def monthly(self):
        now = timezone.now()
        return sum([pocket.diamonds for pocket in self.pockets.filter(date__year=now.year, date__month=now.month)])

    @property
    def yearly(self):
        return sum([pocket.diamonds for pocket in self.pockets.filter(date__year=timezone.now().year)])

    @property
    def level(self):
        diamonds = self.diamonds
        return {
            diamonds < 100: "🐵",
            99 < diamonds < 500: "🐰",
            499 < diamonds < 1000: "🐭",
            999 < diamonds < 5000: "🐱",
            4999 < diamonds < 10000: "🐶",
            9999 < diamonds < 50000: "🦉",
            49999 < diamonds < 100000: "🦅",
            99999 < diamonds < 500000: "🦊",
            499999 < diamonds < 1000000: "🐨",
            999999 < diamonds < 5000000: "🐼",
            4999999 < diamonds < 10000000: "🐻",
            9999999 < diamonds < 50000000: "🐯",
            49999999 < diamonds: "🦁",
        }[True]

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"


class Pocket(AbstractModel):
    user = ForeignKey(
        User,
        verbose_name="Foydalanuvchi",
        related_name="pockets",
        on_delete=CASCADE
    )
    diamonds = PositiveSmallIntegerField(
        verbose_name="Brilliantlar miqdori",
        default=0
    )
    date = DateField(
        verbose_name="Sana",
        default=timezone.now
    )

    def __str__(self):
        return f"{self.user}: {self.diamonds} 💎"

    def increase(self, amount):
        self.diamonds += amount
        self.save()

    class Meta:
        verbose_name = "Xamyon"
        verbose_name_plural = "Xamyonlar"


class Book(AbstractModel):
    name = CharField(
        max_length=32,
        verbose_name="Nomi"
    )
    price = PositiveIntegerField(
        verbose_name="Narxi"
    )
    order = PositiveSmallIntegerField(
        verbose_name="Tartib raqami"
    )
    first = PositiveSmallIntegerField(
        verbose_name="Biriktirilgan birinchi so'z tartib raqami"
    )
    last = PositiveSmallIntegerField(
        verbose_name="Biriktirilgan oxirgi so'z tartib raqami"
    )
    description = TextField(
        verbose_name="Daraja haqida ma'lumot"
    )
    is_active = BooleanField(
        verbose_name="Aktiv",
        default=False
    )

    def __str__(self):
        return f"{self.order}) {self.name}"

    def get_random_ten_exercises(self, hundred: int):
        exercises = [exercise for word in self.words.filter(id__gte=hundred - 99, id__lte=hundred) for exercise in word.exercises.all()]
        shuffle(exercises)
        return exercises[:10]

    def get_random_ten_words(self, thousand: int):
        words = list(self.words.filter(id__gte=thousand - 999, id__lte=thousand))
        shuffle(words)
        return words[:10]

    @property
    def thousand(self):
        return [i*1000 + 1000 for i in range(self.first//1000, self.last//1000)]

    class Meta:
        verbose_name = "Kitob"
        verbose_name_plural = "Kitoblar"


class Word(AbstractModel):
    id = PositiveIntegerField(
        verbose_name="Tartib raqami",
        primary_key=True,
        unique=True,
    )
    book = ForeignKey(
        Book,
        verbose_name="Kitob",
        related_name="words",
        on_delete=SET_NULL,
        null=True
    )
    word = CharField(
        max_length=128,
        verbose_name="So'z"
    )
    translation = CharField(
        max_length=512,
        verbose_name="Tarjima"
    )
    variants = TextField(
        verbose_name="Variantlar",
        help_text="Variantlarni vergul(,) bilan ajratib yozing"
    )

    def __str__(self):
        return f"{self.word} - {self.translation}"

    @property
    def options(self):
        _ = [self.word, *self.variants.split(',')]
        shuffle(_)
        return _

    class Meta:
        verbose_name = "So'z"
        verbose_name_plural = "So'zlar"


class Exercise(AbstractModel):
    word = ForeignKey(
        Word,
        verbose_name="So'z",
        related_name="exercises",
        on_delete=SET_NULL,
        null=True,
        blank=True
    )
    question = TextField(
        verbose_name="Savol",
        help_text="Yangi qatorlarni qanday kiritsangiz shunday ko'rinadi"
    )
    answer = CharField(
        max_length=100,
        verbose_name="To'g'ri javob",
        null=True,
        blank=True
    )
    variants = TextField(
        verbose_name="Variantlar",
        help_text="Variantlarni vergul(,) bilan ajratib yozing",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.question

    @property
    def true_answer(self):
        return self.answer if self.answer else self.word.word

    @property
    def options(self):
        answer = self.answer if self.answer else self.word.word
        variants = self.variants if self.variants else self.word.variants
        options = [answer, *variants.split(',')]
        shuffle(options)
        return options

    class Meta:
        verbose_name = "Mashq"
        verbose_name_plural = "Mashqlar"


class Battle(AbstractModel):
    book = ForeignKey(
        Book,
        verbose_name="Kitob",
        related_name="battles",
        on_delete=CASCADE
    )
    thousand = PositiveSmallIntegerField(
        verbose_name="Tanlangan minglik"
    )
    quizzes = TextField(
        verbose_name="Tanlangan savollar tartib raqamlari"
    )
    found = BooleanField(
        verbose_name="Raqib topilgan",
        default=False
    )
    with_friend = BooleanField(
        default=False,
        verbose_name="Do'st bilan"
    )
    finished = BooleanField(
        verbose_name="Bellashuv yakunlangan",
        default=False
    )

    def __str__(self):
        return f"{self.id} - {self.book} {self.thousand - 999}-{self.thousand}"

    @property
    def words(self):
        return [Word.get(id=word_id) for word_id in self.quizzes.split(',')]

    @property
    def answers_and_words(self):
        words = [Word.get(id=word_id) for word_id in self.quizzes.split(',')]
        winner, loser = self.participants.all()
        if winner.true_answers < loser.true_answers or (winner.true_answers == loser.true_answers and winner.battle_time > loser.battle_time):
            loser, winner = winner, loser
        winner_answers = winner.answers.split(',')
        loser_answers = loser.answers.split(',')
        status = {
            '0': "❌",
            '1': "✅"
        }
        return '\n'.join([f"{status[winner_answers[index]]} | {status[loser_answers[index]]} | <b>{word.word} - {word.translation}</b>" for index, word in enumerate(words)])

    class Meta:
        verbose_name = "Bellashuv"
        verbose_name_plural = "Bellashuvlar"


class Participant(AbstractModel):
    battle = ForeignKey(
        Battle,
        verbose_name="Bellashuv",
        related_name="participants",
        on_delete=CASCADE
    )
    participant = ForeignKey(
        User,
        verbose_name="Qatnashchi",
        related_name="battles",
        on_delete=CASCADE
    )
    answers = TextField(
        verbose_name="Javoblar",
        default='',
    )
    started_time = DateTimeField(
        verbose_name="Boshlangan vaqti",
        null=True
    )
    end_time = DateTimeField(
        verbose_name="Tugagan vaqti",
        null=True
    )

    @property
    def true_answers(self):
        return sum(map(int, self.answers.split(',') if self.answers else []))

    @property
    def battle_time(self):
        return (self.end_time - self.started_time).seconds

    def __str__(self):
        return self.participant.full_name

    class Meta:
        verbose_name = "Qatnashchi"
        verbose_name_plural = "Qatnashchilar"


class Training(AbstractModel):
    user = ForeignKey(
        User,
        CASCADE,
        related_name="trainings",
        verbose_name="Foydalanuvchi"
    )
    book = ForeignKey(
        Book,
        CASCADE,
        related_name="trainings",
        verbose_name="Kitob"
    )
    thousand = PositiveSmallIntegerField(
        verbose_name="Minglik"
    )
    hundred = PositiveSmallIntegerField(
        verbose_name="Yuzlik"
    )

    def __str__(self):
        return f"{self.user}, {self.book.name} {self.thousand} {self.hundred}"


class Channel(AbstractModel):
    channel_id = CharField(
        max_length=32,
        verbose_name="IDsi",
        help_text="Kanal IDsini olish uchun kanaldagi biron xabarni @ShowJsonBot ga yuboring"
    )
    name = CharField(
        max_length=256,
        verbose_name="Nomi"
    )
    link = CharField(
        max_length=256,
        verbose_name="Manzil",
        help_text="https://t.me bilan boshlanuvchi manzil"
    )
    members = ManyToManyField(
        User,
        related_name='channels',
        verbose_name="A'zolar",
        blank=True
    )
    required = BooleanField(
        default=False,
        verbose_name="Doim a'zo bo'lish talab etiladimi ?",
        choices=((True, "Ha"), (False, "Yo'q"))
    )
    is_active = BooleanField(
        default=False,
        verbose_name="Holati aktivmi?",
        choices=((True, "Ha"), (False, "Yo'q"))
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kanal"
        verbose_name_plural = "Kanallar"


class Provider(AbstractModel):
    name = CharField(
        max_length=64,
        verbose_name="Nomi"
    )
    token = CharField(
        max_length=256,
        verbose_name="Token"
    )
    is_active = BooleanField(
        default=False,
        choices=((True, "Aktiv"), (False, "No aktiv")),
        verbose_name="Holati"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Provayder"
        verbose_name_plural = "Provayderlar"


class Payment(AbstractModel):
    user = ForeignKey(
        User,
        on_delete=SET_NULL,
        related_name="payments",
        verbose_name="Foydalanuvchi",
        null=True
    )
    provider = ForeignKey(
        Provider,
        on_delete=SET_NULL,
        related_name="payments",
        verbose_name="To'lov operatori",
        null=True
    )
    amount = PositiveIntegerField(
        verbose_name="Miqdori"
    )

    def __str__(self):
        return f"{self.user} | {self.provider} - {self.amount:,} so'm"

    class Meta:
        verbose_name = "To'lov"
        verbose_name_plural = "To'lovlar"


class Post(AbstractModel):
    type = CharField(
        max_length=2,
        choices=MESSAGE.TYPE.CHOICE,
    )
    file = CharField(
        max_length=255,
        null=True,
        blank=True
    )
    text = TextField()
    sent = PositiveIntegerField(
        default=0,
    )

    @property
    def get_type(self):
        return MESSAGE.TYPE.DICT.get(self.type)

    def __str__(self):
        return f"Post with id {self.id} was sent to {self.sent} users."

    class Meta:
        verbose_name = " post"
        verbose_name_plural = "Posts"
