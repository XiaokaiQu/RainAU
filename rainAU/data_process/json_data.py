import decimal, json, datetime

#Custom Serialization to deal with Decimal, Datetime, Date
class DecEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        
        super(DecEncoder, self).default(obj)