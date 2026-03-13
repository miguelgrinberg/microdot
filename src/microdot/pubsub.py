class PubSub:
    subscriptions = {}

    def subscribe(self, observer, topic):
        if topic not in self.subscriptions:
            self.subscriptions[topic] = []
        self.subscriptions[topic].append(observer)

    def unsubscribe(self, observer, topic):
        if topic in self.subscriptions:
            try:
                self.subscriptions[topic].remove(observer)
                if not self.subscriptions[topic]:
                    del self.subscriptions[topic]
            except (ValueError, IndexError):
                pass

    @classmethod
    async def publish(cls, topic, data):
        for observer in cls.subscriptions.get(topic, []):
            await observer.send(data, event=topic)
