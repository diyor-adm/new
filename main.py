from telegram.bot import Bot
from telegram.chat import Chat
from telegram.constants import CHAT_GROUP
from telegram.ext import Updater, MessageHandler,Dispatcher, ConversationHandler, CommandHandler, CallbackContext, Filters
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, MessageEntity, ParseMode, message, update
from time import gmtime, strftime, time
import django
import os
import sys
import logging
from telegram.files.document import Document
from telegram.utils.helpers import effective_message_type
import xlsxwriter
import pandas as pd
from datetime import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

sys.dont_write_bytecode = True
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()
from db.models import Appeal

updater: Updater = Updater(token='2073307763:AAHhuynOe4Lex93k0BWDvUqoGH5gvjKm42o')
dispatcher = updater.dispatcher
MENU_STATE, FIRST_NAME_STATE, LAST_NAME_STATE, REGION_STATE, ADDRESS_STATE, PHONE_STATE, APPEAL_STATE = range(
    7)


def menu_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton('Yangi murojaat')],
        [KeyboardButton('Mening murojaatlarim')]
    ], resize_keyboard=True, one_time_keyboard=True)


def phone_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton('Telefon raqam yuborish', request_contact=True)]], resize_keyboard=True, one_time_keyboard=True)


def region_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton('Nurafshon shahri')],
        [KeyboardButton('O`rta Chirchiq tumani')]
    ], resize_keyboard=True, one_time_keyboard=True)


def start_handler(update: Update, context: CallbackContext):
    if update.effective_user.first_name != None and update.effective_user.last_name!= None:
        fullname = f'{update.effective_user.first_name} {update.effective_user.last_name}'
    else:
        fullname = f'hurmatli foydalanuvchi'
    update.message.reply_text(f'Assalomu alaykum {fullname}. Murojaatlarni qabul qiluvchi botga xush kelibsiz!\nKerakli bo`limni tanlang', reply_markup=menu_keyboard())
    return MENU_STATE


def menu_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Sizga kerakli bo`limni tanlang', reply_markup=menu_keyboard())
    return MENU_STATE


def new_appeal_handler(update: Update, context: CallbackContext):

    update.message.reply_text('Ismingizni kiriting',reply_markup=ReplyKeyboardRemove())
    return FIRST_NAME_STATE


def first_name_handler(update: Update, context: CallbackContext):
    context.chat_data.update({
        'first_name': update.message.text,
    })
    print(context.chat_data)
    update.message.reply_text('Familiyangizni kiriting!')
    return LAST_NAME_STATE


def last_name_resend_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Familiyangizni kiriting!')


def region_resend_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Iltimos quyidan yashash tuman yoki shahringizni tanlang!')


def address_resend_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Iltimos yashash joyingizni to`liq kiriting!')


def last_name_handler(update: Update, context: CallbackContext):
    context.chat_data.update({
        'last_name': update.message.text,
    })
    print(context.chat_data)
    update.message.reply_text(
        'Quyida istiqomat qiluvchi tuman yoki shahringizni tanlang!', reply_markup=region_keyboard())
    return REGION_STATE


def region_handler(update: Update, context: CallbackContext):
    context.chat_data.update({
        'region': update.message.text,
    })
    print(context.chat_data)
    update.message.reply_text(
        'Yashash joyingizni to`liq kiriting',reply_markup=ReplyKeyboardRemove())
    return ADDRESS_STATE


def address_handler(update: Update, context: CallbackContext):
    context.chat_data.update({
        'address': update.message.text,
    })
    print(context.chat_data)
    update.message.reply_text(
        'Telefon raqamingizni kiriting yoki pastdagi tugmani bosing', reply_markup=phone_keyboard())

    return PHONE_STATE


def phone_handler(update: Update, context: CallbackContext):
    context.chat_data.update({
        'phone_number': update.message.text,
    })
    print(context.chat_data)
    update.message.reply_text(
        'Murajaat qilishingiz sababini to`liq yozing', reply_markup=ReplyKeyboardRemove())
    return APPEAL_STATE


def phone_entity_handler(update: Update, context: CallbackContext):
    phone_number_entity = pne = list(
        filter(lambda e: e.type == 'phone_number', update.message.entities))[0]
    print(phone_number_entity)
    phone_number = update.message.text[pne.offset:pne.offset + pne.length]
    if len(phone_number) ==9:
        phone_number = f'+998{phone_number}'
    context.chat_data.update({
        'phone_number': phone_number,
    })
    update.message.reply_text(
        'Murajaat qilishingiz sababini to`liq yozing', reply_markup=ReplyKeyboardRemove())
    return APPEAL_STATE


def phone_contact_handler(update: Update, context: CallbackContext):
    phone_number = update.message.contact['phone_number']
    context.chat_data.update({
        'phone_number': f'+{phone_number}',
    })
    print(context.chat_data)
    update.message.reply_text(
        'Murojaat qilishingiz sababini to`liq yozing', reply_markup=ReplyKeyboardRemove())
    return APPEAL_STATE


def phone_resend_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Iltimos telefon raqamingizni +998********* ko`rinishida kiriting yoki pastdagi tugmani bosing',
                              reply_markup=phone_keyboard())


def appeal_handler(update: Update, context: CallbackContext):
    context.chat_data.update({
        'appeal': update.message.text,
    })
    print(context.chat_data)
    dt = datetime.now()
    cd = context.chat_data
    appeal = Appeal.objects.create(
        first_name=cd['first_name'][0:255],
        last_name=cd['last_name'][0:255],
        region=cd['region'][0:255],
        address=cd['address'][0:255],
        phone_number=cd['phone_number'][0:63],
        appeal=cd['appeal'],
        date_time = dt.strftime(f"%Y-%m-%d %H:%M:%S"),
        user_id=update.effective_user.id
    )
    fullname = f'{cd["first_name"][0:255]} {cd["last_name"][0:255]}'
    phone = cd['phone_number'][0:63]
    reg = cd['region'][0:255]
    address = cd['address'][0:255]
    appeal = cd['appeal']
    dtime = dt.strftime(f"%Y-%m-%d %H:%M:%S")

    # context.bot.forward_message( )
    context.bot.send_message(chat_id = '-1001507722890', text=f'<b>Murojaatchi:</b> {fullname}\n<b>Yashash tumani(shahri):</b> {reg}\n<b>Yashash manzili:</b> {address}\n<b>Telefon raqami:</b> {phone}\n<b>Murojaat sababi:</b> {appeal}\n<b>Murojaat qilingan vaqt:</b> {dtime}',parse_mode=ParseMode.HTML)

    update.message.reply_text(
        'Murojaatingiz qabul qilindi. Tez orada aloqaga chiqamiz')
    return menu_handler(update, context)


def appeal_resend_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Iltimos murojaatingizni matn ko`rinishida qoldiring!')


def send_file(update: Update, context: CallbackContext):
    appeals = Appeal.objects.all()
    workbook = xlsxwriter.Workbook(f'Barcha_murojaatlar.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})
    wrap = workbook.add_format({'text_wrap': True})
    worksheet.set_column(1, 5, 20,wrap)
    worksheet.write('A1', 'Murojaat', bold)
    worksheet.write('B1', 'Ismi', bold)
    worksheet.write('C1', 'Familiyasi', bold)
    worksheet.write('D1', 'Yashash tumani(shahri)', bold)
    worksheet.write('E1', 'Yashash manzili', bold)
    worksheet.write('F1', 'Telefon raqami', bold)
    worksheet.set_column(6, 6, 50,wrap)
    worksheet.write('G1', 'Murojaat sababi', bold)
    worksheet.set_column(7, 7, 20)
    worksheet.write('H1', 'Murojaat qilingan vaqt', bold)
    row = 1
    col = 0
    for appeal in appeals:
        worksheet.write_string(row, col, f'{row}')
        worksheet.write_string(row, col+1, appeal.first_name)
        worksheet.write_string(row, col+2, appeal.last_name)
        worksheet.write_string(row, col+3, appeal.region)
        worksheet.write_string(row, col+4, appeal.address)
        worksheet.write_string(row, col+5, appeal.phone_number)
        worksheet.write_string(row, col+6, appeal.appeal)
        worksheet.write_string(row, col+7, appeal.date_time)
        row += 1
    worksheet.write(row, 0, 'Umumiy murojaatlar soni', bold)
    worksheet.write(row, 2, f'{row-1}', bold)
    workbook.close()
    context.bot.send_document(chat_id = '-1001507722890', document=open('Barcha_murojaatlar.xlsx', 'rb'))
    os.remove('Barcha_murojaatlar.xlsx')

def all_appeal_handler(update: Update, context: CallbackContext):
    appeals = Appeal.objects.order_by('id').filter(user_id=update.effective_user.id)[::]
    if len(appeals) == 0:
       update.message.reply_text('Siz hech qanday murojaat qoldirmagansiz!')
    else:
        first_name = ''
        last_name = ''
        fullname = f'{update.effective_user.first_name} {update.effective_user.last_name}'
    # update.message.reply_text('Mening oxirgi 5 ta murojaatim')
        workbook = xlsxwriter.Workbook(f'{fullname}_murojaatlar.xlsx')
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})
        wrap = workbook.add_format({'text_wrap': True})
        worksheet.set_column(1, 5, 20,wrap)
        worksheet.write('A1', 'Murojaat', bold)
        worksheet.write('B1', 'Ismi', bold)
        worksheet.write('C1', 'Familiyasi', bold)
        worksheet.write('D1', 'Yashash tumani(shahri)', bold)
        worksheet.write('E1', 'Yashash manzili', bold)
        worksheet.write('F1', 'Telefon raqami', bold)
        worksheet.set_column(6, 6, 50,wrap)
        worksheet.write('G1', 'Murojaat sababi', bold)
        worksheet.set_column(7, 7, 20)
        worksheet.write('H1', 'Murojaat qilingan vaqt', bold)
        row = 1
        col = 0
        for appeal in appeals:
            worksheet.write_string(row, col, f'{row}')
            worksheet.write_string(row, col+1, appeal.first_name)
            worksheet.write_string(row, col+2, appeal.last_name)
            worksheet.write_string(row, col+3, appeal.region)
            worksheet.write_string(row, col+4, appeal.address)
            worksheet.write_string(row, col+5, appeal.phone_number)
            worksheet.write_string(row, col+6, appeal.appeal)
            worksheet.write_string(row, col+7, appeal.date_time)
            row += 1
        worksheet.write(row, 0, 'Umumiy murojaatlar soni', bold)
        worksheet.write(row, 2, f'{row-1}', bold)
        workbook.close()
        context.bot.send_document(update.effective_user.id, document=open(f'{fullname}_murojaatlar.xlsx', 'rb'))
        os.remove(f'{fullname}_murojaatlar.xlsx')

    # dt = datetime.now()
    # dtime = strftime(f"%Y-%m-%d %H:%M:%S", dt)
   
    # else:
    #     for appeal in appeals:
    #         update.message.reply_text(f'{appeal.appeal}'\
    #             f'\n\n'\
    #             f'<b>{appeal.first_name} {appeal.last_name}\n{dtime}</b>'\
    #             ,  parse_mode=ParseMode.HTML)


def stop_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Hayr!', reply_markup=ReplyKeyboardRemove())

def group(update: Update, context: CallbackContext):
    arg = update.message.text
    if arg == '/stat':
        send_file(update,context)
    is_reply = update.message.reply_to_message is not None
    if is_reply:
        sent_dt = update.message.reply_to_message.text[-19:]
        print('==================')
        all_text = update.message.reply_to_message.text.split('\n')
        phone_num = all_text[3][-13:]
        print(phone_num)
        print('==================')
        appeals = Appeal.objects.order_by('id').filter(date_time=sent_dt).filter(phone_number=phone_num)[::]
        appeal = ''
        user_id = ''
        full_name = ''
        dtime = ''
        for i in appeals:
            appeal = i.appeal
            user_id = i.user_id
            full_name = f'{i.first_name} {i.last_name}'
            dtime = i.date_time
        context.bot.send_message(chat_id = user_id, text=f"Assalomu alaykum, hurmatli <b>{full_name}</b> \nSizni <b>{dtime}</b> dagi murojaatingizga asosan, <b>{arg}</b>",parse_mode=ParseMode.HTML)

    # return dispatcher.add_handler(MessageHandler(Filters.text('/stat'),send_file))


dispatcher.add_handler(MessageHandler(Filters.group, group))

dispatcher.add_handler(ConversationHandler(
    entry_points=[
        MessageHandler(Filters.private, start_handler)],
        
    states={
        MENU_STATE: [
            MessageHandler(Filters.regex(r'^Yangi murojaat$'),
                           new_appeal_handler),
            MessageHandler(Filters.regex(
                r'^Mening murojaatlarim$'), all_appeal_handler),
            MessageHandler(Filters.all, menu_handler)
        ],
        FIRST_NAME_STATE: [
            MessageHandler(Filters.text, first_name_handler),
            MessageHandler(Filters.all, new_appeal_handler),
        ],
        LAST_NAME_STATE: [
            MessageHandler(Filters.text, last_name_handler),
            MessageHandler(Filters.all, last_name_resend_handler),
        ],
        REGION_STATE: [
            MessageHandler(Filters.regex(
                r'^Nurafshon shahri$'), region_handler),
            MessageHandler(Filters.regex(
                r'^O`rta Chirchiq tumani$'), region_handler),
            MessageHandler(Filters.all, region_resend_handler),
        ],
        ADDRESS_STATE: [
            MessageHandler(Filters.text, address_handler),
            MessageHandler(Filters.all, address_resend_handler),
        ],
        PHONE_STATE: [
            MessageHandler(Filters.text & Filters.entity(
                MessageEntity.PHONE_NUMBER), phone_entity_handler),
            MessageHandler(Filters.contact, phone_contact_handler),
            MessageHandler(Filters.all, phone_resend_handler),
        ],
        ADDRESS_STATE: [
            MessageHandler(Filters.text, address_handler),
            MessageHandler(Filters.all, address_resend_handler),
        ],
        APPEAL_STATE: [
            MessageHandler(Filters.text, appeal_handler),
            MessageHandler(Filters.all, appeal_resend_handler),
        ],
    },


    fallbacks=['stop', stop_handler],

))

updater.start_polling(timeout=600)
updater.idle()
