#a=[i for i in range (0,10) if i % 2 ==0]
#print(a)


empty_class = 'BUI TRAN TRUNG HIEU'
empty_class1= list(empty_class)
empty_class2 = list([empty_class])
print(empty_class1)
print(empty_class2)

list_mua_hang = ['Cam','Quyt','Tao','Thom','Xoai','Oi']
list_mua_hang[:2]=['Xoai Non','Cam Tuoi']#[0,2,4,6,8],[1,3,5,7,9]
print(list_mua_hang[:])

list_mua_hang_theomua = [
                 ['Cam','Quyt','Tao'],
                 ['Thom','Xoai','Oi'],
                 ['Man','Thanh Long','Dua Hau']
                 ]


print(list_mua_hang_theomua[1][0])








