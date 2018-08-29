import re
from Deal_Date import deal_date as dd

class deal_spread:

    @classmethod
    def get_spread(cls, spreadstr, inputform):
        
        try:
            spreadstr = dd.replace_dates(spreadstr, inputform) 

            reg_ex = re.compile('\d+\.*\d*%', re.IGNORECASE)

            res = reg_ex.findall(spreadstr)

            if len(res) == 1:
                return float(res[0][:-1]) * 0.01
            elif len(res) == 0:
                # there is no percent, try to identify a separate number
                reg_ex2 = re.compile(r'\s\d+\.*\d*\s', re.IGNORECASE)
            
                res = reg_ex2.findall(spreadstr)

                if len(res) == 1:
                    return float(res[0])
                elif len(res) == 0:
                    raise ValueError("I can't identify any independent number")
                else:
                    raise ValueError("I am confused, too many independent numbers are given")
            else:
                raise ValueError("I am confused, there are two numbers ending with %")
        
        except ValueError as e:
            print(e)
            return False


    @classmethod
    def get_all(cls, cds_string, inputform, nowdate = False):
        
        res = []

        spread = cls.get_spread(cds_string, inputform)

        if spread is not False:
            res.append(spread)
        else:
            res.append("NA")

        dates1 = dd.get_two_dates(cds_string, inputform, nowdate)

        if dates1 is not False:

            res = res + dates1
        else:
            res = res + ['NA','NA']

        return res
