# HH.ru Data Fetcher and Converter

Программа для получения данных о вакансиях с HH.ru и конвертации их в различные форматы.

# Получение данных с HH.ru

python app.py fetch --text "Ключевые слова" --experience Уровень_опыта --output имя_файла.json

Параметры:
--text (обязательный): Поисковый запрос (например, "Python developer")
--experience: Уровень опыта:
noExperience - Нет опыта
between1And3 - От 1 года до 3 лет
between3And6 - От 3 до 6 лет
moreThan6 - Более 6 лет
--output: Имя выходного JSON-файла (по умолчанию: vacancies.json)

# Конвертация JSON в CSV

python app.py convert входной_файл.json --all --output выходной_файл.csv
