---
title: "React hooksを基礎から理解する (useState編)"
source: "https://qiita.com/seira/items/f063e262b1d57d7e78b4"
author:
  - "[[seira]]"
published: 2020-01-26
created: 2025-07-21
description: "React hooksとは React 16.8 で追加された新機能です。 クラスを書かなくても、 stateなどのReactの機能を、関数コンポーネントでシンプルに扱えるようになりました。 React hooksを基礎から理解する (useState編) 今ここ R..."
tags:
  - "clippings"
  - "React"
  - "Hooks"
  - "useState"
  - "Frontend"
  - "StateManagement"
---
![](https://relay-dsp.ad-m.asia/dmp/sync/bizmatrix?pid=c3ed207b574cf11376&d=x18o8hduaj&uid=)

この記事は最終更新日から3年以上が経過しています。

## React hooksとは

React 16.8 で追加された新機能です。  
クラスを書かなくても、 `state` などのReactの機能を、関数コンポーネントでシンプルに扱えるようになりました。

- React hooksを基礎から理解する (useState編)　 今ここ
- [React hooksを基礎から理解する (useEffect編)](https://qiita.com/seira/items/e62890f11e91f6b9653f)
- [React hooksを基礎から理解する (useContext編)](https://qiita.com/seira/items/fccdf4e73c59c491558d)
- [React hooksを基礎から理解する (useReducer編)](https://qiita.com/seira/items/2fbad56e84bda885c84c)
- [React hooksを基礎から理解する (useCallback編)](https://qiita.com/seira/items/8a170cc950241a8fdb23)
- [React hooksを基礎から理解する (useMemo編)](https://qiita.com/seira/items/42576765aecc9fa6b2f8)
- [React hooksを基礎から理解する (useRef編)](https://qiita.com/seira/items/0e6a2d835f1afb50544d)

## useStateとは

`useState()` は、関数コンポーネントでstateを管理（ `state` の保持と更新）するためのReactフックであり、最も利用されるフックです。

`state` とはコンポーネントが内部で保持する「状態」のことで、画面上に表示されるデータ等、アプリケーションが保持している状態を指しています。stateは `props` と違い後から変更することができます。

## クラスコンポーネントと関数コンポーネントを比較してみる

クラスコンポーネントと関数コンポーネントにおける「状態」の扱い方の違いを確認してみます。

### クラスコンポーネント

```react
import React from 'react'
import './styles.css'

// countの初期値として、1~10までのランダムな数値を生成 
const initialState = Math.floor(Math.random() * 10) + 1

class Counter extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
    // クラスでは、コンストラクタ内で、this.stateの初期値{ count: initialState }をセット
      count: initialState,
      // this.stateの初期値{ open: false }をセット
      open: true
    }
  }
  // toggleメソッドを作成 
  toggle = () => {
    this.setState({ open: !this.state.open })
  }

  render() {
    return (
      <>
        <button onClick={this.toggle}>
          {this.state.open ? 'close' : 'open'}
        </button>
        <div className={this.state.open ? 'isOpen' : 'isClose'}>
          <p>現在の数字は {this.state.count} です</p>
          {/*ボタンをクリックした時に、this.setState()を呼ぶことでcountステートを更新 */}
          <button
            onClick={() => this.setState({ count: this.state.count + 1 })}
          >
            + 1
          </button>
          <button
            onClick={() => this.setState({ count: this.state.count - 1 })}
          >
            - 1
          </button>
          <button onClick={() => this.setState({ count: 0 })}>0</button>
          <button onClick={() => this.setState({ count: initialState })}>
            最初の数値に戻す
          </button>
        </div>
      </>
    )
  }
}

export default Counter
```

ちなみにstyles.cssの中身はこれだけ。

```css
.isClose {
  display: none;
}

.isOpen {
  display: block;
}
```

こんなカウンターが出来ました。  
[![](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2F164a68b2-a408-bc8d-dab3-8696cfda08ec.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=9eb23ea70139b9ab2f2656daa1f22156)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2F164a68b2-a408-bc8d-dab3-8696cfda08ec.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=9eb23ea70139b9ab2f2656daa1f22156)

### 関数コンポーネント

hooks の `useState` を使ってクラスコンポーネントから関数コンポーネントに書き換えてみます。  
関数コンポーネントの基本形は以下の通り。

```react
const ExComponent = props => {
  // ここでhooksを使える
  return <div />
}
```

#### useStateの基本形

```react
//const [状態変数, 状態を変更するための関数] = useState(状態の初期値);
const [count, setCount] = useState(initialState)

// ちなみにクラスコンポーネントでは、、、
this.state = {
  count: initialState
}
```

`useState` の左辺の `state` 変数には任意の名前を付けることが出来ます。  
（分割代入構文をイメージすると理解しやすいです。）

- 1つ目の要素： `state` の現在の値
- 2つ目の要素： `state` の現在の値を更新するための関数
- `state` が更新されても `initialState` は `initialState` として保持される

```react
// 関数コンポーネント内で state を使えるようにするため、useState をインポート 
import React, { useState } from 'react'
import './styles.css'

const Counter = () => {
  // countの初期値として、1~10までのランダムな数値を生成
  const initialState = Math.floor(Math.random() * 10) + 1
  // count という名前の state 変数を宣言、初期値 initialState をセット
  const [count, setCount] = useState(initialState)
  // open という名前の state 変数を宣言、初期値 true をセット
  const [open, setOpen] = useState(true)
  // toggleの関数を宣言
  const toggle = () => setOpen(!open)

  return (
    <>
      <button onClick={toggle}>{open ? 'close' : 'open'}</button>
      <div className={open ? 'isOpen' : 'isClose'}>
        <p>現在の数字は{count}です</p>
        {/* setCount()は、countを更新するための関数。countを引数で受け取ることも出来る */}
        <button onClick={() => setCount(prevState => prevState + 1)}>
          + 1
        </button>
        <button onClick={() => setCount(count - 1)}>- 1</button>
        <button onClick={() => setCount(0)}>０</button>
        <button onClick={() => setCount(initialState)}>最初の数値に戻す</button>
      </div>
    </>
  )
}

export default Counter
```

クラスで書いた場合と、同じ結果になりました  
[![](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2F164a68b2-a408-bc8d-dab3-8696cfda08ec.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=9eb23ea70139b9ab2f2656daa1f22156)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2F164a68b2-a408-bc8d-dab3-8696cfda08ec.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=9eb23ea70139b9ab2f2656daa1f22156)

再レンダリング後も React はその変数の現在の `state` の値をそのまま持っており 、最新の `state` の値を関数に渡します。現在の `state` の値を更新したい場合は、 `setState` を呼びます。

## 最後に

次回は `useEffect` について書きたいと思います。

useState関連のQiita記事書きました  
[React公式チュートリアルのクラスコンポーネントを関数コンポーネントに書き替える](https://qiita.com/seira/items/689b76fa716ba4e20986)

### 参考にさせていただいたサイト

[0](https://qiita.com/seira/items/#comments)

コメント一覧へ移動

新規登録して、もっと便利にQiitaを使ってみよう

1. あなたにマッチした記事をお届けします
2. 便利な情報をあとで効率的に読み返せます
3. ダークテーマを利用できます
[ログインすると使える機能について](https://help.qiita.com/ja/articles/qiita-login-user)

[新規登録](https://qiita.com/signup?callback_action=login_or_signup&redirect_to=%2Fseira%2Fitems%2Ff063e262b1d57d7e78b4&realm=qiita) [ログイン](https://qiita.com/login?callback_action=login_or_signup&redirect_to=%2Fseira%2Fitems%2Ff063e262b1d57d7e78b4&realm=qiita)

[1042](https://qiita.com/seira/items/f063e262b1d57d7e78b4/likers)

947

### 関連ノート
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useCallback編+ React.memo)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useContext編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useEffect編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useMemo編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useReducer編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useRef編)]]