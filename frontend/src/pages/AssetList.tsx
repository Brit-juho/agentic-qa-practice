// 장비 목록 화면 — 대여 가능한 자산을 보여주고 대여 시작
import { useEffect, useState } from 'react';
import { Asset, createRental, fetchAssets } from '../api/client';

export function AssetList() {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function reload() {
    setLoading(true);
    try {
      setAssets(await fetchAssets());
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    reload();
  }, []);

  async function rent(assetId: number) {
    setError(null);
    try {
      await createRental(assetId);
      await reload();
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <section>
      <h2>장비 목록</h2>
      {loading && <p>로딩 중...</p>}
      {error && <p style={{ color: 'crimson' }}>오류: {error}</p>}
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {assets.map((asset) => (
          <li
            key={asset.id}
            style={{
              padding: 12,
              border: '1px solid #ddd',
              marginBottom: 8,
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <div>
              <strong>{asset.name}</strong> <small>({asset.asset_type})</small>
              <br />
              상태: {asset.status}
            </div>
            <button
              onClick={() => rent(asset.id)}
              disabled={asset.status !== 'available'}
            >
              대여
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
