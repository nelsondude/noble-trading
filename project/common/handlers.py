from tornado.web import RequestHandler
from tornado.escape import native_str

from .models import User, Trade, session
from .utils import (
    initializeUsers,
    isValidTrade,
    performTrade,
    getUserFromName,
    createUser,
    moneyNeededToPerformTrade,
    initiateTrade,
    acceptTrade,
    declineTrade
)

class BaseHandler(RequestHandler):
    def get_current_user_obj(self):
        user = native_str(self.get_secure_cookie("user"))
        if user:
            user_qs = session.query(User).filter_by(fullname=user).all()
            if len(user_qs) == 1:
                return user_qs[0]
        return None



class LoginHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie("user", "")
        count = session.query(User).count()
        if (count == 0):
            initializeUsers()
        self.render("login.html", title="Login Page")


    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        user_list = session.query(User).filter_by(fullname=username).all()
        if (len(user_list) == 1 and user_list[0].password == password):
            self.set_secure_cookie("user", username)
            self.redirect("/")
            # self.render('detail.html', user=user_list[0])
        else:
            self.redirect('login')


class RegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html")

    def post(self):
        name = self.get_argument('nickname')
        username = self.get_argument('username')
        password = self.get_argument('password')
        users = session.query(User).filter_by(fullname=username).all()
        if len(users) == 0:
            createUser(name, username, password)
            session.commit()
            self.redirect('/login')
        else:
            error = 'Could not successfully create user. Please try a different username.'
            self.render("register.html", error=error)


class HomeHandler(BaseHandler):
    def get(self):
        user = native_str(self.get_secure_cookie("user"))
        if user:
            user_qs = session.query(User).filter_by(fullname=user).all()
            if len(user_qs) == 1:
                user_obj = user_qs[0]
                sender_trades = session.query(Trade).filter_by(sender=user_obj).order_by(Trade.id.desc())
                receiver_trades = session.query(Trade).filter_by(receiver=user_obj).order_by(Trade.id.desc())
                self.render('home.html',
                            user=user_obj,
                            sender_trades=sender_trades,
                            receiver_trades=receiver_trades)
        else:
            self.redirect('/login')


class CompleteTradeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        tradeId = int(self.get_argument('tradeId'))
        action = self.get_argument('action')
        if action == 'accept':
            acceptTrade(tradeId)
        elif action == 'decline':
            declineTrade(tradeId)


class TradeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        sender = self.get_current_user_obj()
        if sender:
            receivers = session.query(User).filter(User.id != sender.id).all()
            self.render(
                'trade.html',
                user=sender,
                users=receivers,
                feedback=None
            )
        else:
            self.redirect('/login')



    def post(self, *args, **kwargs):
        amount = float(self.get_argument('amount'))
        sender = self.get_current_user_obj()
        sender_account = self.get_argument('sender_account')

        receiver = getUserFromName(self.get_argument('receiver'))
        receiver_account = self.get_argument('receiver_account')
        if not sender:
            self.redirect('/login')

        sender_valid = isValidTrade(sender, amount)
        receiver_valid = isValidTrade(receiver, amount)

        if (not sender_valid):
            required = moneyNeededToPerformTrade(sender, amount)

            feedback = {
                'title': 'You do not have enough money to successfully request this trade.',
                'message': 'The sum of your checking and trading accounts needs to be greater than 20% of the trade request',
                'prompt': 'You need $%s0 more to complete the transaction.'%required
            }
        elif (not receiver_valid):
            required = moneyNeededToPerformTrade(receiver, amount)
            feedback = {
                'title': 'The receiver of this trade does not have enough money to accept.',
                'message': 'The sum of their checking and trading accounts needs to be greater than 20% of the trade request',
                'prompt': 'They need $%s0 more to complete the transaction.'%required
            }

        elif (sender_valid and receiver_valid):
            initiateTrade(sender, sender_account, receiver, receiver_account, amount)
            feedback = {
                'title': 'You requested a trade!',
                'message': "You requested to send $%s0 to %s's %s account."%(amount, receiver.fullname, receiver_account),
                'prompt': 'Try and request another trade!'
            }

        receivers = session.query(User).filter(User.id != sender.id).all()
        self.render(
            'trade.html',
            user=sender,
            users=receivers,
            feedback=feedback
        )
