---
title: "React hooksを基礎から理解する (useMemo編)"
source: "https://qiita.com/seira/items/42576765aecc9fa6b2f8"
author:
  - "[[seira]]"
published: 2020-07-20
created: 2025-07-21
description: "React hooksとは React 16.8 で追加された新機能です。 クラスを書かなくても、 stateなどのReactの機能を、関数コンポーネントでシンプルに扱えるようになりました。 React hooksを基礎から理解する (useState編) React ..."
tags:
  - "clippings"
  - "React"
  - "Hooks"
  - "useMemo"
  - "Frontend"
  - "PerformanceOptimization"
  - "Memoization"
---
![](https://relay-dsp.ad-m.asia/dmp/sync/bizmatrix?pid=c3ed207b574cf11376&d=x18o8hduaj&uid=)

この記事は最終更新日から3年以上が経過しています。

## React hooksとは

React 16.8 で追加された新機能です。  
クラスを書かなくても、 `state` などのReactの機能を、関数コンポーネントでシンプルに扱えるようになりました。

- [React hooksを基礎から理解する (useState編)](https://qiita.com/seira/items/f063e262b1d57d7e78b4)
- [React hooksを基礎から理解する (useEffect編)](https://qiita.com/seira/items/e62890f11e91f6b9653f)
- [React hooksを基礎から理解する (useContext編)](https://qiita.com/seira/items/fccdf4e73c59c491558d)
- [React hooksを基礎から理解する (useReducer編)](https://qiita.com/seira/items/2fbad56e84bda885c84c)
- [React hooksを基礎から理解する (useCallback編)](https://qiita.com/seira/items/8a170cc950241a8fdb23)
- React hooksを基礎から理解する (useMemo編) 今ここ
- [React hooksを基礎から理解する (useRef編)](https://qiita.com/seira/items/0e6a2d835f1afb50544d)

↓React.memo, useCallBack, useMemoに関する記事なので、よろしければ参考にしてみてください↓  
[【React】もっと速くなる！？パフォーマンス最適化に挑戦！](https://qiita.com/seira/items/9e38204758030cd5442a)

## useMemoとは

useMemoは関数の結果を保持するためのフックで、何回やっても結果が同じ場合の値などを保存(メモ化)し、そこから値を再取得します。  
不要な再計算をスキップすることから、パフォーマンスの向上が期待出来ます。  
useCallbackは関数自体をメモ化しますが、useMemoは関数の結果を保持します。

### メモ化とは

メモ化とは同じ結果を返す処理について、初回のみ処理を実行記録しておき、値が必要となった2回目以降は、前回の処理結果を計算することなく呼び出し値を得られるようにすることです。  
都度計算しなくて良くなることからパフォーマンス向上が期待できます。

### 基本形

#### 依存配列が空の場合

```jsx
const sampleMemoFunc = () => {
  const memoResult = useMemo(() => hogeMemoFunc(), [])

  return <div>{memoResult}</div>
}
```

依存配列=\[deps\] へ空配列を渡すと何にも依存しないので、1回のみ実行。  
つまり、依存関係が変わらない場合はキャッシュから値をとってくる。

#### 依存配列に値が入っている場合

props.nameの値が変わったときだけ関数を再実行させたい場合は以下のように書きます。

```jsx
const sampleMemoFunc = (props) => {
  const memoResult = useMemo(() => hogeMemoFunc(props.name), [props.name])

  return <div>{memoResult}</div>
}
```

依存配列=\[deps\] へ変数を並べると、変数のどれかの値が変わった時にfuncを再実行する。  
つまり、依存関係が変わった場合に再実行する。

### サンプル

```jsx
import React, {useMemo, useState} from 'react'

const UseMemo = () => {
  const [count01, setCount01] = useState(0)
  const [count02, setCount02] = useState(0)

  const result01 = () => setCount01(count01 + 1)
  const result02 = () => setCount02(count02 + 1)

  // const square = () => {
  //   let i = 0
  //   while (i < 2) i++
  //   return count02 * count02
  // }

  const square = useMemo(() => {
    let i = 0
    while (i < 200000000000) i++
    return count02 * count02
  }, [count02])

  return (
    <>
      <div>result01: {count01}</div>
      <div>result02: {count02}</div>
      {/* <div>square: {square()}</div> */}
      <div>square: {square}</div>
      <button onClick={result01}>increment</button>
      <button onClick={result02}>increment</button>
    </>
  )
}

export default UseMemo
```

#### square関数をuseMemoに代入しない場合

```jsx
const square = () => {
  let i = 0
  while (i < 200000000000) i++
  return count02 * count02
}

return <div>square: {square()}</div>
```

square関数をuseMemoに代入しない場合、square関数の処理に関係ないはずのresult01ボタンを押した場合でも明らかに処理が重い。  
count01はsquare関数の処理は通していないので関係無いはずだが、コンポーネントが再生成されたタイミングでsquare関数が実行されてしまうことが原因で、処理が重くなっている。

#### square関数をuseMemoに代入した場合

```jsx
const square = useMemo(() => {
  let i = 0
  while (i < 200000000000) i++
  return count02 * count02
}, [count02])

return <div>square: {square}</div>
```

square関数をuseMemoへ代入した場合、result01ボタンを押した時に処理の重さは感じられなくなった。

square関数をuseMemoに代入し値を保持することで、依存配列であるcount02が更新されない限り、square関数の処理が実行されなくなったため、result01ボタンを押した場合の処理が軽くなった。

React.memo/useCallback/useMemo関連の記事を書き直しましたので、よろしければどうぞ！！

- [【React】もっと速くなる！？パフォーマンス最適化に挑戦！](https://qiita.com/seira/items/9e38204758030cd5442a)

## 最後に

次回は useRef について書きたいと思います。

参考にさせていただいたサイト  
[https://reactjs.org/](https://reactjs.org/)

[2](https://qiita.com/seira/items/#comments)

コメント一覧へ移動

新規登録して、もっと便利にQiitaを使ってみよう

1. あなたにマッチした記事をお届けします
2. 便利な情報をあとで効率的に読み返せます
3. ダークテーマを利用できます
[ログインすると使える機能について](https://help.qiita.com/ja/articles/qiita-login-user)

[新規登録](https://qiita.com/signup?callback_action=login_or_signup&redirect_to=%2Fseira%2Fitems%2F42576765aecc9fa6b2f8&realm=qiita) [ログイン](https://qiita.com/login?callback_action=login_or_signup&redirect_to=%2Fseira%2Fitems%2F42576765aecc9fa6b2f8&realm=qiita)

[214](https://qiita.com/seira/items/42576765aecc9fa6b2f8/likers)

124

### 関連ノート
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useCallback編+ React.memo)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useContext編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useEffect編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useReducer編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useRef編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useState編)]]