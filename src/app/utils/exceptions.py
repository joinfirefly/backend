class ActivityPubException(Exception):
    pass

class WebFingerNotSupported(ActivityPubException):
    pass

class HostNotFoundError(ActivityPubException):
    pass

class ActorNotFound(ActivityPubException):
    pass

class RemoteActorException(ActivityPubException):
    pass