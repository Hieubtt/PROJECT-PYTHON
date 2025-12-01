a1 = float(input('Nhập cạnh thứ 1 :'))
a2 = float(input('Nhập cạnh thứ 2 :'))
a3 = float(input('Nhập cạnh thứ 3 :'))

print('Phân loại tam giác:')
print('----------------------Kết Quả----------------------')

if a1==a2==a3:
    print('Đây là tam giác đều')
elif a1+a2<=a3 or a1+a3<=a2 or a2+a3<=a1: 
    print('Đây không phải là tam giác')
elif (a1**2 + a2**2 == a3**2 or a1**2 + a3**2 == a2**2 or a2**2 + a3**2 == a1**2)and (a1 == a2 or a1 == a3 or a2 == a3):
    print('Đây là tam giác vuông cân')   
elif a1**2 + a2**2 == a3**2 or a1**2 + a3**2 ==a2**2  or a3**2 + a2**2 == a1**2:
    print('Đây là tam giác vuông')
elif a1==a2 or a1==a3 or a2==a3:
    print('Đây là tam giác cân')
elif a1!=a2!=a3:
    print('Đây là tam giác thường')
