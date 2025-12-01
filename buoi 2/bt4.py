month = int(input('Nhập số tháng từ 1 đến 12:'))
year = int(input('Nhập số năm :'))

if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12 :
    print('Thang',month,'có 31 ngày')
elif month == 4 or month == 6 or month == 9 or month == 11 :
    print('Thang',month,'có 30 ngày')
elif month == 2 and (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0) :
    print('Thang',month,'có 29 ngày')
else : 
    print('Thang',month,'có 28 ngày')