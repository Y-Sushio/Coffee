import sqlite3

with sqlite3.connect("Coffee.sqlite") as data_base:
    cursor = data_base.cursor()

    dict_grade = {"Арабика": ("Вкусный", 350), "Робуста": ("Очень вкусный", 450),
                  "Либерика": ("Неплохой кофе", 150), "Эксцельса": ("Хороший кофе", 275)}

    count = 1
    for grade in list(dict_grade.keys()):
        for degree_roasting in ["Слабая", "Средняя", "Сильная"]:
            for volume in [50, 100, 150, 200]:
                for grind in [False, True]:
                    cursor.execute("""INSERT INTO Coffee VALUES
                    (?, ?, ?, ?, ?, ?, ?)""", (count, grade, degree_roasting, grind, dict_grade[grade][0],
                                               dict_grade[grade][1] * (volume / 100) + 25 * (volume / 100) if grind else
                                               dict_grade[grade][1] * (volume / 100), volume))

                    count += 1
