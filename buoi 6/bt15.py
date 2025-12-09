# Cho danh sách các dictionary (ví dụ: danh sách sinh viên với các thuộc tính). 
# Viết hàm nhóm theo nhiều tiêu chí cùng lúc (ví dụ: theo lớp và điểm số).
# Test 
students = [ {'name': 'An', 'class': '10A', 'score': 8}, {'name': 'Bình', 'class': '10A', 'score': 9},
 {'name': 'Chi', 'class': '10B', 'score': 8}, 
{'name': 'Dũng', 'class': '10A', 'score': 8}, 
{'name': 'Em', 'class': '10B', 'score': 9}, ]


def group_dict(data,keys):
    group  = {}

    for item in data:
        group_key = tuple(item[k] for k in keys)
        if group_key not in group:
            group[group_key] = []

        group[group_key].append(item)
    return group    

result = group_dict(students, ["class", "score"])

for key, value in result.items():
    print(key, ":", value)