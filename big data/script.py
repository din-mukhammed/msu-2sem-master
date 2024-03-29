import json

full_list = [
    ["AMD Ryzen 5 3500X, OEM", "AMD Ryzen 5 3500X OEM", 0],
    ["AMD Ryzen 5 2600, BOX", "AMD Ryzen 5 2600 BOX", 1],
    ["AMD Ryzen 7 5800X, OEM", "AMD Ryzen 7 5800X OEM", 2],
    ["AMD Ryzen 7 3800X, BOX", "AMD Ryzen 7 3800X BOX", 3],
    ["AMD Ryzen 5 3600X, OEM", "AMD Ryzen 5 3600X OEM", 4],
    ["INTEL Core i5 10600K, OEM", "Intel Core i5-10600K OEM", 5],
    ["INTEL Core i3 10100, BOX", "Intel Core i3-10100 BOX", 6],
    ["INTEL Core i7 8700, OEM", "Intel Core i7-8700 OEM", 7],
    ["INTEL Core i5 9600KF, OEM", "Intel Core i5-9600KF OEM", 8],
    ["INTEL Pentium Gold G6400, OEM", "Intel Pentium Gold G6400 OEM", 9],
]
full_dict = {}
for name1, name2, id in full_list:
    full_dict[name1], full_dict[name2] = id, id

DUP_ID = 'duplicate_id'


def change_file(filename):
    data = None
    with open(filename, 'r', encoding='cp1251') as file:
        data = json.load(file)
    for obj in data:
        obj[DUP_ID] = full_dict[obj['Название']]
    with open(f'out_{filename}', 'w', encoding='utf-8') as file:
        json.dump(obj=data, fp=file, indent=4, ensure_ascii=False)


dupdict = {}


def print_ids(filename):
    data = None
    with open(filename, 'r') as file:
        data = json.load(file)
    for obj in data:
        print(f'{obj["Название"]}  =  {obj["duplicate_id"]}')
        dupdict[obj['Название']] = obj['duplicate_id']


min_freq_field = "Минимальная частота оперативной памяти"
max_freq_field = "Максимальная частота оперативной памяти"
del_key = 'Частота'

del_fields = ['Поддержка режима ECC', 'Свободный множитель', 'Гарантия']


def del_and_change(filename):
    data = None
    with open(filename, 'r') as f:
        data = json.load(f)
    for obj in data:
        for del_field in del_fields:
            if del_field in obj.keys():
                del obj[del_field]
    with open('out' + filename, 'w') as file:
        json.dump(obj=data, fp=file, indent=4, ensure_ascii=False)


def common_fields(f1, f2):
    fields = set()
    data1, data2 = None, None
    with open(f1, 'r') as file:
        data1 = json.load(file)
    obj1 = data1[0]
    with open(f2, 'r') as file:
        data2 = json.load(file)
    obj2 = data2[0]
    intersection = set(obj1.keys()) & set(obj2.keys())
    for val in intersection:
        print(val)


def change_dns_file(f1):
    with open(filename, 'r') as f:
        data = json.load(f)
    for obj in data:
        for del_field in del_fields:
            if del_field in obj.keys():
                del obj[del_field]
    with open('out' + filename, 'w') as file:
        json.dump(obj=data, fp=file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    citilink = 'citilink.json'
    dns = 'dns.json'
    # del_and_change(filename=citilink)
    # del_and_change(filename=dns)
    common_fields(citilink, dns)
    # del_and_change(citilink)
    # change_file(citilink)
    # change_file(dns)
    # print_ids(out_citilink)
    # print_ids(out_dns)
    # ids = [[] for i in range(10)]
    # print('*'*100)
    # for key, val in dupdict.items():
    #     ids[val].append(key)
    # for vec in ids:
    #     print(*vec, len(vec), vec[0] == vec[1])
