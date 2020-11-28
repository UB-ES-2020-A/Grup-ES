import threading


class Lock(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    def __init__(self):
        """ Virtually private constructor. """
        if self.__singleton_instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Lock.__singleton_instance = self
            self.lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls._singleton_instance = cls()
        return cls.__singleton_instance


lock = Lock.get_instance().lock
