#Đề bài: Tạo từ điển lưu thông tin của 3 sinh viên, với key là mã sinh viên và value là tuple chứa (họ tên, điểm).
#Cho phép tìm kiếm thông tin sinh viên bằng mã sinh viên

n = int(input('Hãy nhập số lượng học sinh cần nhập : '))
sinh_vien = {}
for i in range(n):
    ma_sv = input(f"Nhập mã sinh viên thứ {i+1}: ")
    ho_ten = input("Nhập họ tên: ")
    diem = float(input("Nhập điểm: "))
    
    if ma_sv not in sinh_vien: # lưu theo dạng tuple để tránh trùng mã SV
        sinh_vien[ma_sv] = []
    sinh_vien[ma_sv].append((ho_ten, diem)) # dùng được append khi giá trị của 1 dict là 1 cái list
    print(sinh_vien)
    
    #Lưu vào dict
    #sinh_vien[ma_sv] = (ho_ten, diem)


ma_sv_can_tim = input("Nhập mã sinh viên cần tìm : ")

result_1 = sinh_vien.get(ma_sv_can_tim,False)

print(result_1)

if result_1 !=False:
    ho_ten,diem = result_1[0] 
    print(f"Mã số SV là : {ma_sv_can_tim},Họ tên: {ho_ten}, Điểm: {diem}")
else:
    print('Không tìm thấy mã sinh viên này trong danh sách. !')
