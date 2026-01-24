from fastapi import HTTPException, status

class AuthError:

    def user_not_found(detail: str = "User not found"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )
    
    def invalid_credentials(detail: str = "Invalid username or password"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )
    
    def user_not_verified(detail: str = "User is not verified"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )
    

    def invalid_or_expired(detail: str = "Invalid or expired token"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        ) 
