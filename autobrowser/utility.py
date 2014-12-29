import getpass
from threading import Timer
from multiprocessing import Pool


def read_secret(prompt_message = "Enter password/code/secret to be used in "
                             "application:\n"):

    secret = getpass.getpass(prompt_message)
    return secret

class FunctionRunner():

    """
    A container for running a function repeatedly.
    There are 2 features offered for repeated execution:-
    1. REPEAT_PERIODIC - multi-process periodic repeat i.e. non-blocking
    2. REPEAT_SEQ - single threaded sequential repeat i.e. blocking

    Look at the below methods, _repeat_func_sequential & _repeat_func_periodic
    for more details.

    eg.
    settings = dict()
    settings["repeat_feature"] = FunctionRunner.REPEAT_SEQ
    settings["repeat_delay"] = 6 #in sec
    FunctionRunner(fn,("optional fn args tuple"), settings).start()
    """

    NO_REPEAT = 0
    REPEAT_PERIODIC = 1
    REPEAT_SEQ = 2

    def __init__(self, func, args = (), settings = {}):

        self._default_settings()
        self._update_defaults(settings)
        self.func = func
        self.args = args

    def _default_settings(self):
        self.settings = {}
        self.settings["num_processes"] = 3
        self.settings["repeat_feature"] = FunctionRunner.NO_REPEAT
        self.settings["repeat_delay"] = 5

    def _update_defaults(self, settings):
        for k in settings:
            self.settings[k] = settings[k]

    def _repeat_func_sequential(self, delay):

        """
        Private helper method to repeatedly call given function argument
        sequentially after 'delay' seconds. The function calls are blocking
        and they wait for one to complete before starting another.

        :param delay:
        """

        self.func(*self.args)
        Timer(delay, self._repeat_func_sequential, (delay,)).start()

    def _repeat_func_periodic(self, delay):

        """
        Private helper method to call given function argument every
        'delay' seconds. The function calls are non-blocking independent
        of each other as they run async on separate processes

        :param delay:
        """

        self.pool.apply_async(self.func, self.args)
        Timer(delay, self._repeat_func_periodic, (delay,)).start()

    def start(self):
        if self.settings["repeat_feature"] == FunctionRunner.NO_REPEAT:
            self.func(*self.args)
        elif self.settings["repeat_feature"] == FunctionRunner.REPEAT_PERIODIC:
            self.pool = Pool(self.settings["num_processes"])
            self._repeat_func_periodic(self.settings["repeat_delay"])
        elif self.settings["repeat_feature"] == FunctionRunner.REPEAT_SEQ:
            self._repeat_func_sequential(self.settings["repeat_delay"])