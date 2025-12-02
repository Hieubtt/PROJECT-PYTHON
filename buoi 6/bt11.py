#def f(x):
    #if x > 0 :
        #return 'Duong'
    #else:
        #return 'Am'
    
#b = f(-5)
#print(b)

def palindrome(chuoi):
    
    #chuoi = input('Nhập vào 1 chuỗi : ')

    chuoi_clean=chuoi.lower()
    chuoi_clean=chuoi_clean.replace(' ','')
    chuoi_dao= chuoi_clean[::-1]

    if chuoi_dao==chuoi_clean:
        return('la palindrome')
    else:
        return('khong phai palindrome')
#print(palindrome(''))
print(palindrome('Race car'))
print(palindrome('BUI TRAN TRUNG HIEU'))