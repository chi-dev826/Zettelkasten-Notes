---
title: "データ取得のための React Hooks ライブラリ – SWR"
source: "https://swr.vercel.app/ja"
author:
published: 2023-10-16
created: 2025-07-18
description: "SWR is a React Hooks library for data fetching. SWR first returns the data from cache (stale), then sends the fetch request (revalidate), and finally comes with the up-to-date data again."
tags:
  - "clippings"
  - "React"
  - "SWR"
  - "DataFetching"
---
## SWR

データ取得のための React Hooks ライブラリ

#### Lightweight

#### Realtime

#### Suspense

#### Pagination

#### Backend Agnostic

#### SSR / SSG Ready

#### TypeScript Ready

#### Remote + Local

“SWR” という名前は、 [HTTP RFC 5861 (opens in a new tab)](https://tools.ietf.org/html/rfc5861) で提唱された HTTP キャッシュ無効化戦略である `stale-while-revalidate` に由来しています。 SWR は、まずキャッシュからデータを返し（stale）、次にフェッチリクエストを送り（revalidate）、最後に最新のデータを持ってくるという戦略です。

✅

[はじめに](https://swr.vercel.app/ja/docs/getting-started) · [例題](https://swr.vercel.app/ja/examples/basic) · [ブログ](https://swr.vercel.app/ja/blog) · [GitHub リポジリ (opens in a new tab)](https://github.com/vercel/swr)

## 概要

```jsx
import useSWR from 'swr'

 

function Profile() {

  const { data, error, isLoading } = useSWR('/api/user', fetcher)

 

  if (error) return <div>failed to load</div>

  if (isLoading) return <div>loading...</div>

  return <div>hello {data.name}!</div>

}
```

この例では、 `useSWR` フックは `key` 文字列と `fetcher` 関数を受け取ります。 `key` はデータの一意な識別子（通常は API の URL）で、 `fetcher` に渡されます。 `fetcher` はデータを返す任意の非同期関数で、ネイティブの fetch や Axios のようなツールを使うことができます。

このフックは、リクエストの状態にもとづいて `data` と `isLoading`, `error` の三つの値を返します。

## 特徴

たった 1 行のコードで、プロジェクト内のデータ取得のロジックを単純化し、さらにこれらの素晴らしい機能をすぐに利用できるようになります：

- **速い** 、 **軽量** そして **再利用可能** なデータの取得
- 組み込みの **キャッシュ** とリクエストの重複排除
- **リアルタイム** な体験
- トランスポートとプロトコルにとらわれない
- SSR / ISR / SSG support
- TypeScript 対応
- React Native

SWR は、スピード、正確性、安定性のすべての面をカバーし、より良い体験を構築するのに役立ちます：

- 高速なページナビゲーション
- 定期的にポーリングする
- データの依存関係
- フォーカス時の再検証
- ネットワーク回復時の再検証
- ローカルキャッシュの更新（Optimistic UI）
- スマートなエラーの再試行
- ページネーションとスクロールポジションの回復
- React Suspense

And lot [more](https://swr.vercel.app/ja/docs/getting-started).

## コミュニティ

SWR は、React フレームワークである [Next.js (opens in a new tab)](https://nextjs.org/) と同じチームによって作られています。 今後のプロジェクトのアップデートについては、Twitter で [@vercel (opens in a new tab)](https://twitter.com/vercel) をフォローしてください。

お気軽に [GitHub のディスカッション (opens in a new tab)](https://github.com/vercel/swr/discussions) に参加してください！

Last updated on

### 関連ノート
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useEffect編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useReducer編)]]