class DomainError(Exception):
    """Base class for domain errors."""


class EntityNotFoundError(DomainError):
    """Requested domain entity does not exist."""


class BusinessRuleViolation(DomainError):
    """Domain business rule was violated."""
