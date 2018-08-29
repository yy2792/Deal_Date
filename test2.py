from Deal_Spread import deal_spread as ds
from Deal_Date import deal_date as dd

date1 = "-CDS-1-20/06/22- 0.58% 50.000.000.00 EUR 14--04/2018 20--06/2022"

date2 = "-CDS-1-20/06/22- 0.58 50.000.000.00 EUR 14--04/2018 20--06/2022"

print(date1)

print(ds.get_all(date1, "%d--%m/%Y"))

print(date2)

print(dd.replace_dates(date2,"%d--%m/%Y"))
print(ds.get_spread(date2, "%d--%m/%Y"))
print(ds.get_all(date2, "%d--%m/%Y"))



