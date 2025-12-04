import math
class toan_hoc():
    def __init__(self,chieu_dai,chieu_rong,chieu_cao):
        try:
            float(chieu_dai)
            float(chieu_rong)
            float(chieu_cao)
        except TypeError:
            raise TypeError('Lỗi kiểu dữ liệu nhập vào!')
        else:
            self.chieu_dai= chieu_dai
            self.chieu_rong = chieu_rong
            self.chieu_cao = chieu_cao
    def tinh_hop_chu_nhat(self):
        Sxp_hinh_hop_cn = 2*(self.chieu_dai * self.chieu_cao + self.chieu_rong * self.chieu_cao)
        Stp_hinh_hop_cn = 2*(self.chieu_dai * self.chieu_rong + self.chieu_dai*self.chieu_rong * self.chieu_cao**2)
        TheTich_hinh_hop_cn = self.chieu_dai*self.chieu_rong*self.chieu_cao
        a= {"Sxp":Sxp_hinh_hop_cn,"Stp":Stp_hinh_hop_cn,"The_Tich":TheTich_hinh_hop_cn}
        print(f'Diện tích xung quanh hình chữ nhật là : {a["Sxp"]}')
        print(f'Diện tích toàn phần hình chữ nhật là : {a["Stp"]}')
        print(f'thể tích hình chữ nhật là : {a["The_Tich"]}' )
    @staticmethod
    def tinh_lap_phuong(canh):
        try: 
            float(canh)
        except TypeError:
            raise TypeError('Lỗi kiểu dữ liệu nhập vào!')
        else:
            Sxp_lap_phuong = 4 * canh**2
            Stp_lap_phuong = 6 * canh**2
            The_tich_lap_phuong = canh*canh*canh
        a= {"Sxp":Sxp_lap_phuong,"Stp":Stp_lap_phuong,"The_Tich":The_tich_lap_phuong}
        print(f'Diện tích xung quanh hình lập phương là : {a["Sxp"]}')
        print(f'Diện tích toàn phần hình lập phương là : {a["Stp"]}')
        print(f'thể tích hình lập phương là : {a["The_Tich"]}' )
    @staticmethod
    def tinh_hinh_cau(ban_kinh):
        try: 
            float(ban_kinh)
        except TypeError:
            raise TypeError('Lỗi kiểu dữ liệu nhập vào!')
        else:
            Sxp_cau = 4 * math.pi * ban_kinh**2
            Stp_cau = 4 * math.pi * ban_kinh**2   
            The_tich_cau = (4%3)*math.pi*ban_kinh**3
        a= {"Sxp":Sxp_cau,"Stp":Stp_cau,"The_Tich":The_tich_cau}
        print(f'Diện tích xung quanh hình cầu là : {a["Sxp"]}')
        print(f'Diện tích toàn phần hình cầu là : {a["Stp"]}')
        print(f'thể tích hình cầu là : {a["The_Tich"]}' )    
    @staticmethod
    def tinh_hinh_tru(ban_kinh,chieu_cao):
        try:
            float(ban_kinh)
            float(chieu_cao)
        except TypeError:
            raise TypeError('Lỗi kiểu dữ liệu nhập vào!')
        else:
            Sxp_tru = 2 * math.pi * ban_kinh * chieu_cao 
            Stp_tru = 2 * math.pi * ban_kinh * chieu_cao * (ban_kinh + chieu_cao)  
            The_tich_tru = math.pi * ban_kinh**2 * chieu_cao
        a= {"Sxp":Sxp_tru,"Stp":Stp_tru,"The_Tich":The_tich_tru}
        print(f'Diện tích xung quanh hình trụ là : {a["Sxp"]}')
        print(f'Diện tích toàn phần hình trụ là : {a["Stp"]}')
        print(f'thể tích hình trụ là : {a["The_Tich"]}' )

while True:
    try:
        print('===== CHƯƠNG TRÌNH TOÁN HÌNH HỌC =====')
        print('1. Hình hộp chữ nhật')
        print('2. Hình lập phương')
        print('3. Hình cầu')
        print('4. Hình trụ')
        print('5. thoát')
        lua_chon=int(input('Nhập lựa chọn của bạn : '))
    except TypeError:
        raise TypeError('Lỗi kiểu dữ liệu nhập vào!')
    else:
        Toan_hoc=toan_hoc(0,0,0)
        if lua_chon == 1:
            a=int(input('Nhập chiều dài : '))
            b=int(input('Nhập chiều rộng : '))
            c=int(input('Nhập chiều cao : '))
            Toan_hoc=toan_hoc(a,b,c)
            Toan_hoc.tinh_hop_chu_nhat()
        elif lua_chon == 2:
            a=int(input('Nhập cạnh : '))
            
            Toan_hoc.tinh_lap_phuong(a)
        elif lua_chon == 3:
            a=int(input('Nhập bán kính : '))
            Toan_hoc.tinh_hinh_cau(a)
        elif lua_chon == 4:
            a=int(input('Nhập bán kính : '))
            b=int(input('Nhập chiều cao : '))
            Toan_hoc.tinh_hinh_tru(a,b)
        else:
            break


