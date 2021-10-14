import zipfile
import os
import hashlib
import requests
import re
import csv


# Первое задание


zip_lab = zipfile.ZipFile(r'D:\\labs\\lab1\\tiff-4.2.0_lab1.zip')
os.mkdir('D:\\labs\\lab1\\archive')
zip_lab.extractall('D:\\labs\\lab1\\archive')
zip_lab.close()


# Второе задание


txt_files = []
for r, d, f in os.walk("D:\\labs\\lab1\\archive"):
    for file in f:
        if file.endswith(".txt"):
            txt_files.append(str(r + '\\' + file))
print("Список всех файлов с расширением .txt:")
print('\n'.join(txt_files))

result = []
for file in txt_files:
    data = open(file, 'rb')
    con = data.read()
    result.append(hashlib.md5(con).hexdigest())
    data.close()
print("Хэш файлов:")
print('\n'.join(result))


# Третье задание


target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
target_file = ''
target_file_data = ''
for r, d, f in os.walk(r"D:\\labs\\lab1\\archive"):
    for file in f:
        data = os.path.join(r, file)
        file_data = open(data, "rb")
        con = file_data.readline()
        if hashlib.md5(con).hexdigest() == target_hash:
            target_file = r + "\\" + file
            target_file_data = con
print(target_file)
print(target_file_data)


# Четвертое задание


r = requests.get(target_file_data)
result_dct = {}
counter = 0
headers = []
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
for line in lines:
    if counter == 0:
        headers = re.sub('\<[^>]*\>', " ", line)
        headers = re.findall("Заболели|Умерли|Вылечились|Активные случаи", headers)
    else:
        temp = re.sub('<.*?>', ';', line)
        temp = re.sub("\(.*?\)", '', temp)
        temp = re.sub(';+', ';', temp)
        temp = temp[1: len(temp) - 1]
        temp = re.sub('\s(?=\d)', '', temp)
        temp = re.sub('(?<=\d)\s', '', temp)
        temp = re.sub('(?<=0)\*', '', temp)
        temp = re.sub('_', '0', temp)

        tmp_split = temp.split(';')
        if len(tmp_split) == 6:
            tmp_split.pop(0)

        country_name = tmp_split[0]
        country_name = re.sub('.*\s\s', '', country_name)

        col1_val = tmp_split[1]
        col2_val = tmp_split[2]
        col3_val = tmp_split[3]
        col4_val = tmp_split[4]

        result_dct[country_name] = [0, 0, 0, 0]
        result_dct[country_name][0] = int(col1_val)
        result_dct[country_name][1] = int(col2_val)
        result_dct[country_name][2] = int(col3_val)
        result_dct[country_name][3] = int(col4_val)
    counter += 1


    # Пятое задание


    output = open('data.csv', 'w')
    w = csv.writer(output, delimiter=";")
    w.writerow(headers)
    for key, value in result_dct.items():
        w.writerow([key, value[0], value[1], value[2], value[3]])
    output.close()


    # Шестое задание

    target_country = input("Введите название страны: ")
    try:
        print(result_dct[target_country])
        print("Заболели|Умерли|Вылечились|Активные случаи")
    except Exception:
        print("Введите корректное значение ")