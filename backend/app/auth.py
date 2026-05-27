# X-User-Id 헤더로 가짜 인증을 처리 (워크숍용 단순화)
from fastapi import Header, HTTPException, status


def current_user(x_user_id: str | None = Header(default=None)) -> str:
    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-User-Id 헤더가 필요합니다",
        )
    return x_user_id
