def loai_bo_trung_lap(danh_sach):
    for i in range(len(danh_sach)):
        for j in range(i+1,len(danh_sach)):
            if danh_sach[i] == danh_sach[j]:
                danh_sach.remove(danh_sach[j])
    return danh_sach

print('Danh sách đã bỏ trùng lặp : ',loai_bo_trung_lap([1, 2, 3, 5, 6, 7, 8]))
            