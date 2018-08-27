from Deal_Date import deal_date as dd

print("-CDS-1-20/06/22- 58 50.000.000.00 EUR 14--04/2018 20--06/2022")
print(dd.get_two_dates("-CDS-1-20/06/22- 58 50.000.000.00 EUR 14--04/2018 20--06/2022","%d--%m/%Y"))


print("-CDS-1-20/06/22- 58 50.000.000.00 EUR 14--04/2018 20--06/2022","%d--%m/%Y")
print(dd.get_two_dates("-CDS-1-20/06/22- 58 50.000.000.00 EUR 14--04/2018 20--06/2022","%d--%m/%Y"))

print("-CDS-5-20/12/18-JC PENNEY SENIOR U 19 2.000.000.00 USD 14**042018 20**122018")
print(dd.get_two_dates("-CDS-1-20/06/22- 58 50.000.000.00 EUR 14**042018 20**122018","%d**%m%Y"))

print("-CDS-5-20/12/18-JC PENNEY SENIOR U 19 2.000.000.00 USD 14**0418 20**1218")
print(dd.get_two_dates("-CDS-1-20/06/22- 58 50.000.000.00 EUR 14**0418 20**1218","%d**%m%Y"))

print("11JUN**20")
print(dd.find_date("11JUN**20", "%d%b**%Y"))

print("11**Sept20")
print(dd.find_date('11**SEPT20', "%d**%b%Y"))

print("Sepxxxx1120")
print(dd.find_date('Sepxxxx1120', "%bxxxx%d%Y"))

print("11**Sept--20")
print(dd.find_date('11**SEPT--20', "%d**%b--%Y"))

print("Sep11--20")
print(dd.find_date('Sep11--20', "%b%d--%Y"))

