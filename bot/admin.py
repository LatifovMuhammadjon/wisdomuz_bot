from threading import Thread
from time import sleep

from django.urls import reverse
from telebot import TeleBot
from telebot.apihelper import ApiException

from django.contrib import admin, messages
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User as Staff, Group

from .models import Pocket,User, Book, Word, Exercise, Battle, Channel, Provider, Payment, Post, Count, MESSAGE, TOKEN

admin.site.site_header = "Boshqaruv paneli"
admin.site.index_title = "@wisdom_edubot"
admin.site.site_title = "Boshqaruv paneli"
admin.site.empty_value_display = "Biriktirilmagan"

admin.site.unregister(Staff)
admin.site.unregister(Group)

bot = TeleBot(TOKEN, parse_mode='html')


class ExerciseForm(forms.ModelForm):
    word_id = forms.IntegerField(min_value=1)

    class Meta:
        model = Exercise
        exclude = ['created_time']

    def clean(self):
        cleaned_data = super().clean()
        word_id = cleaned_data.get('word_id')
        if word_id:
            word: Word = Word.get(id=word_id)
            if not word:
                raise forms.ValidationError("Ushbu tartib raqamli so'z topilmadi", code='invalid')
        else:
            raise forms.ValidationError("Tartib raqam kiritilishi shart", code='invalid')

    def save(self, commit=True):
        word_id = self.cleaned_data.get('word_id')
        exercise = super(ExerciseForm, self).save(commit=commit)
        exercise.word = Word.get(id=word_id)
        if commit:
            exercise.save()
        return exercise


def start_posting(post: Post):
    if post:
        total = 0
        users = list(User.all())
        for user in users:
            try:
                if post.type == MESSAGE.TYPE.AUDIO:
                    bot.send_audio(
                        user.user_id,
                        post.file,
                        caption=post.text,
                    )
                elif post.type == MESSAGE.TYPE.VOICE:
                    bot.send_voice(
                        user.user_id,
                        post.file,
                        caption=post.text,
                    )
                elif post.type == MESSAGE.TYPE.VIDEO:
                    bot.send_video(
                        user.user_id,
                        post.file,
                        caption=post.text
                    )
                elif post.type == MESSAGE.TYPE.PHOTO:
                    bot.send_photo(
                        user.user_id,
                        post.file,
                        caption=post.text
                    )
                else:
                    bot.send_message(
                        user.user_id,
                        post.text
                    )
                total += 1
                sleep(0.05)
            except ApiException as e:
                error = str(e.args)
                if "deactivated" in error or "blocked by the user" in error:
                    continue
                else:
                    users.append(user)
        post.sent = total
        post.save()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_time'
    list_display = [
        'user_id',
        'full_name',
        'energy',
        'diamonds',
        'is_member',
        'is_banned'
    ]

    readonly_fields = ['user_id', 'full_name', 'energy', 'is_member']
    fields = ['user_id', 'full_name', 'energy', 'is_member', 'is_banned']

    search_fields = ['full_name', 'user_id']
    list_filter = ['is_member', 'is_banned']
    exclude = ['created_time']

    def diamonds(self, obj):
        return obj.diamonds

    diamonds.short_description = "💎"

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_time'
    list_display = [
        'name',
        'order',
        'first',
        'last',
        'description'
    ]
    exclude = ['created_time']
    list_filter = ['is_active']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    change_form_template = "admin/word_change.html"
    date_hierarchy = 'created_time'
    list_display = [
        'id',
        'book',
        'word',
        'translation',
        'variants'
    ]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def save_model(self, request, obj, form: ExerciseForm, change):
        super(WordAdmin, self).save_model(request, obj, form, change)
        if obj and not change:
            Exercise.create(
                word=obj,
                question=obj.translation
            )

    exclude = ['created_time']
    search_fields = ['id', 'book__name', 'word', 'translation']


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    form = ExerciseForm
    date_hierarchy = 'created_time'
    list_display = [
        'id',
        'word',
        'question',
        'answer',
        'variants'
    ]

    fields = [
        'word_id',
        'question',
        'answer',
        'variants'
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ExerciseAdmin, self).get_form(request, obj, **kwargs)
        if obj and obj.word:
            form.base_fields['word_id'].initial = obj.word.id
        return form

    def save_model(self, request, obj, form: ExerciseForm, change):
        form.base_fields['word'] = form.cleaned_data.get('word_id')
        super(ExerciseAdmin, self).save_model(request, obj, form, change)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    search_fields = ['word__word', 'word__translation', 'question', 'answer']


@admin.register(Battle)
class BattleAdmin(admin.ModelAdmin):
    change_form_template = 'admin/battle_change.html'
    date_hierarchy = 'created_time'
    list_display = [
        'get_participants',
        'book',
        'quizzes',
        'found'
    ]

    readonly_fields = ['book', 'thousand']
    fields = ['book', 'thousand']
    search_fields = ['book__name']
    list_filter = ['thousand', 'found', 'finished']
    exclude = ['created_time']

    def get_participants(self, obj):
        return " - ".join([participant.participant.full_name for participant in obj.participants.all()])

    get_participants.short_description = "Qatnashchilar"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = [
        'channel_id',
        'name',
        'link',
        'members_count',
        'required',
        'is_active'
    ]

    exclude = [
        'members',
        'created_time'
    ]

    def members_count(self, channel: Channel):
        return f"{channel.members.count()} ta"

    members_count.short_description = "A'zolar soni"


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_time'
    list_display = [
        'name',
        'token',
        'is_active'
    ]

    search_fields = [
        'name',
        'token'
    ]

    list_filter = [
        'is_active'
    ]

    exclude = ['created_time']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_time'
    list_display = [
        'user',
        'provider',
        'created_time'
    ]

    search_fields = [
        'user__ful_name',
        'provider__name',
        'amount'
    ]

    fields = [
        'user',
        'provider',
        'get_amount',
    ]

    readonly_fields = [
        'user',
        'provider',
    ]

    list_filter = [
        'provider'
    ]

    def get_amount(self, obj: Payment):
        return f"{obj.amount:,} so'm"

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    get_amount.short_description = "Miqdori"

admin.site.register(Pocket)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_time'
    list_display = [
        'id',
        'type',
        'sent'
    ]

    list_filter = [
        'type'
    ]

    exclude = [
        'sent',
        'created_time'
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.save()
            thread = Thread(target=start_posting, args=(obj,))
            thread.start()
            self.message_user(request, "Sending post to users sent...", messages.SUCCESS)
        return HttpResponseRedirect(reverse("admin:bot_post_changelist"))
