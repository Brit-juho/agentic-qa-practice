# frontend — 장비 대여 UI

React + TypeScript + Vite.

## 실행

```bash
cd frontend
npm install
npm run dev   # http://localhost:5173
```

백엔드가 `http://localhost:8000`에서 떠 있어야 합니다.

## 화면

- `/` — 장비 목록 (`AssetList`)
- `/mine` — 내 대여 (`MyRentals`)

> `feat/return-extend` 브랜치엔 `/return-extend` 화면이 추가됩니다.

## 인증

`localStorage`에 `userId` 키가 있어야 함. dev 환경에서 페이지 진입 시 자동으로 `alice`로 셋팅.
