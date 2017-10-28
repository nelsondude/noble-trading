from tornado.web import RequestHandler
from tornado.escape import native_str

from .models import User
from .models import session
from .utils import (
    initializeUsers,
    isValidTrade,
    performTrade,
    getUserFromName,
    createUser,
    moneyNeededToPerformTrade
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
        user_obj = None
        if user:
            user_qs = session.query(User).filter_by(fullname=user).all()
            if len(user_qs) == 1:
                user_obj = user_qs[0]
        self.render('home.html', user=user_obj)



class TradeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        user = self.get_current_user_obj()
        if user:
            users = session.query(User).filter(User.id != user.id).all()
            self.render(
                'trade.html',
                user=user,
                users=users,
                feedback=None
            )
        else:
            self.redirect('/login')

    def post(self, *args, **kwargs):
        amount = float(self.get_argument('amount'))
        sender_account = self.get_argument('sender_account')
        receiver_account = self.get_argument('receiver_account')
        receiver = getUserFromName(self.get_argument('receiver'))
        sender = self.get_current_user_obj()
        if not sender:
            self.redirect('/login')
        tradeBal = sender.trading.balance
        checkBal = sender.checking.balance
        if (isValidTrade(checkBal, tradeBal, amount)):
            performTrade(user, user_account, receiver, receiver_account, amount)
            feedback = {
                'title': 'You made a successful trade!',
                'message': "You traded $%s0 to %s's %s account."%(amount, receiver.fullname, receiver_account),
                'prompt': 'Try and make another trade!'
            }

        else:
            required = moneyNeededToPerformTrade(
                checkBal,
                tradeBal,
                amount
            )
            feedback = {
                'title': 'Your trade request was not successfully processed.',
                'message': 'The sum of your checking and trading accounts needs to be greater than 20% of the trade request',
                'prompt': 'You need $%s0 more to complete the transaction.'%required
            }
        users = session.query(User).filter(User.id != user.id).all()
        self.render(
            'trade.html',
            user=user,
            users=users,
            feedback=feedback
        )
