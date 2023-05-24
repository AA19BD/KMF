from pydantic import BaseModel, EmailStr


class BaseResponse(BaseModel):
    # may define additional fields or config shared across responses
    class Config:
        orm_mode = True


class AccessTokenResponse(BaseResponse):
    token_type: str
    access_token: str
    expires_at: int
    issued_at: int
    refresh_token: str
    refresh_token_expires_at: int
    refresh_token_issued_at: int


class UserResponse(BaseResponse):
    id: str
    email: EmailStr


class BankProcessResponse(BaseModel):
    contract_number: str
    account_number: str
    card: str
    branch_of_the_bank: str
    main_currency: str
    period: str
    client_name: str
    transaction: str


class ErrorResponse(BaseModel):
    message: str
    details: str = None


class ProcessBankStatementResponse(BaseModel):
    success: BankProcessResponse = None
    error: ErrorResponse = None
