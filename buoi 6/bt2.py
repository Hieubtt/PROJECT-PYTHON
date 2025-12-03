def func_tinh_tong (a,b):

    while True:
        try:
            a=int(a)
            b=int(b)
        except ValueError:
            raise('Nhập sai kiểu dữ liệu.')
        finally:
            return a+b

print(func_tinh_tong(5,0))