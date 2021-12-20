from datetime import datetime
from db.models import Appeal
import xlsxwriter
# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Murojaatlar.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
money_format = workbook.add_format({'num_format': '$#,##0'})
date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})
worksheet.set_column(1, 1, 15)
worksheet.write('A1', 'Ismi', bold)
worksheet.write('B1', 'Familiyasi', bold)
worksheet.write('C1', 'Yashash tumani(shahri)', bold)
worksheet.write('D1', 'Yashash manzili', bold)
worksheet.write('E1', 'Telefon raqami', bold)
worksheet.write('F1', 'Murojaat sababi', bold)
worksheet.write('G1', 'Murojaat qilingan vaqt', bold)
expenses = (
    ['Rent', '2013-01-13', 1000],
    ['Gas',  '2013-01-14',  100],
    ['Food', '2013-01-16',  300],
    ['Gym',  '2013-01-20',   50],
)
row = 1
col = 0
for item, date_str, cost in (expenses):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    worksheet.write_string  (row, col,     item              )
    worksheet.write_datetime(row, col + 1, date, date_format )
    worksheet.write_number  (row, col + 2, cost, money_format)
    row += 1
worksheet.write(row, 0, 'Total', bold)
worksheet.write(row, 2, '=SUM(C2:C5)', money_format)
workbook.close()


{'message': {
    'new_chat_members': [],
    'date': 1640015222,
    'reply_to_message': 
        {'new_chat_members': [],
        'date': 1639987242,
        'photo': [],
        'supergroup_chat_created': False,
        'channel_chat_created': False,
        'entities': [
            {'offset': 0, 'length': 12, 'type': 'bold'},
            {'offset': 34, 'length': 23, 'type': 'bold'},
            {'offset': 75, 'length': 16, 'type': 'bold'},
            {'offset': 99, 'length': 15, 'type': 'bold'},
            {'offset': 115, 'length': 13, 'type': 'phone_number'},
            {'offset': 129, 'length': 16, 'type': 'bold'},
            {'offset': 155, 'length': 23, 'type': 'bold'}
            ],
        'text': 'Murojaatchi: Abduxoliq Saidaliyev\nYashash tumani(shahri): Nurafshon shahri\nYashash manzili: Hxjeks\nTelefon raqami: +998935470847\nMurojaat sababi: Yehebwoa\nMurojaat qilingan vaqt: 2021-12-20 13:00:42', 
        'group_chat_created': False,
        'chat': {
            'username': 'murojaatbotuchun', 
            'id': -1001507722890, 
            'type': 'supergroup', 
            'title': 'Murojaat group'}, 
            'delete_chat_photo': False, 
            'message_id': 113, 
            'caption_entities': [], 
            'new_chat_photo': [], 
            'from': {
                'username': 'Toshkent_viloyat_murojaat_bot', 
                'id': 2073307763, 
                'first_name': 'Murojaat bot', 
                'is_bot': True}
                }, 
            'photo': [], 
            'supergroup_chat_created': False, 
            'channel_chat_created': False, 
            'entities': [], 
            'text': 'D', 
            'group_chat_created': False, 
            'chat': {
                'username': 'murojaatbotuchun',
                'id': -1001507722890, 
                'type': 'supergroup', 
                'title': 'Murojaat group'
                }, 
            'delete_chat_photo': False, 
            'message_id': 115, 
            'caption_entities': [],
            'new_chat_photo': [], 
            'from': {
                'username': 'Diyor_adm',
                'id': 332668743, 
                'first_name': 'Diyorbek', 
                'language_code': 'uz', 
                'last_name': 'Abduqodirov', 
                'is_bot': False}
                }, 
            'update_id': 338703815}