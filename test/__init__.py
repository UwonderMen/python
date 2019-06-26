

"""
    面试题：
    s = {"name":"zhangsan"}

    这样访问：s.name会报错

    只能使用s["name"]访问


    怎么将一个字典的属性访问改为以点的形式访问，例如s.name

        解决方法：
            1、将字典封装在一个类中进行访问，但是不允许通过包装的类来修改这个对象，如下面解决方法
"""

class DictObj:
    def __init__(self,d:dict):
        # self._dict = d
        if isinstance(d,dict):
            self.__dict__["_dict"] = d
        else:
            self.__dict__["_dict"] = {}

    def __getattr__(self, item):
        return self._dict[item]
        # return getattr(self._dict,item)

    def __setattr__(self, key, value):
        raise NotImplemented("not Implement..")


d = DictObj({"name":"zhangsan","age":12})

print(d.name)
print(d.__dict__)