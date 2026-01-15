from datetime import time, datetime

from Transaction import Transaction


class RiskAnalyzer:
    def __init__(self) -> None:
        self.big_summary = False
        self.risk_level = "LOW"
        self.is_new_account = True
        self.night_operation = False

    def check_summary(self, transaction: Transaction):
        if transaction.transaction_summ >= 1000000:
            self.big_summary = True
        return self.big_summary
    
    def check_is_new_account(self, transaction: Transaction):
        history = transaction.sender.accounts_history
        reciever_id = transaction.reciever_account_id
        if reciever_id in history:
            self.is_new_account = False
        return self.is_new_account
    
    def check_operation_time(self, transaction: Transaction):
        startime = time(23, 0, 0)
        endtime = time(5,0,0)
        time_now = datetime.now().time()
        if time_now > startime and time_now < endtime:
            self.night_operation = True
        return self.night_operation
    
    def analyze_risk_level(self, transaction: Transaction):
        risks_list = [self.check_is_new_account, self.check_operation_time, self.check_summary]
        risks_counter = 0
        for risks in risks_list:
            if risks == True:
                risks_counter += 1
        if risks_counter == 0:
            self.risk_level = "LOW"
        elif risks_counter == 1:
            self.risk_level = "NORMAL"
        elif risks_counter >= 2:
            self.risk_level = "HIGH"

        return self.risk_level
