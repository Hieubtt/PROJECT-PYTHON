#Tạo một tuple chứa thông tin về một học sinh: (họ tên, tuổi, điểm toán, điểm văn, điểm anh). 
#Cho phép người dùng nhập thông tin từ bàn phím, sau đó tính và in ra điểm trung bình của học sinh đó.

ho_ten = input('Nhập họ và tên : ')
tuoi = int(input('Nhập tuổi : '))
diem_toan = float(input('Nhập điểm toán : '))
diem_van = float(input('Nhập điểm văn : '))
diem_anh = float(input('Nhập điểm anh : '))

tuple_hs = (ho_ten,tuoi,diem_toan,diem_van,diem_anh)

print(f'Học sinh : {ho_ten} - Tuổi : {tuoi}')
print()
print(f'Điểm trung bình : {(diem_van + diem_toan + diem_anh)/3}')


