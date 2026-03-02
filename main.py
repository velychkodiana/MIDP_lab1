import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


# 1.1 Завантаження набору даних
df = pd.read_csv('bmw_global_sales_dataset.csv')
print("ПЕРШІ 5 РЯДКІВ")
print(df.head())

# 1.2 Очищення набору даних (залишаємо 8 колонок)
columns_to_keep = ['year', 'country', 'model', 'engine_type', 'price_usd',
                   'marketing_spend_usd', 'units_sold', 'competition_index']
df = df[columns_to_keep]

# 1.3 Обробка пропущених значень
# Видаляємо рядки, де ціна або кількість проданих авто є порожніми (якщо такі є)
df = df.dropna(subset=['price_usd', 'units_sold'])

# 1.4 Форматування даних
# Булева ознака: чи є авто дорогим (ціна > 80,000)
df['is_premium'] = df['price_usd'] > 80000
# Також перетворимо рік у формат дати (хоча там лише рік)
df['year_dt'] = pd.to_datetime(df['year'], format='%Y')


# 2. ДОСЛІДЖЕННЯ НАБОРУ ДАНИХ

# 2.1 Загальна кількість рядків
total_rows = len(df)
print(f"\nКількість записів після очищення: {total_rows}")

# 2.2 Робота з числовими показниками
# Фільтр: ціна більше за 70,000
high_price_df = df[df['price_usd'] > 70000].copy()
print(f"Кількість дорогих авто (>70k): {len(high_price_df)}")

# Середнє значення витрат на маркетинг для цієї вибірки
avg_marketing = high_price_df['marketing_spend_usd'].mean()
print(f"Середні витрати на маркетинг для дорогих авто: {avg_marketing:.2f}")

# Топ-10 за кількістю продажів серед дорогих авто
top_10_sales = high_price_df.nlargest(10, 'units_sold')
print("\nТоп-10 записів за кількістю продажів (з дорогих):")
print(top_10_sales[['model', 'country', 'units_sold']])

# 2.3 Дослідження категорій та тексту
# Точний збіг: Країна - USA
usa_count = len(df[df['country'] == 'USA'])

# Частковий збіг: моделі серії "X" (X1, X5 і т.д.)
x_models_df = df[df['model'].str.contains('X')].copy()

# Комбіновані підрахунки
cond1 = df['country'] == 'USA'
cond2 = df['model'].str.contains('X')

both = len(df[cond1 & cond2])
only_1 = len(df[cond1 & ~cond2])
neither = len(df[~cond1 & ~cond2])

print(f"\nUSA: {usa_count}")
print(f"USA та модель X: {both}")
print(f"Тільки USA (без X): {only_1}")
print(f"Ні USA, ні модель X: {neither}")

# 2.4 Дослідження числових діапазонів
# Кількість записів, за 2021 рік
year_2021_count = len(df[df['year'] == 2021])

# Кількість продажів у діапазоні від 500 до 1000 за одну угоду
range_count = len(df[(df['units_sold'] >= 500) & (df['units_sold'] <= 1000)])

print(f"\nЗаписів за 2021 рік: {year_2021_count}")
print(f"Продажі в діапазоні 500-1000: {range_count}")
print(f"Чи більше за 2021 рік ніж у діапазоні? {year_2021_count > range_count}")

# 2.5 Комбіновані фільтри
# "Значущі за ціною" - де продажі > 800
significant_df = df[df['units_sold'] > 800].copy()
print("\nТоп-5 значущих за ціною:")
print(significant_df.nlargest(5, 'price_usd')[['model', 'price_usd', 'units_sold']])

# Медіана ціни для топ-10 за витратами на маркетинг
median_price_top_marketing = df.nlargest(10, 'marketing_spend_usd')['price_usd'].median()
print(f"Медіанна ціна топ-10 за маркетингом: {median_price_top_marketing}")

# 2.6 Порівняння груп
# Дві категорії: Австралія та Франція
df_aus = df[df['country'] == 'Australia'].copy()
df_fra = df[df['country'] == 'France'].copy()

# Створення порівняльної таблиці
comparison_df = pd.DataFrame({
    'category_name': ['Australia', 'France'],
    'total_records': [len(df_aus), len(df_fra)]
})

# Додавання середнього значення ціни
comparison_df['average_price'] = [df_aus['price_usd'].mean(), df_fra['price_usd'].mean()]
print("\nПорівняння груп:")
print(comparison_df)

# 2.7 Комплексні завдання
# Складний фільтр: (США та Австралія) ТА ціна > 50000 ТА НЕ Petrol
complex_filter = df[((df['country'] == 'USA') | (df['country'] == 'Australia')) &
                    (df['price_usd'] > 50000) &
                    (df['engine_type'] != 'Petrol')]
print(f"\nКількість записів за складним фільтром: {len(complex_filter)}")



# Графік: Сумарні продажі по роках
df.groupby('year')['units_sold'].sum().plot(kind='bar', color='pink')
plt.title('Загальні продажі BMW по роках')
plt.xlabel('Рік')
plt.ylabel('Продано одиниць')
plt.tight_layout()
plt.savefig('sales_plot.png')
print("\nГрафік збережено як 'sales_plot.png'")