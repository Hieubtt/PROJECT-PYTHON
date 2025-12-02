doan_chuoi = input('Hãy nhập vào 1 đoạn chuỗi : ')

tu_list_doan_chuoi = doan_chuoi.split()

max_len = max(len(tu) for tu in tu_list_doan_chuoi)
min_len = min(len(tu) for tu in tu_list_doan_chuoi)

print(max_len)
print(min_len)
tu_dai_nhat = [tu for tu in tu_list_doan_chuoi if len(tu) == max_len]
tu_ngan_nhat = [tu for tu in tu_list_doan_chuoi if len(tu) == min_len]
print('Từ dài nhất trong đoạn chuỗi là : ',tu_dai_nhat)
print('Từ ngan nhất trong đoạn chuỗi là : ',tu_ngan_nhat)