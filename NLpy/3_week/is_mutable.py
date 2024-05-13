# mutable_objects_practice.py

print("리스트 실습")
my_list = [1, 2, 3]
print("원본 리스트:", my_list)

my_list.append(4)
print("요소 추가 후:", my_list)

my_list[0] = 0
print("요소 변경 후:", my_list)

print("\n딕셔너리 실습")
my_dict = {'a': 1, 'b': 2}
print("원본 딕셔너리:", my_dict)

my_dict['c'] = 3
print("요소 추가 후:", my_dict)

my_dict['a'] = 0
print("값 변경 후:", my_dict)

print("\n함수와 mutable 객체")
def update_list(a_list):
    a_list.append(4)

def update_dict(a_dict):
    a_dict['d'] = 4

print("함수 호출 전 리스트:", my_list)
update_list(my_list)
print("함수 호출 후 리스트:", my_list)

print("함수 호출 전 딕셔너리:", my_dict)
update_dict(my_dict)
print("함수 호출 후 딕셔너리:", my_dict)


"""
Mutable 객체는 함수 내에서 변경될 때, 원본 객체에도 영향을 미친다.
이는 유용할 수도 있지만, 예기치 않은 결과를 초래할 수도 있다.
"""

# class_with_mutable_objects.py

class MyClass:
    def __init__(self):
        self.my_list = [1, 2, 3]
        self.my_dict = {'a': 1, 'b': 2}

    def update_list(self, element):
        self.my_list.append(element)

    def update_dict(self, key, value):
        self.my_dict[key] = value

    def display(self):
        print("리스트:", self.my_list)
        print("딕셔너리:", self.my_dict)

my_instance = MyClass()

print("초기 상태:")
my_instance.display()

my_instance.update_list(4)
my_instance.update_dict('c', 3)

print("\n업데이트 후:")
my_instance.display()

another_instance = MyClass()

print("\n다른 인스턴스:")
another_instance.display()

"""
MyClass의 각 인스턴스는 자신만의 mutable 객체를 가진다. 
이 객체들에 대한 변경사항은 다른 인스턴스의 mutable 객체에 영향을 미치지 않는다.
"""