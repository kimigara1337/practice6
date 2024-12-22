import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Загрузка оптимизированного набора данных
df = pd.read_csv('all_regions_trimmed.csv')

# Настройка стилей для графиков
sns.set(style="whitegrid")

# Создание папки для сохранения графиков (если она не существует)
if not os.path.exists('plots'):
    os.makedirs('plots')

# 1. Линейный график: Сравнение цен по годам (year vs price)
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='year', y='price', marker='o', color='b')
plt.title('Зависимость цены от года выпуска')
plt.xlabel('Год выпуска')
plt.ylabel('Цена (в рублях)')
plt.savefig('plots/lineplot_year_vs_price.png')  # Сохранение графика
plt.close()

# 2. Столбчатая диаграмма: Средняя цена по типу кузова (bodyType vs price)
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='bodyType', y='price', estimator='mean', palette='viridis')
plt.title('Средняя цена по типу кузова')
plt.xlabel('Тип кузова')
plt.ylabel('Средняя цена (в рублях)')
plt.xticks(rotation=45, ha="right")
plt.savefig('plots/barplot_bodyType_vs_price.png')  # Сохранение графика
plt.close()

# 3. Круговая диаграмма: Распределение автомобилей по типу топлива (fuelType)
plt.figure(figsize=(8, 8))
fuel_type_counts = df['fuelType'].value_counts()
plt.pie(fuel_type_counts, labels=fuel_type_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set2"))
plt.title('Распределение автомобилей по типу топлива')
plt.axis('equal')  # Чтобы диаграмма была круглой
plt.savefig('plots/pie_fuelType_distribution.png')  # Сохранение графика
plt.close()

# 4. Корреляционная матрица: Корреляция между числовыми признаками
plt.figure(figsize=(10, 6))
correlation_matrix = df[['year', 'mileage', 'power', 'price']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=1)
plt.title('Корреляционная матрица')
plt.savefig('plots/heatmap_correlation_matrix.png')  # Сохранение графика
plt.close()

# 5. Гистограмма: Распределение цен на автомобили (price)
plt.figure(figsize=(10, 6))
sns.histplot(df['price'], bins=30, kde=True, color='skyblue')
plt.title('Распределение цен на автомобили')
plt.xlabel('Цена (в рублях)')
plt.ylabel('Частота')
plt.savefig('plots/histogram_price_distribution.png')  # Сохранение графика
plt.close()

# 6. Диаграмма рассеяния: Зависимость мощности от пробега (power vs mileage)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='mileage', y='power', hue='fuelType', palette='Set1', marker='o')
plt.title('Зависимость мощности от пробега')
plt.xlabel('Пробег (км)')
plt.ylabel('Мощность (л.с.)')
plt.legend(title='Тип топлива')
plt.savefig('plots/scatter_mileage_vs_power.png')  # Сохранение графика
plt.close()

# 7. Столбчатая диаграмма: Средний пробег по типу трансмиссии (transmission vs mileage)
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='transmission', y='mileage', estimator='mean', palette='Blues')
plt.title('Средний пробег по типу трансмиссии')
plt.xlabel('Тип трансмиссии')
plt.ylabel('Средний пробег (км)')
plt.savefig('plots/barplot_transmission_vs_mileage.png')  # Сохранение графика
plt.close()

