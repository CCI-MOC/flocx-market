class MarketplaceException(Exception):
    msg_fmt = "An unknown exception occurred."
    code = 500

    def __init__(self, message=None, **kwargs):
        if message is None:
            try:
                message = self.msg_fmt.format(**kwargs)
            except KeyError:
                message = self.msg_fmt

        self.message = message
        super(MarketplaceException, self).__init__(message)


class ResourceNotFound(MarketplaceException):
    code = 404
    msg_fmt = "{resource_type} {resource_uuid} not found."


class ResourceNoPermission(MarketplaceException):
    code = 403
    msg_fmt = "You do not have permissions on {resource_type} {resource_uuid}."


class RequiresAdmin(MarketplaceException):
    code = 403
    msg_fmt = ("You must be an admin to perform this"
               "action on type {resource_type}.")


class InvalidInput(ValueError):
    code = 403

    def __init__(self, message=None):
        self.message = message
        super(ValueError, self).__init__(message)
