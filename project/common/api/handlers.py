import tornado, datetime, json
from sqlalchemy.ext.serializer import loads, dumps

from ..models import session, Trade, User

def print_json(dict):
    print(json.dumps(dict, sort_keys=True, indent=4, separators=(',', ': ')))


class TradesAPIHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        id = self.get_argument('id', default=None)
        status = self.get_argument('status', default=None)
        receiver = self.get_argument('receiver', default=None)
        sender = self.get_argument('sender', default=None)
        amount_greater = self.get_argument('amount_greater', default=None)
        amount_less = self.get_argument('amount_less', default=None)

        qs = session.query(Trade)
        result = []
        if id:
            self.write(qs.get(int(id)).to_json())

        else:
            if status:
                qs = qs.filter_by(status=status)
            if receiver:
                qs = qs.filter_by(receiver_id=int(receiver))
            if sender:
                qs = qs.filter_by(sender_id=int(sender))
            if amount_greater:
                qs = qs.filter(Trade.amount >= float(amount_greater))
            if amount_less:
                qs = qs.filter(Trade.amount <= float(amount_less))

            for obj in qs:
                dict = obj.to_dict()
                result.append(dict)


            self.write({'results': result})

class UsersAPIHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        id = self.get_argument('id', default=None)
        fullname = self.get_argument('fullname', default=None)


        qs = session.query(User)
        result = []
        if id:
            self.write(qs.get(int(id)).to_json())

        else:
            if fullname:
                qs = qs.filter_by()
            for obj in qs:
                result.append(obj.to_dict())

            self.write({'result': result})