so_dien = int(input('Số điện tiêu thụ trong tháng :'))

so_tien_thanh_toan = 0 
while so_dien > 0 :
    if so_dien >= 401: 
        so_tien_thanh_toan =(so_dien-400) * 2927
        print((so_dien-400) * 2927,'6')
        so_dien = 400
        
    elif so_dien >=301 and so_dien<=400:
        so_tien_thanh_toan = so_tien_thanh_toan+(so_dien-300) * 2834
        print((so_dien-300) * 2834,'5')
        so_dien = 300
        
    elif so_dien >=201 and so_dien<=300:        
        so_tien_thanh_toan = so_tien_thanh_toan +(so_dien-200) * 2536
        print((so_dien-200) * 2536,'4')
        so_dien = 200
        
    elif so_dien >= 101 and so_dien <= 200:
        so_tien_thanh_toan = so_tien_thanh_toan +(so_dien-100) * 2014
        print((so_dien-100) * 2014,'3')
        so_dien =100
        
    elif so_dien >= 51 and so_dien <= 100:
        so_tien_thanh_toan = so_tien_thanh_toan + (so_dien-50) * 1734
        print((so_dien-50) * 1734,'2')
        so_dien = 50
        
    elif so_dien <=50:
        so_tien_thanh_toan = so_tien_thanh_toan + so_dien * 1678 
        print(so_dien * 1678 ,'1')
        so_dien = 0
        



print('Số tiền điện cần thanh toán là :',so_tien_thanh_toan,'VND')

    

