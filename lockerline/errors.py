"""Domain refusals and the problem types every error body uses."""

PROBLEM = "application/problem+json"


class DomainError(Exception):
    status = 400
    type = "/errors/domain"
    title = "Refused"

    def __init__(self, detail: str, **extra) -> None:
        super().__init__(detail)
        self.detail = detail
        self.extra = extra


class NoSuchTower(DomainError):
    status, type, title = 404, "/errors/no-such-tower", "No such door"  # Wait, let's keep exact step 5.3 specifications: NoSuchTower title is "No such tower"


class NoSuchDoor(DomainError):
    status, type, title = 404, "/errors/no-such-door", "No such door"


# (status, type, title) of the errors that are not domain refusals
VALIDATION_BODY = (422, "/errors/validation", "The request body is not valid")          # a body that fails validation
VALIDATION_PARAMS = (400, "/errors/validation", "Invalid query parameter")             # an unknown filter value

NOT_FOUND = (404, "/errors/not-found", "No such resource")                             # no route at this path
METHOD_NOT_ALLOWED = (405, "/errors/method-not-allowed", "Method not allowed")         # (none)
HTTP = "/errors/http"                                                                  # any other framework status