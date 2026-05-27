// 앱 진입점 — React 마운트 + Router
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { App } from './App';

// 워크숍 단순화를 위해 페이지 진입 시 가짜 사용자 자동 셋팅
if (!localStorage.getItem('userId')) {
  localStorage.setItem('userId', 'alice');
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
);
