import rpyc


def login(self, username: str)
    pass

# Query operations

def get_user_info(self, id: UserId)
    pass

def list_topics(self)
    pass
# Publisher operations

def publish(self, id: UserId, topic: Topic, data: str)
    pass
# Subscriber operations

def subscribe_to(self, id: UserId, topic: Topic, callback: FnNotify)
    pass
def unsubscribe_to(self, id: UserId, topic: Topic)
    pass


def subscribe_all(self, id: UserId, callback: FnNotify)
    pass

def unsubscribe_all(self, id: UserId) -> FnNotify:
    pass