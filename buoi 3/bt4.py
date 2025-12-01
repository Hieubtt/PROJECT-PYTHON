colors = ["Đỏ", "Xanh", "Vàng", "Tím", "Cam"] 
colors1= colors[:2] + colors[3:]

print("Sau khi xoá Vàng" + str(colors[:2] + colors[3:]))

print("Sau khi xoá phần tử cuối" + str(colors1[:-1]))