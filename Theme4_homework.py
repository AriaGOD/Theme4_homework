import tkinter as tk # Импорт библиотеки для отрисовки
class HanoiTower:
    def __init__(self, num_disks, num_towers, canvas):
        # Инициализация кол-ва дисков и стержней
        self.num_disks = num_disks
        self.num_towers = num_towers
        # Создание словаря для хранения (стержень - список дисков)
        self.towers = {i: [] for i in range(1, num_towers + 1)}
        # Инициализация первого стержня с дисками в порядке убывания
        self.towers[1] = list(range(num_disks, 0, -1))
        self.canvas = canvas
        self.disk_width = 20  # ширина
        self.disk_height = 20  # высота
        self.draw_towers()  # отрисовка начального состояния

    def draw_towers(self):
        # Рисует стержни и диск. Очищает холст
        self.canvas.delete("all")
        tower_width = 20
        gap_between_towers = 150
        base_y = 300
        # Рисует стержни
        for i in range(1, self.num_towers + 1):
            x = i * gap_between_towers
            self.canvas.create_rectangle(x - tower_width // 2, 50, x + tower_width // 2, base_y, fill="pink")

            # Рисует диски на каждом стержне
            for j, disk in enumerate(self.towers[i]):
                disk_color = f"#{disk * 30 % 255:02x}{disk * 50 % 255:02x}aa"
                disk_width = self.disk_width * disk + 40  # Определяет ширину диска
                y = base_y - j * self.disk_height  # Размещение дисков друг над другом
                self.canvas.create_rectangle(x - disk_width // 2, y - self.disk_height,
                                             x + disk_width // 2, y, fill=disk_color)

        # Обновление холста
        self.canvas.update()
    def move_disk(self, source, target):
        # Перемещает верхний диск
        disk = self.towers[source].pop()
        self.towers[target].append(disk)
        self.draw_towers()
        print(f'Блин {disk}: Стержень {source} -> Стержень {target}')
        # Записывает перемещения в файл
        with open('Решение.txt', 'a') as file:
            file.write(f'Блин {disk}: Стержень {source} -> Стержень {target}\n')

    def solve(self, n, source, target, support):
        # Двигает диски с использованием стержня support
        if n == 1:
            # Один диск -  перемещает его на target стержень
            self.move_disk(source, target)
        else:
            if self.num_towers == 3:
                # Если 3 стержня - классический алгоритм решения
                self.solve(n - 1, source, support, target)
                self.move_disk(source, target)
                self.solve(n - 1, support, target, source)
            else:
                # Больше стержней - более сложное решение (+ возможность промежуточного хранения)
                self.solve(n - 1, source, support, target)
                self.move_disk(source, target)
                self.solve(n - 1, support, target, source)
def get_input():
    # Запрос у юзера кол-ва дисков и стержней, проверка корректности ввода
    while True:
        try:
            num_disks = int(input('Введите количество дисков (1-8): '))
            num_towers = int(input('Введите количество стержней (не менее 3): '))
            if 1 <= num_disks <= 8 and num_towers >= 3:
                return num_disks, num_towers
            else:
                print("Даны неверные переменные")
        except ValueError:
            print("Введите числа")
def main():
    # Создает окно с холстом
    root = tk.Tk()
    root.title("Ханойская башня")
    canvas = tk.Canvas(root, width=1500, height=600, bg="white")
    canvas.pack()
    # Получение данных от юзера
    num_disks, num_towers = get_input()
    print(f'Решение для {num_disks} дисков и {num_towers} стержней:')
    # Создает и очищает файл, записывая в него начальные условия
    with open('Решение.txt', 'w') as file:
        file.write(f'Решение для {num_disks} дисков и {num_towers} стержней:\n')
    # Создает экземпляр класса "HanoiTower" и решает задачу
    hanoi = HanoiTower(num_disks, num_towers, canvas)
    hanoi.solve(num_disks, 1, 3, 2) # Старт с первого стержня, конец на третьем, вспомогательный — второй

    # Запуск окна с холстом
    root.mainloop()

if __name__ == "__main__":
    main()
