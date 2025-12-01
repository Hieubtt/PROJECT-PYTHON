chieu_cao_1 = int(input('Hãy nhập chiều cao 1: '))
chieu_cao_2 = int(input('Hãy nhập chiều cao 2: ')) 
chieu_cao_3 = int(input('Hãy nhập chiều cao 2: '))

print('--------------Kết Quả------------------')
if chieu_cao_1 > chieu_cao_2 and chieu_cao_1 > chieu_cao_3 :
    print('Chiều cao lớn nhất là : ',chieu_cao_1)
elif chieu_cao_2 > chieu_cao_1 and chieu_cao_2 > chieu_cao_3 :
    print('Chiều cao lớn nhất là : ',chieu_cao_2)
else : 
    print('Chiều cao lớn nhất là :',chieu_cao_3)