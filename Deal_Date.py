
# coding: utf-8

# In[237]:


import re
import datetime
from dateutil.relativedelta import relativedelta


# In[407]:


# mm-dd-yy(yy)
# dd-mm-yy(yy)
# yy(yy)-mm-dd
# yy(yy)-dd-mm

# mm could be in number or abbrev form eg. June, July

class deal_date:
    
    # if only two digit of year is shown, what should be added to year? ex. 19 means 2019
    yearprefix = "20"
    
    month_dict = {"Jan":1,"Feb":2,"Mar":3,"Apr":4, "May":5, "Jun":6, "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12,"Sept":9}
    
    spec_month_dict = {"Sept":"Sep"}
    
    #special case in regular expression
    specialcase = {"*": 1, "+": 1, "\\": 1, "^": 1, "$": 1, ".": 1, "|": 1, "?": 1, "(" : 1, ")": 1, "[": 1, "{": 1, "-": 1}
    
    @classmethod
    def find_date(cls, datename, inputform):
        # inputform (d,m,Y)(anythong)(d,m,Y)(anythong)(d,m,Y)
        # ex. %m-%b-%Y
        try:
            
            seplist = cls.get_sep(inputform)
            
            if not seplist:
                raise ValueError("wrong inputformat format")
            
            # first strip out all the sep
            if seplist[0] + seplist[1] == '':
                
                
                # this situation corresponds to no sep is given, carzy format
                
                tempform = inputform
                
                # for ddmmyyyy 6 digits date
                if len(re.findall('\d{8}', datename)) == 1:
                    pass
                
                elif len(re.findall('\d{6}', datename)) == 1:
                    
                    a = datename[:2]
                    b = datename[2:4]
                    c = datename[4:]
                    
                    indxm = [m.span() for m in re.finditer(r'Y', tempform, flags=re.IGNORECASE)]    

                    if len(indxm) == 1:
                        tstart, tend = indxm[0]
                        if tstart == 1:
                            
                            datename = '20' + a + b + c
                        
                        elif tstart == 3:
                            
                            datename = a + '20' + b + c
                                
                        elif tstart == 5:
                            
                            datename = a + b + '20' + c 
                    else:
                        
                        raise ValueError("No Y or too many Y is in the form")
                        
                    
                else:
                        
                    tempkey = ''

                    for key in cls.month_dict:
                        if len(re.findall(key, datename, flags=re.IGNORECASE)) == 1:
                            tempkey = key
                            break
                    
                    for key in cls.spec_month_dict:
                        if len(re.findall(key, datename, flags=re.IGNORECASE)) == 1:
                            tempkey = key
                            break
                    
                    #print(tempkey)
                    #there is special case that, ex, datetiem does not take in Sept
                    if tempkey in cls.spec_month_dict:
                        datename = re.sub(tempkey, cls.spec_month_dict[tempkey], datename)
                        tempkey = cls.spec_month_dict[tempkey]
                        #print(datename)
                        
                    if len(datename) == len(tempkey) + 4:
                        indxm = [m.span() for m in re.finditer(r'Y', tempform, flags=re.IGNORECASE)]    

                        if len(indxm) == 1:
                            tstart, tend = indxm[0]
                            if tstart == 1:
                                
                                datename = '20' + datename

                            elif tstart == 3:

                                indxm = [m.span() for m in re.finditer(r'b', tempform, flags=re.IGNORECASE)] 

                                if len(indxm) == 1:
                                    tstart, tend = indxm[0]
                                    if tstart == 1:
                                        datename = datename[:len(tempkey)] + '20' + datename[len(tempkey):]
                                    else:
                                        datename = datename[:2] + '20' + datename[2:]

                                else:
                                    raise ValueError("No b or too many b is in the form")

                            elif tstart == 5:

                                datename = datename[:-2] + '20' + datename[-2:]
                                print(datename)

                        else:
                            raise ValueError("illegal format")
                            
                return datetime.datetime.strptime(datename, inputform).strftime('%m/%d/%Y')
                
            # there exists sep
            else:
                joinstr = ''
                if seplist[0] == "":
                    joinstr = seplist[1] 
                elif seplist[1] == "":
                    joinstr = seplist[0] 
                else:
                    joinstr = "[" + seplist[0] + '|' + seplist[1] + "]"
                
                # now we have a clean, free of sepcial case date string
                tempform = "".join(re.split(joinstr, inputform))
                
                # split the datelist, note that for mmddyyyy, no way we can split this
                datelist = re.split(joinstr, datename)
                
                datelist = list(filter(None, datelist))
                
                # year, month, day, could be any of them
                a, b, c = datelist
            
                # we want to see if Year is inside the string, and where it is
                indxm = [m.span() for m in re.finditer(r'Y', tempform, flags=re.IGNORECASE)]    

                if len(indxm) == 1:
                    tstart, tend = indxm[0]
                    if tstart == 1:
                        if len(a) == 2:
                            datename = '20' + a + seplist[0] + b + seplist[1] + c
                    elif tstart == 3:
                        if len(b) == 2:
                            datename = a + seplist[0] + '20' + b + seplist[1] + c
                    elif tstart == 5:
                        if len(c) == 2:
                            datename = a + seplist[0] + b + seplist[1] + '20' + c 

                return datetime.datetime.strptime(datename, inputform).strftime('%m/%d/%Y')
        
        except ValueError as e:
            print(e)
            return False
    
    @classmethod    
    def find_all_dates(cls, datename, inputform):
        try:
            res = []

            # inputform should only include
            # d % b % y
            # d % y % b
            # b % d % y
            # b % y % d
            # y % b % d
            # y % d % b

            # d % m % y
            # d % y % m
            # m % d % y
            # m % y % d
            # y % m % d
            # y % m % b

            # % could be anything
            
            seplist = cls.get_sep(inputform)
            
            if not seplist:
                raise ValueError("wrong inputformat format")
            
            tempform = ''
            
            # first strip out all the sep
            if seplist[0] + seplist[1] == '':
                tempform = inputform
            
            else:
                joinstr = ''
                if seplist[0] == "":
                    joinstr = seplist[1]
                elif seplist[1] == "":
                    joinstr = seplist[0]
                else:
                    joinstr = "[" + seplist[0] + '|' + seplist[1] + "]"
                
                # now we have a clean, free of sepcial case date string
                tempform = "".join(re.split(joinstr, inputform))
                
            
            # we want to see if abrev of month is inside the string, and where it is
            indxm = [m.span() for m in re.finditer(r'b', tempform, flags=re.IGNORECASE)]
            
            # where the abre form lies, 0, 1, 2?
            if len(indxm) == 1:
                tstart, tend = indxm[0]
                if tstart == 1:
                    indicate = 0
                elif tstart == 3:
                    indicate = 1
                elif tstart == 5:
                    indicate = 2
                
                if indicate == 0:
                    for key in cls.month_dict:
                        reg_ex = re.compile(key + seplist[0] + r'\d+' + seplist[1] + r'\d+', re.IGNORECASE)
                        res = res + reg_ex.findall(datename)

                elif indicate == 1:                                                 
                    for key in cls.month_dict:
                        reg_ex = re.compile(r'\d+'+ seplist[0] + key + seplist[1] + r'\d+', re.IGNORECASE)
                        res = res + reg_ex.findall(datename)

                elif indicate == 2:
                    for key in cls.month_dict:
                        reg_ex = re.compile(r'\d+'+ seplist[0] + r'\d+' + seplist[1] + key, re.IGNORECASE)
                        res = res + reg_ex.findall(datename)
            
            
            elif len(indxm) > 1:
                raise ValueError("why you typed two b")
            
            # if there is no b in the inputformat, match number sep number sep number
            else:
                reg_ex = re.compile(r'\d+' + seplist[0] + r'\d+' + seplist[1] + r'\d+', re.IGNORECASE)
                res = res + reg_ex.findall(datename)
                
            return res
        
        except ValueError as e:
            print(e)
            return False
    
    @classmethod    
    def deal_uniq_dates(cls, datename, inputform):
        # this method returns a unique list of dates
        try:
            
            return list(set(cls.deal_all_dates(datename, inputform)))
        
        except ValueError as e:
            print(e)
            return False
    
    # get a list of the two special sep that separates the inputform
    @classmethod
    def get_sep(cls, inputform):
        try:
            seplist = re.findall(r'(?<=%[mdbY])[^mdbY]*(?=%[mdbY])', inputform)

            if len(seplist) != 2:
                raise ValueError("wrong inputformat format")

            # if special case exists, add '/' to them
            seplist[0] = cls.nospecial(seplist[0])
            seplist[1] = cls.nospecial(seplist[1])

            return seplist
        
        except ValueError as e:
            print(e)
            return False
            
        
    @classmethod    
    def deal_all_dates(cls, datename, inputform):
        res = []
        
        datelist = cls.find_all_dates(datename, inputform)
        
        for i in datelist:
            res = res + [cls.find_date(i, inputform)]
        
        return res
        
    @classmethod    
    def nospecial(cls, str1):
        res = ""
        for i in str1:
            if i in cls.specialcase:
                res = res + '\\' + i
            else:
                res = res + i
        
        return res
    
    # for CDS application, from a taken description, we expect only two dates can be found, 
    # if two dates are found, compare and first return the earlier date
    # if one date is found, return the most recent date that has the same month and day
    @classmethod
    def get_two_dates(cls, datename, inputform, nowdate = False):
        
        try:
            
            temp_list = cls.deal_uniq_dates(datename, inputform)

            # nowdate is the corresponding time when we do the data processing, format "mm/dd/YYYY"
            if not nowdate:
                nowdate = datetime.datetime.today()
                nowdate = cls.last_day_of_month(nowdate)
                
            elif type(nowdate) is not str:
                raise ValueError("nowdate should be string")
                
            elif len(re.findall('\d{2}/\d{2}/\d{4}', nowdate)) != 1:
                raise ValueError("nowdate should be in the right format mm/dd/YYYY")
            
            nowdate_d = datetime.datetime.strptime(nowdate, "%m/%d/%Y")

            # dates more than two, throw error
            if len(temp_list) > 2:
                raise ValueError("wrong inputformat format")

            elif len(temp_list) == 2:
                newdate1 = datetime.datetime.strptime(temp_list[0], "%m/%d/%Y")
                newdate2 = datetime.datetime.strptime(temp_list[1], "%m/%d/%Y")

                if newdate1 <= newdate2:
                    return temp_list
                else:
                    return [temp_list[1], temp_list[0]]

            else:
                # only one date is given
                newdate2 = datetime.datetime.strptime(temp_list[0], "%m/%d/%Y")
                
                if newdate2.month <= nowdate_d.month:
                    # take this year
                    newdate1 = newdate2.replace(year = nowdate_d.year)
                    newdate1 = newdate1.strftime('%m/%d/%Y')
                    return [newdate1, temp_list[0]]
            
                elif newdate2.month > nowdate_d.month:
                    # take last year
                    newdate1 = newdate2.replace(year = nowdate_d.year - 1)
                    newdate1 = newdate1.strftime('%m/%d/%Y')
                    return [newdate1, temp_list[0]]
         
        except ValueError as e:
            print(e)
            return False
    
    @classmethod
    def last_day_of_month(cls, date):
        if date.month == 12:
            return date.replace(day=31)
        
        finaldate = date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)
        finaldate = finaldate - relativedelta(months=1)
        
        return finaldate.strftime('%m/%d/%Y')
        
            

