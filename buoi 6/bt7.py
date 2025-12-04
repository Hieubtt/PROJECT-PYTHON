def loc_sinh_vien_gioi(du_lieu):
    for ma_sv,thong_tin in du_lieu.items():
            if thong_tin['diem'] >=8:
                return('Danh sách sinh viên có điểm trên 8.0 : ',ma_sv,thong_tin['ten'],thong_tin['diem'])
     
    

print(loc_sinh_vien_gioi({
    "SV001": {"ten": "Nguyễn Văn A", "diem": 8.5},
    "SV002": {"ten": "Trần Thị B", "diem": 7.5},
    "SV003": {"ten": "Lê Văn C", "diem": 9.0}
}) 
)
sinh_vien = {
    "SV001": {"ten": "Nguyễn Văn A", "diem": 8.5},
    "SV002": {"ten": "Trần Thị B", "diem": 7.5},
    "SV003": {"ten": "Lê Văn C", "diem": 9.0}
}
print(sinh_vien["SV001"]["ten"])
print(sinh_vien["SV001"]["diem"])

