class AppException(Exception):
    def __init__(self, detail: str, code: str, status_code: int):
        self.detail = detail
        self.code = code
        self.status_code = status_code
        super().__init__(detail)


class ResourceNotFound(AppException):
    def __init__(self, detail="Resource not found", code="RESOURCE_NOT_FOUND"):
        super().__init__(detail, code, 404)


class PermissionDenied(AppException):
    def __init__(self, detail="You do not have permission", code="FORBIDDEN"):
        super().__init__(detail, code, 403)


class BusinessRuleViolation(
    AppException
):
    def __init__(self, detail="Business rule violation", code="BUSINESS_RULE_VIOLATION"):
        super().__init__(detail, code, 409)
