from .models import session, User, Trading, Checking

def initializeUsers():
    createUser('Jill', 'Jill Schmill', 'jillpassword')
    createUser('Jack', 'Jack Schmack', 'jackpassword')
    session.commit()

def isValidTrade(checkBal, tradeBal, trade):
    trade_percent = .2
    return (checkBal + tradeBal) > (trade_percent * trade)

def moneyNeededToPerformTrade(checkBal, tradeBal, trade):
    account_sum = checkBal + tradeBal
    trade_percent = .2
    required = trade_percent * trade
    return required - account_sum

def performTrade(sender, sender_account, receiver, receiver_account, amount):
    # Remove Money From Account
    if sender_account == 'checking':
        sender.checking.balance -= amount
    else:
        sender.trading.balance -= amount

    # Add Money To Account
    if receiver_account == 'checking':
        receiver.checking.balance += amount
    else:
        receiver.trading.balance += amount
    session.commit()

def getUserFromName(name):
    qs = session.query(User).filter_by(fullname=name).all()
    if (len(qs) == 1):
        return qs[0]
    return None

def createUser(name, username, password):
    user_obj = User(name=name, fullname=username, password=password)
    user_obj.trading = Trading()
    user_obj.checking = Checking()
    session.add(user_obj)
    session.commit()