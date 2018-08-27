from Deal_Date import deal_date as dd

print("-CDS-1-20/06/22- 58 50.000.000.00 EUR 14--04/2018 20--06/2022")
print(dd.get_two_dates("-CDS-1-20/06/22- 58 50.000.000.00 EUR 14--04/2018 20--06/2022","%d--%m/%Y"))

print("-CDS-5-20/12/18-JC PENNEY SENIOR U 19 2.000.000.00 USD 14/04/2018 20/12/2018")
print(dd.get_two_dates("-CDS-1-20/06/22- 58 50.000.000.00 EUR 14--04/2018 20--06/2022","%d--%m/%Y"))

print(dd.find_date('11-JUN20', "%d-%b%Y"))

print("-CDS-5-20/12/18-JC PENNEY SENIOR U 19 2.000.000.00 USD 14**042018 20**122018")
print(dd.find_date('14**042018', "%d**%m%Y"))
print(dd.get_two_dates("-CDS-1-20/06/22- 58 50.000.000.00 EUR 14**042018 20**122018","%d**%m%Y"))

print("-CDS-5-20/12/18-JC PENNEY SENIOR U 19 2.000.000.00 USD 14**0418 20**1218")
print(dd.get_two_dates("-CDS-1-20/06/22- 58 50.000.000.00 EUR 14**0418 20**1218","%d**%m%Y"))
