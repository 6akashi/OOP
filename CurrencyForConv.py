class CurrencyForConv():
    def __init__(self):
        
        self.convUSD = 1
        self.convRUB = 1
        self.convKZT = 1

    def get_conv(self) -> dict:
        conv = {
            "RUB": self.convRUB,
            "USD": self.convUSD,
            "KZT": self.convKZT
        }
        return conv

    def __str__(self):
        info = self.get_conv()
        return(
            f"ConvRUB: {info.get('RUB', 1)}\n"
            f"ConvUSD: {info.get('USD', 1)}\n"
            f"ConvKZT {info.get('KZT', 1)}\n"
        )
        
class ConvRubTo(CurrencyForConv):
    def __init__(self):
        super().__init__()
        self.convUSD = 2
        self.convKZT = 0.5

class ConvUsdTo(CurrencyForConv):
    def __init__(self):
        super().__init__()
        self.convRUB = 0.5
        self.convKZT = 0.25