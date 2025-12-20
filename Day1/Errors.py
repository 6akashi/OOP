class InvalidOperationError(Exception):
    pass


class AgeError(Exception):
    pass

class AccountFrozenError(Exception):
    pass


class AccountClosedError(Exception):
    pass


class InsufficientFundsError(Exception):
    pass

class AccountAllreadyExist(Exception):
    pass

class TimeError(Exception):
    pass
