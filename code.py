import pygame   # Для создания самого симулятора перекрестка
import os   # Для поиска изображений в папке
import random   # Для случайного выбора изображения машин
import sys  # Для поиска папки с машинами

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симулятор перекрестка") # Название окна

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)

# Параметры машин
CAR_WIDTH, CAR_HEIGHT = 50, 30
ACCELERATION = 0.3
DECELERATION = 1    # Увеличено торможение
MAX_HORIZONTAL_SPEED = 6    # Повышена скорость
MAX_VERTICAL_SPEED = 8  # Повышена скорость
SAFE_DISTANCE = 70 # Увеличена дистанция
STOP_DISTANCE = 100

# Параметры светофоров
light_radius = 15   # Увеличен радиус
light_colors = [RED, YELLOW, GREEN]
current_light = 0  # 0 - красный, 1 - желтый, 2 - зеленый

# Координаты светофоров
traffic_lights = {
    "horizontal": {"x": WIDTH // 2 - 60, "y": HEIGHT // 2 - 20},
    "vertical": {"x": WIDTH // 2 - 20, "y": HEIGHT // 2 - 60}, 
}

# Загрузка изображений машин
CARS_FOLDER = os.path.join(os.path.dirname(sys.argv[0]), "cars")
horizontal_car_images = []
vertical_car_images = []

if os.path.exists(CARS_FOLDER):
    formats = ('.png', '.jpg', '.jpeg') # Форматы изображений машин
    for filename in os.listdir(CARS_FOLDER):    # Перебор всех файлов
        if filename.lower().endswith(formats):  # Проверка на заданные форматы
            try:
                image_path = os.path.join(CARS_FOLDER, filename)    # Полный путь к изображению
                image = pygame.image.load(image_path)
                
                # Удаление белого фона
                if image.get_alpha() is None:   # Проверка на прозрачность
                    image = image.convert_alpha()   # Преобразование изображения в формат с альфа-каналом (та же прозрачность)
                
                for y in range(image.get_height()): 
                    for x in range(image.get_width()):
                        color = image.get_at((x, y))    # Получение цвета пикселя
                        if color.r > 255 - 30 and color.g > 255 - 30 and color.b > 255 - 30:    # Проверка на белый или почти белый цвет
                            image.set_at((x, y), (255, 255, 255, 0))    # Пиксель становится прозрачным
                
                # Масштабирование горизонтальных машин
                image_h = pygame.transform.scale(image, (CAR_HEIGHT, CAR_WIDTH))
                image_h = pygame.transform.rotate(image_h, -90) # Поворот изображения на 90 градусов
                
                # Масштабирование вертикальных машин
                image_v = pygame.transform.scale(image, (CAR_HEIGHT, CAR_WIDTH))
                image_v = pygame.transform.rotate(image_v, 180) # Поворот изображения на 180 градусов
                
                # Добавление машин в массив
                horizontal_car_images.append(image_h)
                vertical_car_images.append(image_v)
            except Exception as e:
                pass

# Создание горизонтальных машин
horizontal_cars = []
for i in range(2):
    car_image = random.choice(horizontal_car_images) if horizontal_car_images else None # Случайный выбор изображений из массива horizontal_car_images
    horizontal_cars.append({
        "x": i * -300,  # Начальная координата по X
        "y": HEIGHT // 2 - 15,  # Начальная координата по Y
        "speed": 0, # Начальная скорость
        "image": car_image,
        "passed_crossing": False,   # Флаг "перекресток пересечен"
        "on_crossing": False    # Флаг "до или на перекрестке"
    })

# Создание вертикальных машин
vertical_cars = []
for i in range(2):
    car_image = random.choice(vertical_car_images) if vertical_car_images else None # Случайный выбор изображений из массива vertical_car_images
    vertical_cars.append({
        "x": WIDTH // 2 - 15,   # Начальная координата по X
        "y": i * -300,  # Начальная координата по Y
        "speed": 0, # Начальная скорость
        "image": car_image,
        "passed_crossing": False,   # Флаг "перекресток пересечен"
        "on_crossing": False    # Флаг "до или на перекрестке"
    })

# Таймер для смены светофора
SWITCH_INTERVAL = 3000
last_switch_time = pygame.time.get_ticks()

# Главный игровой цикл
running = True
while running:
    screen.fill(WHITE)  # Заливка экрана белым цветом
    current_time = pygame.time.get_ticks()  # Текущее время

    for event in pygame.event.get():
        # Если окно закрывается, то цикл завершается
        if event.type == pygame.QUIT:
            running = False
    
    # Рисуем перекресток
    pygame.draw.rect(screen, GRAY, (0, HEIGHT // 2 - 40, WIDTH, 80))
    pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 40, 0, 80, HEIGHT))

    # Рисуем светофоры
    # Горизонтальные светофоры
    pygame.draw.circle(screen, light_colors[current_light],
        (traffic_lights["horizontal"]["x"], traffic_lights["horizontal"]["y"] + 80), light_radius)
    pygame.draw.circle(screen, light_colors[current_light],
        (traffic_lights["horizontal"]["x"] + 120, traffic_lights["horizontal"]["y"] - 40), light_radius)
    
    # Вертикальные светофоры (противоположный сигнал)
    vertical_light = 0 if current_light == 2 else (2 if current_light == 0 else 1)
    pygame.draw.circle(screen, light_colors[vertical_light],
        (traffic_lights["vertical"]["x"] - 40, traffic_lights["vertical"]["y"]), light_radius)
    pygame.draw.circle(screen, light_colors[vertical_light],
        (traffic_lights["vertical"]["x"] + 80, traffic_lights["vertical"]["y"] + 120), light_radius)
    
    # Обновление светофора
    if current_time - last_switch_time > SWITCH_INTERVAL:   # Проверка на прошедшее время
        current_light = (current_light + 1) % 3 # Переключение цвета по порядку
        last_switch_time = current_time # Сброс таймера
    
    # Обновление движения горизонтальных машин
    for i, car in enumerate(horizontal_cars):   # Все горизонтальные машины
        crossing_start = WIDTH // 2 - 40    # Начало перекрестка (левая граница)
        crossing_end = WIDTH // 2 + 40  # Конец перекрестка (правая граница)
        
        # Проверка, есть ли другая машина на перекрестке
        if car["x"] + CAR_WIDTH > crossing_start and car["x"] < crossing_end:
            car["on_crossing"] = True
        else:
            car["on_crossing"] = False
        
        # Проверка, проехала ли машина перекресток
        if car["x"] + CAR_WIDTH > crossing_end:
            car["passed_crossing"] = True
        
        # Стоп-линия
        stop_zone = WIDTH // 2 - STOP_DISTANCE
        
        # Если машина на перекрестке или проехала его,
        if car["passed_crossing"] or car["on_crossing"]:
            can_move = True # то может ехать (без остановки до конца)
        else:
            # Едет только на зеленый
            if current_light == 2:
                can_move = True
            else:
                # Если не зеленый - можно ехать после пересечения стоп-линии
                can_move = car["x"] + CAR_WIDTH < stop_zone

        # Проверка безопасного расстояния
        if i > 0 and not car["passed_crossing"] and not car["on_crossing"]: # Проверка флагов или то, что это не первая машина
            distance = horizontal_cars[i - 1]["x"] - (car["x"] + CAR_WIDTH) # Расстояние до машины спереди
            if distance < SAFE_DISTANCE: # Если расстояние меньше безопасного,
                can_move = False    # то машине запрещеное движение

        # Ускорение или замедление
        if can_move:
            car["speed"] = min(car["speed"] + ACCELERATION, MAX_HORIZONTAL_SPEED)
        else:
            car["speed"] = max(car["speed"] - DECELERATION, 0)
        
        # Обновление позиции
        car["x"] += car["speed"]
        if car["x"] > WIDTH: # Проверка, выехала ли машина за правую границу экрана
            car["x"] = -CAR_WIDTH - random.randint(50, 150) # Перемещение машины влево (за экран)
            # Сброс флагов
            car["passed_crossing"] = False
            car["on_crossing"] = False
            # Смена изображения машины на другое случайное
            if horizontal_car_images:
                car["image"] = random.choice(horizontal_car_images)
            car["speed"] = MAX_HORIZONTAL_SPEED
    
    # Обновление движения вертикальных машин
    for i, car in enumerate(vertical_cars): # Все вертикальные машины
        crossing_start = HEIGHT // 2 - 40   # Начало перекрестка (верхняя граница)
        crossing_end = HEIGHT // 2 + 40 # Конец перекрестка (нижняя граница)
        
        # Проверка, есть ли другая машина на перекрестке
        if car["y"] + CAR_HEIGHT > crossing_start and car["y"] < crossing_end:
            car["on_crossing"] = True
        else:
            car["on_crossing"] = False
        
        # Проверка, проехала ли машина перекресток
        if car["y"] + CAR_HEIGHT > crossing_end:
            car["passed_crossing"] = True
        
        # Стоп-линия
        stop_zone = HEIGHT // 2 - STOP_DISTANCE
        
        # Если машина на перекрестке или проехала его,
        if car["passed_crossing"] or car["on_crossing"]:
            can_move = True # то может ехать (без остановки до конца)
        else:
            # Стоит на месте
            if current_light == 0:
                can_move = True
            else:
                # Если не зеленый - можно ехать после пересечения стоп-линии
                can_move = car["y"] + CAR_HEIGHT < stop_zone

        # Проверка безопасного расстояния
        if i > 0 and not car["passed_crossing"] and not car["on_crossing"]: # Проверка флагов или то, что это не первая машина
            distance = vertical_cars[i - 1]["y"] - (car["y"] + CAR_HEIGHT)  # Расстояние до машины спереди
            if distance < SAFE_DISTANCE:    # Если расстояние меньше безопасного,
                can_move = False    # то машине запрещеное движение
        
        # Ускорение или замедление
        if can_move:
            car["speed"] = min(car["speed"] + ACCELERATION, MAX_VERTICAL_SPEED)
        else:
            car["speed"] = max(car["speed"] - DECELERATION, 0)
        
        # Обновление позиции
        car["y"] += car["speed"]
        if car["y"] > HEIGHT:   # Проверка, выехала ли машина за нижнюю границу экрана
            car["y"] = -CAR_HEIGHT - random.randint(50, 150)    # Перемещение машины наверх (за экран)
            # Сброс флагов
            car["passed_crossing"] = False
            car["on_crossing"] = False
            # Смена изображения машины на другое случайное
            if vertical_car_images:
                car["image"] = random.choice(vertical_car_images)
            car["speed"] = MAX_VERTICAL_SPEED
    
    # Рисуем машины
    # Горизонтальные машины
    for car in horizontal_cars:
        if car["image"] is not None:
            screen.blit(car["image"], (car["x"], car["y"]))
        else:
            pygame.draw.rect(screen, BLUE, (car["x"], car["y"], CAR_WIDTH, CAR_HEIGHT))
    
    # Вертикальные машины
    for car in vertical_cars:
        if car["image"] is not None:
            screen.blit(car["image"], (car["x"], car["y"]))
        else:
            pygame.draw.rect(screen, BLUE, (car["x"], car["y"], CAR_HEIGHT, CAR_WIDTH))

    pygame.display.flip()   # Обновление экрана
    pygame.time.delay(30)   # Задержка между кадрами

pygame.quit()   # Завершение работы pygame