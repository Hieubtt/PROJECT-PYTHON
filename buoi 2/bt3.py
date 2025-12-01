do_tuoi = int(input('Nhập độ tuổi của bạn :'))
print('Xác định cấp học tương ứng :')
print('---------------------------------Kết quả-----------------------------')
if do_tuoi >=6 and do_tuoi <=10:
    print('Độ tuổi của bạn là học sinh cấp 1:')
elif do_tuoi >=11 and do_tuoi <=14:
    print('Độ tuổi của bạn là học sinh cấp 2:')
elif do_tuoi >=15 and do_tuoi <=18:
    print('Độ tuổi của bạn là học sinh cấp 3:')
else : 
    print('Không thuộc độ tuổi học sinh phổ thông.')