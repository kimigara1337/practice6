import pandas as pd
import os
import json

# Оригинальный датасет https://www.kaggle.com/datasets/ekibee/car-sales-information

# 1. Загрузка набора данных
df = pd.read_csv('all_regions_trimmed.csv')

# 2. Анализ набора данных

# а) Размер файла на диске
file_size = os.path.getsize('all_regions_trimmed.csv') / (1024 * 1024)  # Размер в мегабайтах
print(f"Объем файла на диске: {file_size:.2f} MB")

# б) Размер набора данных в памяти
memory_usage = df.memory_usage(deep=True).sum() / (1024 * 1024)  # в мегабайтах
print(f"Объем памяти, занимаемый набором данных: {memory_usage:.2f} MB")

# в) Статистика по колонкам
memory_per_column = df.memory_usage(deep=True) / (1024 * 1024)  # В МБ
data_types = df.dtypes

# Вывод информации по колонкам
columns_stats = pd.DataFrame({
    'memory_mb': memory_per_column,
    'memory_percent': memory_per_column / memory_usage * 100,
    'data_type': data_types
})

print(columns_stats)

# 3. Сортировка по занимаемому объему памяти и вывод в файл
sorted_columns_stats = columns_stats.sort_values(by='memory_mb', ascending=False)

# Преобразуем столбцы с типом "object" в строки (если это необходимо)
for col in sorted_columns_stats.columns:
    if sorted_columns_stats[col].dtype == 'object':
        sorted_columns_stats[col] = sorted_columns_stats[col].astype(str)

# Сохранение статистики в JSON файл
sorted_columns_stats.to_json('columns_stats.json', orient='records')

# 4. Преобразование колонок с типом «object» в категориальные, если количество уникальных значений < 50%
for col in df.select_dtypes(include=['object']).columns:
    if df[col].nunique() / len(df) < 0.5:
        df[col] = df[col].astype('category')

# 5. Понижающее преобразование типов для «int» колонок
for col in df.select_dtypes(include=['int']).columns:
    df[col] = pd.to_numeric(df[col], downcast='integer')

# 6. Понижающее преобразование типов для «float» колонок
for col in df.select_dtypes(include=['float']).columns:
    df[col] = pd.to_numeric(df[col], downcast='float')

# 7. Повторный анализ набора данных
new_memory_usage = df.memory_usage(deep=True).sum() / (1024 * 1024)
new_columns_stats = pd.DataFrame({
    'memory_mb': df.memory_usage(deep=True) / (1024 * 1024),
    'memory_percent': df.memory_usage(deep=True) / new_memory_usage * 100,
    'data_type': df.dtypes
})

print(f"Объем памяти после оптимизации: {new_memory_usage:.2f} MB")
print(new_columns_stats)

# 8. Выбор 10 колонок для дальнейшей работы и использование чанков
selected_columns = ['brand', 'name', 'bodyType', 'fuelType', 'year', 'mileage', 'transmission', 'power', 'price', 'location']

# Чтение данных с использованием чанков
chunksize = 50000
chunk_list = []  # Список для хранения чанков, если нужно объединить их позже

for chunk in pd.read_csv('all_regions_trimmed.csv', usecols=selected_columns, chunksize=chunksize):
    # Обработка чанков (например, удаление пропусков)
    chunk = chunk.dropna()
    chunk_list.append(chunk)

# Объединение всех чанков в один DataFrame
filtered_df = pd.concat(chunk_list, axis=0)

# Сохранение поднабора в новый файл
filtered_df.to_csv('filtered_data.csv', index=False)

print(f"Данные сохранены в файл 'filtered_data.csv'.")
