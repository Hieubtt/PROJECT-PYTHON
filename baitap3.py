
Target = int(input("Giá trị món đồ cần mua : "))

Tien_tiet_kiem = 0 
i = 0 
while Tien_tiet_kiem < Target:
        i = i + 1
        if Tien_tiet_kiem >= Target:
            break
        if i % 5 == 0 :
            Tien_tiet_kiem = Tien_tiet_kiem + 10000 + 5000
        else : 
            Tien_tiet_kiem = Tien_tiet_kiem + 10000
        
        
print ('Số ngày cần tiết kiệm : ' + str(i) ,'Số tiền thừa' + str(Tien_tiet_kiem-Target))




