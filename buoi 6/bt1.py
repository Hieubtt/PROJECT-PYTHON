def func_Chan_le():
    while True:
        try:
            so=int(input('Hãy nhập vào 1 số : '))
        except ValueError:
            print('Nhập sai kiểu dữ liệu')
        finally:  
            if so % 2 == 0:
                return('Đây là số chẵn')
            else:
                return('Đây là số lẻ')


print(func_Chan_le())
                    

    