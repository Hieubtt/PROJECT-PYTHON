def sap_xep_theo_gia_tri(du_lieu,giam_dan):
    List_data = list(du_lieu.items())
    if giam_dan:
        List_data = sorted(List_data,key = lambda x : x[1] , reverse=True)
    else:
        List_data = sorted(List_data,key = lambda x : x[1] , reverse=False)
    
    print(List_data)
    
print(sap_xep_theo_gia_tri({
    "chuoi": 5,
    "tuple": 3,
    "list": 8,
    "dictionary": 2,
    "set": 6
}, False)
)
            






