import getpass
from threading import Timer
from multiprocessing import Pool


def read_secret(
        prompt_message = "Enter password/code/secret:\n"
    ):

    secret = getpass.getpass(prompt_message)
    return secret

class FunctionRunner():
    """
    A container for running a function repeatedly.
    There are 2 functions offered for repeated execution:-
    1. repeat_periodic - multi-process periodic repeat i.e. non-blocking
    2. repeat_sequential - single threaded sequential repeat i.e. blocking

    eg.
    FunctionRunner(fn,("optional fn args tuple").repeat_periodic(5)
    FunctionRunner(fn,("optional fn args tuple").repeat_sequential(5)
    """

    def __init__(self, func, args = ()):

        self.func = func
        self.args = args

    def _repeat_func_sequential(self):
        self.func(*self.args)
        Timer(self.delay, self._repeat_func_sequential).start()

    def _repeat_func_periodic(self):
        self.pool.apply_async(self.func, self.args)
        Timer(self.delay, self._repeat_func_periodic).start()

    def repeat_periodic(self, delay, num_processes = 3):
        """
        Helper method to repeatedly call the given function periodically every
        'delay' seconds. The function calls are non-blocking independent
        of each other as they run async on separate processes

        :param num_processes
        :param delay
        """

        self.pool = Pool(num_processes)
        self.delay = delay
        self._repeat_func_periodic()

    def repeat_sequential(self, delay):
        """
        Helper method to repeatedly call the given function sequentially after
        'delay' seconds. The function calls are blocking and they wait for one
        to complete before starting another.

        :param delay
        """

        self.delay = delay
        self._repeat_func_sequential()
