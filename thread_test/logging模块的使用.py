import logging

"""
    注意：logging模块是线程安全的，因此，在多线程中一般使用都是logging模块
        打印消息
        
    
    logger类的继承：looger实例存在继承关系，利用继承关系可以实现一些级别的继承或者输出信息的
    继承。logger类的顶级父类是root，怎么继承呢 ？？通过使用工厂函数logging.getLogger("a")
    ,在工厂函数中通过使用点(.)表示关系,比如a.b表示是：a是b的父类，b是a的子类
    同时也表示a是root的子类，b是root的子孙类
    
    注意：如果使用工厂函数创建一个looger实例时，如果在工厂函数中没指定参数
    表示实例化一个root的logger
"""


"""
    logger之间的继承
"""
FORMAT = "%(asctime)s:%(thread)d:%(message)s"
# logging.basicConfig(level=logging.INFO,format=FORMAT,datefmt="%y-%m-%d %H:%M:%S")
# loga = logging.getLogger("a")
# loga.setLevel(20)
# loga.info("asdasd")
# logb = logging.getLogger("a.b")
# logb.info("lllll")



"""
    logger日志的不同输出位置（可以输出到控制台或者文件）
    
    Handler类是一个输出的基类
        子类有：
            StreamHandler
                子类：
                    FileHandler：输出到文件类
                    _StderrHandler：输出到标准输出
            NullHandler类：什么都不做
            
    
    Handler这个类可以做什么：
        1、可以单独设置日志级别level
        2、可以单独设置日志输出格式
        3、可以设置过滤器
    
    
    
    关于logger实例的level继承关系：
        logger实例的level继承只与
        
    
    注意：
        关于logger实例的特殊性：
            如果待导入的模块中实例化一个logger，这个logger名字与本模块中logger
            实例名字相同，那么这两个logger是同一个对象
        
        如果在同一个模块中，使用logger工厂函数实例化两个相同名字的logger时，其实
        只是实例化一个logger实例
"""

logging.basicConfig(level=logging.INFO,format=FORMAT,datefmt="%y-%m-%d %H:%M:%S")

logs = logging.getLogger("s")

logs.setLevel(logging.INFO)

print("-----logs:",logs.getEffectiveLevel())

logs_handler = logging.FileHandler("./k.log")

logs_handler.setLevel(logging.INFO)

fmt = logging.Formatter(FORMAT)

logs_handler.setFormatter(fmt=fmt)

logs.addHandler(logs_handler)

print("-----logs:",logs.getEffectiveLevel())



logs1 = logging.getLogger("s.s1")

print("-----logs1:",logs.getEffectiveLevel())

logs1.info("logs1")








