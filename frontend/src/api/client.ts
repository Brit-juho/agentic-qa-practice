// 백엔드 API 호출 클라이언트
const BASE = 'http://localhost:8000';

function authHeaders(): Record<string, string> {
  const userId = localStorage.getItem('userId') ?? '';
  return userId ? { 'X-User-Id': userId } : {};
}

export interface Asset {
  id: number;
  name: string;
  asset_type: string;
  status: string;
}

export interface Rental {
  id: number;
  asset_id: number;
  user_id: string;
  started_at: string;
  due_at: string;
  returned_at: string | null;
}

export async function fetchAssets(): Promise<Asset[]> {
  const res = await fetch(`${BASE}/assets`);
  if (!res.ok) throw new Error('failed_to_fetch_assets');
  return res.json();
}

export async function fetchMyRentals(): Promise<Rental[]> {
  const res = await fetch(`${BASE}/rentals/mine`, { headers: authHeaders() });
  if (!res.ok) throw new Error('failed_to_fetch_rentals');
  return res.json();
}

export async function createRental(assetId: number): Promise<Rental> {
  const res = await fetch(`${BASE}/rentals`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify({ asset_id: assetId }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'unknown' }));
    throw new Error(err.detail);
  }
  return res.json();
}
