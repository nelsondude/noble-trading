from .models import session, User, Trading, Checking, Trade

def initializeUsers():
    createUser('Jill', 'Jill Schmill', 'jillpassword')
    createUser('Jack', 'Jack Schmack', 'jackpassword')
    session.commit()

def isValidTrade(user, trade):
    trade_percent = .2
    return (user.trading.balance + user.checking.balance) > (trade_percent * trade)

def moneyNeededToPerformTrade(user, trade):
    account_sum = user.checking.balance + user.trading.balance
    trade_percent = .2
    required = trade_percent * trade
    return required - account_sum

def initiateTrade(sender, sender_account, receiver, receiver_account, amount):
    trade_obj = Trade(
        sender=sender,
        receiver=receiver,
        sender_account=sender_account,
        receiver_account=receiver_account,
        amount=amount
    )
    session.add(trade_obj)
    session.commit()

def acceptTrade(tradeId):
    trade_obj = session.query(Trade).get(tradeId)
    trade_obj.sender.trading.balance -= trade_obj.amount
    trade_obj.receiver.trading.balance += trade_obj.amount
    trade_obj.status = 'accepted'
    session.commit()

def declineTrade(tradeId):
    trade_obj = session.query(Trade).get(tradeId)
    trade_obj.status = 'declined'
    session.commit()

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