from collections import OrderedDict


class UserDto:
    def __init__(self, id, name, age, address, createTime):
        self.id = id
        self.name = name
        self.age = age
        self.address = address
        self.createTime = createTime

    def __repr__(self):
        return OrderedDict(userId=self.id,
                           name=self.name,
                           age=self.age,
                           address=self.address,
                           createtime=self.createTime)
