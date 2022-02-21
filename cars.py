import csv
import os


class CarBase():
    def __init__(self,photo_file_name,brand,carrying,car_type=None):
        self.car_type=car_type
        self.photo_file_name=photo_file_name
        self.brand=brand
        self.carrying=float(carrying)

    def get_photo_file_ext(self):
        root, ext = os.path.splitext(self.photo_file_name)
        return ext
class Car(CarBase):
    def __init__(self,brand,photo_file_name ,carrying, passenger_seats_count,car_type='car'):
        super().__init__(photo_file_name, brand, carrying,car_type)
        self.passenger_seats_count = int(passenger_seats_count)


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra,car_type='spec_machine'):
        super().__init__(photo_file_name, brand, carrying,car_type)
        self.extra = extra

# car_type;brand;passenger_seats_count;photo_file_name;body_whl;carrying;extra
class Truck(CarBase):
    def __init__(self,brand,photo_file_name,carrying,body_lwh,car_type='truck'):
        super().__init__(photo_file_name,brand,carrying,car_type)
        try:
            data = body_lwh.split("x")
            if len(data)!=3:
                self.body_length = 0.0
                self.body_width = 0.0
                self.body_height = 0.0
            else:
                self.body_length=float(data[0])
                self.body_width=float(data[1])
                self.body_height=float(data[2])
        except Exception as e:
            self.body_length = 0.0
            self.body_width = 0.0
            self.body_height = 0.0

    def get_body_volume(self):
        return self.body_width*self.body_length*self.body_height
# csv_filename = "data_cars.csv"
# car_type;brand;passenger_seats_count;photo_file_name;body_whl;carrying;extra
types = ['car','truck','spec_machine']
# attrs_car = {car_type, photo_file_name, brand, carrying, passenger_seats_count}
# attrs_truc = {car_type,photo_file_name,brand,carrying,body_lwh }
# attrs_spec = { car_type, photo_file_name, brand, carrying, extr}

def validate(data):
    # существующий тип
    if data[0] not in types:
        return False
    try:
        root, ext = os.path.splitext(data[3])
        if ext not in ['.jpg','.jpeg','.png','.gif']:
            return False
        if not(isinstance(data[1], str) and data[1]!=""):
            return False
        data[5]=float(data[5])
        if data[0] == 'car':
            data[2]=int(data[2])
        elif data[0] == 'spec_machine':
            if not(isinstance(data[6], str) and data[6]!=""):
                return False
    except Exception:
        return False
    return True



    # все нужные атрибуты есть , а ненужных нет
# 0)car_type;1)brand;2)passenger_seats_count;3)photo_file_name;4)body_whl;5)carrying;6)extra

def get_car_list(csv_filename):
    car_list = []

    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            # print(row)
            if len(row)!=0 and validate(row) :
                if row[0] == 'car':
                    car_list.append(Car(brand=row[1],passenger_seats_count=int(row[2]),photo_file_name=row[3],carrying=float(row[5]),car_type=row[0]))
                if row[0] == 'truck':
                    car_list.append(Truck(brand= row[1], body_lwh=row[4],photo_file_name= row[3], carrying=float(row[5]),car_type=row[0]))
                if row[0] == 'spec_machine':
                    car_list.append(SpecMachine(brand=row[1],extra=row[6],photo_file_name=row[3],carrying=float(row[5]),car_type=row[0]))
            # print(row)
    return car_list
# csv_filename="data_cars.csv"
# print(get_car_list(csv_filename))
# #
# cars1 = get_car_list(csv_filename)
# print(len(cars1))
# for car1 in cars1:
#     print(type(car1))
#
# print(cars1[0].passenger_seats_count)
#
# print(cars1[1].get_body_volume())
# c = Truck('Man','f2.png','3x4x5x6','20')
# # print(c.car_type)
