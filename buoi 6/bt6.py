def trich_xuat_chuoi(chuoi, bat_dau, ket_thuc):
    try: 
        chuoi[ket_thuc]
    except IndexError:
        raise IndexError('Chỉ mục không hợp lệ hoặc vượt quá chuỗi')
    else:
        return  chuoi[bat_dau:ket_thuc]
    
print('Trích xuất chuỗi là : ',trich_xuat_chuoi("Python là ngôn ngữ lập trình", 7, 100))

print(len("Python là ngôn ngữ lập trình"))