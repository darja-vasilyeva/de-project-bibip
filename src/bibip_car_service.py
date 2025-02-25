from datetime import datetime
from decimal import Decimal
from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale


class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        # Шаг 1: Прочитать существующий индекс моделей
        model_index_file_name = self.root_directory_path + '/model_index.txt'
        try:
            with open(model_index_file_name, "r") as f:
                model_index_lines = f.readlines()
        except FileNotFoundError:
            open(model_index_file_name, 'w').close()
            model_index_lines = []

        # Шаг 2: Вставить новую модель в индекс, в правильном порядке
        new_model_index_lines = list()
        for model_index_line in model_index_lines:
            model_id_and_line_num = str.split(model_index_line, ',')
            model_id = model_id_and_line_num[0]
            if model_id == model.id:
                # модель уже существует
                return model
            line_num = int(model_id_and_line_num[1])
            new_model_index_lines.append([model_id, line_num])

        new_model_index_lines.append([model.index(),
                                     len(model_index_lines) + 1])
        new_model_index_lines.sort()

        # Шаг 3: Очистить и записать индекс в одно действие
        with open(model_index_file_name, 'w') as f:
            for model_id_and_line_num1 in new_model_index_lines:
                record = model_id_and_line_num1[0] + ',' \
                 + str(model_id_and_line_num1[1]) + '\n'
                f.write(record)

        # Шаг 4: Записать модель в файл (добавить новую строку,
        #  выравнивая до 100+2 символa)
        model_file_name = self.root_directory_path + '/models.txt'
        record = (str(model.id) + ',' + model.name + ','
                  + model.brand).ljust(100) + '\n'
        with open(model_file_name, "a") as f:
            f.write(record)

        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        # Шаг 1: Прочитать существующий индекс автомобилей
        car_index_file_name = self.root_directory_path + '/car_index.txt'
        try:
            with open(car_index_file_name, "r") as f:
                car_index_lines = f.readlines()
        except FileNotFoundError:
            open(car_index_file_name, 'w').close()
            car_index_lines = []

        # Шаг 2: Вставить новый автомобиль в индекс, в правильном порядке
        new_car_index_lines = list()
        for car_index_line in car_index_lines:
            vin_and_line_num = str.split(car_index_line, ',')
            vin = vin_and_line_num[0]
            if vin == car.vin:
                # машина уже существует
                return car
            line_num = int(vin_and_line_num[1])
            new_car_index_lines.append([vin, line_num])

        new_car_index_lines.append([car.vin, len(car_index_lines) + 1])
        new_car_index_lines.sort()

        # Шаг 3: Очистить и записать индекс в одно действие
        with open(car_index_file_name, 'w') as f:
            for vin_and_line_num in new_car_index_lines:
                vin = vin_and_line_num[0]
                line_number = vin_and_line_num[1]
                record = vin + ',' + str(line_number) + '\n'
                f.write(record)

        # Шаг 4: Записать автомобиль в файл (добавить новую строку, выравнивая до 100+2 символa)
        car_file_name = self.root_directory_path + '/cars.txt'
        record = (car.vin + ','
                  + str(car.model) + ','
                  + str(car.price) + ','
                  + str(car.date_start.date()) + ','
                  + car.status).ljust(100) + '\n'
        with open(car_file_name, "a") as f:
            f.write(record)

        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car | None:
        # # Шаг 1: Прочитать существующий индекс автомобилей
        car_index_file_name = self.root_directory_path + '/car_index.txt'
        try:
            with open(car_index_file_name, "r") as f:
                car_index_lines = f.readlines()
        except FileNotFoundError:
            open(car_index_file_name, 'w').close()
            car_index_lines = []
        # Шаг 2: Найти строку с автомобилем, который продается            
        car_line = None
        for car_index_line in car_index_lines:
            vin_and_line_num = str.split(car_index_line, ',')
            vin = vin_and_line_num[0]
            if vin == sale.car_vin:
                car_line = int(vin_and_line_num[1])
                break
        if car_line is None:
            print('Автомобиль с указанным VIN отсутствует в базе автомобилей')
            return None

        # Шаг 3: Прочитать запись автомобиля по номеру строки
        #  (все строки имеют длину 100+2 символa)
        car_file_name = self.root_directory_path + '/cars.txt'
        try:
            with open(car_file_name, "r") as f:
                f.seek((car_line - 1) * 102)
                car_record = f.read(100)
        except FileNotFoundError:
            open(car_file_name, 'w').close()
            car_record = ''

        # Шаг 4: Обновить статус автомобиля на продано
        car_record_tokens = car_record.strip().split(',')
        if len(car_record_tokens) < 5:  # возможно пустой или повреждённый файл
            return None
        car_record_tokens[4] = CarStatus.sold

        # Шаг 5: Записать обновленную запись автомобиля по номеру строки
        #  (все строки имеют длину 100+2 символa)
        with open(car_file_name, "r+") as f:
            f.seek((car_line - 1) * 102)
            record = (car_record_tokens[0] + ','
                      + car_record_tokens[1] + ','
                      + car_record_tokens[2] + ','
                      + car_record_tokens[3] + ','
                      + car_record_tokens[4]).ljust(100) + '\n'
            f.write(record)

        # Шаг 6: Прочитать существующий индекс продаж
        sell_index_file_name = self.root_directory_path + '/sales_index.txt'
        try:
            with open(sell_index_file_name, "r") as f:
                sell_index_lines = f.readlines()
        except FileNotFoundError:
            open(sell_index_file_name, 'w').close()
            sell_index_lines = []

        # Шаг 7: Вставить новую продажу в индекс, в правильном порядке
        new_sales_index_lines = list()
        sales_line_num = None
        for car_index_line in sell_index_lines:
            vin_and_line_num = str.split(car_index_line, ',')
            vin = vin_and_line_num[0]
            line_num = int(vin_and_line_num[1])
            if vin == sale.car_vin:
                sales_line_num = int(vin_and_line_num[1])
            new_sales_index_lines.append([vin, line_num])

        # Шаг 8: Если продажа не существует, добавить ее в индекс
        #  и основной файл
        if sales_line_num is None:
            new_sales_index_lines.append([sale.index(),
                                         len(sell_index_lines) + 1])
            new_sales_index_lines.sort()

            # Шаг 3.1: Очистить и записать индекс в одно действие
            with open(sell_index_file_name, 'w') as f:
                for new_sales_index_line in new_sales_index_lines:
                    record = new_sales_index_line[0] + ',' \
                     + str(new_sales_index_line[1]) + '\n'
                    f.write(record)

            # Шаг 3.2: Записать продажу в файл (добавить новую строку,
            #  выравнивая до 100+2 символa)
            sales_file_name = self.root_directory_path + '/sales.txt'
            record = (sale.sales_number + ','
                      + sale.car_vin + ','
                      + str(sale.sales_date.date()) + ','
                      + str(sale.cost)).ljust(100) + '\n'
            with open(sales_file_name, "a") as f:
                f.write(record)

        return Car(
            vin=car_record_tokens[0],
            model=int(car_record_tokens[1]),
            price=Decimal(car_record_tokens[2]),
            date_start=datetime.fromisoformat(car_record_tokens[3]),
            status=CarStatus(car_record_tokens[4])
        )

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        # Шаг 1: Прочитать существующий файл с автомобилями
        car_file_name = self.root_directory_path + '/cars.txt'
        try:
            with open(car_file_name, "r") as f:
                car_lines = f.readlines()
        except FileNotFoundError:
            open(car_file_name, 'w').close()
            car_lines = []

        # Шаг 2: Перебрать строки и выбрать только те,
        #  которые имеют статус 'status'
        cars = list()
        for car_line in car_lines:
            car_record = car_line.strip().split(',')
            if CarStatus(car_record[4]) == CarStatus.available:  # status:
                cars.append(Car(
                    vin=car_record[0],
                    model=int(car_record[1]),
                    price=Decimal(car_record[2]),
                    date_start=datetime.fromisoformat(car_record[3]),
                    status=CarStatus(car_record[4])
                ))
        # cars.sort()
        return cars

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        # Шаг 1: Прочитать существующий индекс автомобилей
        car_index_file_name = self.root_directory_path + '/car_index.txt'
        try:
            with open(car_index_file_name, "r") as f:
                car_index_lines = f.readlines()
        except FileNotFoundError:
            open(car_index_file_name, 'w').close()
            car_index_lines = []

        # Шаг 2: Найти номер строки с автомобилем по VIN
        car_line_num = None
        for sales_index_line in car_index_lines:
            vin_and_line_num = str.split(sales_index_line, ',')
            vin_index = vin_and_line_num[0]
            line_num = int(vin_and_line_num[1])
            if vin_index == vin:
                car_line_num = line_num
                break
        if car_line_num is None:
            print('Автомобиль с указанным VIN не найден')
            return None

        # Шаг 3: Прочитать запись автомобиля по номеру строки 
        # (все строки имеют длину 100+2 символa)
        car_file_name = self.root_directory_path + '/cars.txt'
        with open(car_file_name, "r") as f:
            f.seek((car_line_num - 1) * 102)
            car_record = f.read(100)
        car_record = car_record.strip().split(',')

        # Шаг 4: Прочитать существующий индекс моделей
        model_index_file_name = self.root_directory_path + '/model_index.txt'
        try:
            with open(model_index_file_name, "r") as f:
                model_index_lines = f.readlines()
        except FileNotFoundError:
            open(model_index_file_name, 'w').close()
            model_index_lines = []

        # Шаг 5: Найти номер строки с моделью по ID
        model_id = int(car_record[1])
        model_line_num = None
        for sales_index_line in model_index_lines:
            model_id_and_line_num = str.split(sales_index_line, ',')
            model_id_index = int(model_id_and_line_num[0])
            if model_id_index == model_id:
                model_line_num = int(model_id_and_line_num[1])
                break
        if model_line_num is None:
            print('Автомобиль с указанным VIN не найден')
            return None

        # Шаг 6: Прочитать запись модели по номеру строки 
        # (все строки имеют длину 100+2 символa)
        model_file_name = self.root_directory_path + '/models.txt'
        with open(model_file_name, "r") as f:
            f.seek((model_line_num - 1) * 102)
            model_record = f.read(100)
        model_record = model_record.strip().split(',')

        # Шаг 7: Прочитать существующий индекс продаж
        sales_index_file_name = self.root_directory_path + '/sales_index.txt'
        try:
            with open(sales_index_file_name, "r") as f:
                sales_index_lines = f.readlines()
        except FileNotFoundError:
            open(sales_index_file_name, 'w').close()
            sales_index_lines = []

        # Шаг 8: Найти номер строки с продажей по VIN
        sales_line_num = None
        for sales_index_line in sales_index_lines:
            vin_and_line_num = str.split(sales_index_line, ',')
            vin_index = vin_and_line_num[0]
            line_num = int(vin_and_line_num[1])
            if vin_index == vin:
                sales_line_num = line_num
                break

        # Шаг 9: Прочитать запись продажи по номеру строки, если номер
        # существует (все строки имеют длину 100+2 символa)
        sale_record = None
        if sales_line_num is not None:
            sale_file_name = self.root_directory_path + '/sales.txt'
            with open(sale_file_name, "r") as f:
                f.seek((sales_line_num - 1) * 102)
                sale_record = f.read(100)

        # Шаг 9.1: по умолчанию продажа не найдена
        sales_date = None
        sales_cost = None

        # Шаг 9.2: если продажа найдена
        if sale_record is not None:
            sale_record = sale_record.strip().split(',')
            sales_date = datetime.fromisoformat(sale_record[2])
            sales_cost = Decimal(sale_record[3])

        return CarFullInfo(
            vin=car_record[0],
            car_model_name=model_record[1],
            car_model_brand=model_record[2],
            price=Decimal(car_record[2]),
            date_start=datetime.fromisoformat(car_record[3]),
            status=CarStatus(car_record[4]),
            sales_date=sales_date,
            sales_cost=sales_cost
        )

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car  | None:
        # Шаг 1: Прочитать существующий индекс автомобилей
        car_index_file_name = self.root_directory_path + '/car_index.txt'
        try:
            with open(car_index_file_name, "r") as f:
                car_index_lines = f.readlines()
        except FileNotFoundError:
            open(car_index_file_name, 'w').close()
            car_index_lines = []

        # Шаг 2: Посчитать обновлённый индекс автомобилей
        new_car_index_lines = list()
        car_line_num = None
        for car_index_line in car_index_lines:
            vin_and_line_num = str.split(car_index_line, ',')
            vin_index = vin_and_line_num[0]
            line_num = int(vin_and_line_num[1])
            if vin_index == vin:
                car_line_num = line_num
                new_car_index_lines.append([new_vin, line_num])
            else:
                new_car_index_lines.append([vin_index, line_num])
        if car_line_num is None:
            print('Автомобиль с указанным VIN не найден. Операция не произведена')
            return None                
        new_car_index_lines.sort()

        # Шаг 3: Очистить и записать индекс в одно действие
        with open(car_index_file_name, 'w') as f:
            for new_car_index_line in new_car_index_lines:
                record = new_car_index_line[0] + ',' + str(new_car_index_line[1]) + '\n'
                f.write(record)

        # Шаг 4: Прочитать запись автомобиля по номеру строки (все строки имеют длину 102 символa)
        car_file_name = self.root_directory_path + '/cars.txt'
        with open(car_file_name, "r") as f:
            f.seek((car_line_num - 1) * 102)
            car_record = f.read(100)
        car_record = car_record.strip().split(',')

        # Шаг 5: Обновить VIN в записи автомобиля
        car_record[0] = new_vin

        # Шаг 6: Записать обновленную запись автомобиля по номеру строки (все строки имеют длину 102 символa)
        with open(car_file_name, "r+") as f:
            f.seek((car_line_num - 1) * 102)
            content_to_write = (car_record[0] + ','
                                + car_record[1] + ','
                                + car_record[2] + ','
                                + car_record[3] + ','
                                + car_record[4]
                                ).ljust(100) + '\n'
            f.write(content_to_write)

        return Car(
            vin=car_record[0],
            model=int(car_record[1]),
            price=Decimal(car_record[2]),
            date_start=datetime.fromisoformat(car_record[3]),
            status=CarStatus(car_record[4])
        )

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car | None:
        # Шаг 0: Найти VIN проданного автомобиля
        sold_car_vin = sales_number.split('#')[1]

        # Шаг 1: Прочитать существующий индекс продаж
        sell_index_file_name = self.root_directory_path + '/sales_index.txt'
        try:
            with open(sell_index_file_name, "r") as f:
                sell_index_lines = f.readlines()
        except FileNotFoundError:
            open(sell_index_file_name, 'w').close()
            sell_index_lines = []

        # Шаг 2: Найти номер строки с продажей по VIN
        sales_line_num = None
        new_sales_index_lines = list()
        for sales_index_line in sell_index_lines:
            sales_number_and_line_num = str.split(sales_index_line, ',')
            sales_vin = sales_number_and_line_num[0]
            line_num = int(sales_number_and_line_num[1])
            if sales_vin == sold_car_vin:
                sales_line_num = line_num
            else:
                new_sales_index_lines.append([sales_vin, line_num])

        if sales_line_num is None:
            print('В базе продаж не найден запрошенный VIN')
            return None
        # Шаг 3: Удалить продажу
        last_sales_line_num = len(sell_index_lines)
        if sales_line_num != last_sales_line_num:
            # Если продажа не последняя, то мы можем "затереть" 
            # ее при помощи последней продажи
            # Шаг 3.1.1: Прочитать последнюю продажу
            #  (все строки имеют длину 100+2 символa)
            sell_file_name = self.root_directory_path + '/sales.txt'
            with open(sell_file_name, "r") as f:
                f.seek((last_sales_line_num - 1) * 102)
                last_sell_record = f.read(100)

            # Шаг 3.1.2: Записать последнюю продажу на место удаляемой
            with open(sell_file_name, "r+") as f:
                f.seek((sales_line_num - 1) * 102)
                f.write(last_sell_record)

            # Шаг 3.1.3: Обновить индекс продаж
            last_sell_record_vin = last_sell_record.strip().split(',')[1]
            for i, new_sales_index_line in enumerate(new_sales_index_lines):
                if new_sales_index_line[0] == last_sell_record_vin:
                    new_sales_index_lines[i][1] = sales_line_num
                    break

        # Шаг 4: Очистить и записать индекс в одно действие
        with open(sell_index_file_name, 'w') as f:
            for new_sales_index_line in new_sales_index_lines:
                record = new_sales_index_line[0] + ',' \
                     + str(new_sales_index_line[1]) + '\n'
                f.write(record)

        # Шаг 5: Удалить последнюю строку из файла продаж
        sales_file_name = self.root_directory_path + '/sales.txt'
        with open(sales_file_name, "r+") as f:
            f.seek((last_sales_line_num - 1) * 102) # last_sales_line_num
            f.truncate()

        # Шаг 6: Прочитать индекс существующих автомобилей
        car_index_file_name = self.root_directory_path + '/car_index.txt'
        try:
            with open(car_index_file_name, "r") as f:
                car_index_lines = f.readlines()
        except FileNotFoundError:
            open(car_index_file_name, 'w').close()
            car_index_lines = []

        # Шаг 7: Найти номер строки с автомобилем по VIN
        car_line_num = None
        for car_index_line in car_index_lines:
            vin_and_line_num = str.split(car_index_line, ',')
            vin = vin_and_line_num[0]
            line_num = int(vin_and_line_num[1])
            if vin == sold_car_vin:
                car_line_num = line_num
                break
        if car_line_num is None:
            print('В базе машин не найден запрошенный VIN')
            return None
        
        # Шаг 8: Прочитать запись автомобиля по номеру строки
        #  (все строки имеют длину 100+2 символa)
        car_file_name = self.root_directory_path + '/cars.txt'
        with open(car_file_name, "r") as f:
            f.seek((car_line_num - 1) * 102)
            car_record = f.read(100)
        car_record = car_record.strip().split(',')

        # Шаг 9: Обновить статус автомобиля на доступен
        car_record[4] = CarStatus.available

        # Шаг 10: Записать обновленную запись автомобиля по номеру строки (все строки имеют длину 100+2 символa)
        with open(car_file_name, "r+") as f:
            f.seek((car_line_num - 1) * 102)
            record = (car_record[0] + ','
                      + car_record[1] + ','
                      + car_record[2] + ','
                      + car_record[3] + ','
                      + car_record[4]).ljust(100) + '\n'
            f.write(record)

        return Car(
            vin=car_record[0],
            model=int(car_record[1]),
            price=Decimal(car_record[2]),
            date_start=datetime.fromisoformat(car_record[3]),
            status=CarStatus(car_record[4])
        )

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        # Шаг 1: Прочитать все продажи
        sales_file_name = self.root_directory_path + '/sales.txt'
        try:
            with open(sales_file_name, "r") as f:
                sales_lines = f.readlines()
        except FileNotFoundError:
            open(sales_file_name, 'w').close()
            sales_lines = []

        # Шаг 2: Взять все VIN проданных автомобилей
        sold_car_vin_to_cost = dict()
        for sale_line in sales_lines:
            sale_record = sale_line.strip().split(',')
            sold_car_vin = sale_record[1]
            sold_car_cost = Decimal(sale_record[3])
            sold_car_vin_to_cost[sold_car_vin] = sold_car_cost

        # Шаг 3: Для каждого VIN проданного автомобиля, найти строчки
        #  с записями автомобилей
        sold_car_line_num_cost_list = list()
        car_index_file_name = self.root_directory_path + '/car_index.txt'
        with open(car_index_file_name, "r") as f:
            car_index_lines = f.readlines()
        for car_index_line in car_index_lines:
            vin_and_line_num = str.split(car_index_line, ',')
            vin = vin_and_line_num[0]
            line_num = int(vin_and_line_num[1])
            if vin in sold_car_vin_to_cost:
                sold_car_line_num_cost_list.append([line_num, sold_car_vin_to_cost[vin]])

        # Шаг 4: Для каждой строчки с записью автомобиля, найти ID модели
        sold_cars_model_id_cost_list = list()
        car_file_name = self.root_directory_path + '/cars.txt'
        with open(car_file_name, "r") as f:
            for line_num, cost in sold_car_line_num_cost_list:
                f.seek((line_num - 1) * 102)
                car_record = f.read(100)
                car_record = car_record.strip().split(',')
                sold_cars_model_id_cost_list.append([int(car_record[1]), cost])

        # Шаг 5: Посчитать количество продаж для каждой модели
        model_sales_count_dict = dict()
        model_sales_total_dict = dict()
        for model_id, cost in sold_cars_model_id_cost_list:
            if model_id in model_sales_count_dict:
                model_sales_count_dict[model_id] += 1
                model_sales_total_dict[model_id] += cost
            else:
                model_sales_count_dict[model_id] = 1
                model_sales_total_dict[model_id] = cost

        # Шаг 6: Собрать информацию о количестве продаж и общей сумме продаж для каждой модели
        model_sales_count_total_line_num_list = list()
        model_index_file_name = self.root_directory_path + '/model_index.txt'
        with open(model_index_file_name, "r") as f:
            model_index_lines = f.readlines()
        for model_index_line in model_index_lines:
            model_id_and_line_num = str.split(model_index_line, ',')
            model_id = int(model_id_and_line_num[0])
            line_num = int(model_id_and_line_num[1])
            if model_id in model_sales_count_dict:
                model_sales_count_total_line_num_list.append([
                    model_sales_count_dict[model_id],
                    model_sales_total_dict[model_id],
                    line_num
                ])
        # Шаг 7: Сортировка по количеству продаж, затем по общей сумме продаж
        model_sales_count_total_line_num_list.sort(key=lambda x: (x[0], x[1]), reverse=True)

        # Шаг 8: Взять топ-3 модели
        top_models = list()
        for i in range(min(3, len(model_sales_count_total_line_num_list))):
            model_sales_count = model_sales_count_total_line_num_list[i][0]
            line_num = model_sales_count_total_line_num_list[i][2]
            model_file_name = self.root_directory_path + '/models.txt'
            with open(model_file_name, "r") as f:
                f.seek((line_num - 1) * 102)
                model_record = f.read(100)
                model_record = model_record.strip().split(',')
                top_models.append(ModelSaleStats(
                    car_model_name=model_record[1],
                    brand=model_record[2],
                    sales_number=model_sales_count
                ))

        return top_models
