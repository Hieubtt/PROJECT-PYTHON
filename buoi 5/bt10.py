##Đề bài: Nhập vào một chuỗi, đếm số lần xuất hiện của từng ký tự trong chuỗi và lưu vào từ điển
chuoi_ki_tu = input('Nhập chuỗi kí tự : ')

dict_ky_tu = {}
for keys in chuoi_ki_tu:
    dict_ky_tu[keys] = dict_ky_tu.get(keys, 0) + 1
#dict_ky_tu[keys] = có nghĩa là nó cập nhật value của keys trong dict 
# dict_ky_tu.get('a': '0') nếu get ko get đc giá trị thì trả về 0
print("Số lần xuất hiện từng ký tự:")
for key,value in dict_ky_tu.items():
    print(f"'{key}': {value}")
#for key in List_1:

