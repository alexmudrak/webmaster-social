from abc import ABC, abstractmethod


class AbstractNotificationSender(ABC):
    @abstractmethod
    async def send(self, message):
        # TODO: Add typing for message
        raise NotImplementedError
