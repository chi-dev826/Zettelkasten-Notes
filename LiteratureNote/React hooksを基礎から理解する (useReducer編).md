---
title: "React hooksを基礎から理解する (useReducer編)"
source: "https://qiita.com/seira/items/2fbad56e84bda885c84c"
author:
  - "[[seira]]"
published: 2020-06-16
created: 2025-07-21
description: "React hooksとは React 16.8 で追加された新機能です。 クラスを書かなくても、stateなどのReactの機能を、関数コンポーネントでシンプルに扱えるようになりました。 React hooksを基礎から理解する (useState編) React h..."
tags:
  - "clippings"
  - "React"
  - "Hooks"
  - "useReducer"
  - "Frontend"
  - "StateManagement"
  - "APIFetching"
---
![](https://relay-dsp.ad-m.asia/dmp/sync/bizmatrix?pid=c3ed207b574cf11376&d=x18o8hduaj&uid=)

この記事は最終更新日から3年以上が経過しています。

## React hooksとは

React 16.8 で追加された新機能です。  
クラスを書かなくても、 `state` などのReactの機能を、関数コンポーネントでシンプルに扱えるようになりました。

- [React hooksを基礎から理解する (useState編)](https://qiita.com/seira/items/f063e262b1d57d7e78b4)
- [React hooksを基礎から理解する (useEffect編)](https://qiita.com/seira/items/e62890f11e91f6b9653f)
- [React hooksを基礎から理解する (useContext編)](https://qiita.com/seira/items/fccdf4e73c59c491558d)
- React hooksを基礎から理解する (useReducer編) 今ここ
- [React hooksを基礎から理解する (useCallback編)](https://qiita.com/seira/items/8a170cc950241a8fdb23)
- [React hooksを基礎から理解する (useMemo編)](https://qiita.com/seira/items/42576765aecc9fa6b2f8)
- [React hooksを基礎から理解する (useRef編)](https://qiita.com/seira/items/0e6a2d835f1afb50544d)

## useReducerとは

状態管理のためのフックで、 `useState` と似たような機能。 `useState` は `useReducer` に内部実装されています。

`(state, action) => newState` という型の `reducer` を受け取り、現在の `state` と `dispatch` 関数の両方を返します。

react.jsx

```javascript
const [state, dispatch] = useReducer(reducer,'初期値')
```

- `reducer` は `state` を更新するための関数で、 `dispatch` は、 `reducer` を実行するための呼び出し関数です。  
	（変数を宣言するときに、stateの更新方法をあらかじめ設定しておくことが出来る。）

#### dispatch(action)で実行

- `action` は何をするのかを示すオブジェクト
- `{type: increment, payload: 0}` のように、 `type` プロパティ（ `action` の識別子）と値のプロパティで構成されている。

### useStateとuseReducerの比較

|  | useState | useReducer |
| --- | --- | --- |
| 扱えるstateのtype | 数値、文字列、オブジェクト、論理値 | オブジェクト、配列 |
| 関連するstateの取り扱い | ☓ | 複数を同時に取り扱うことが出来る |
| ローカルorグローバル | ローカル | グローバル useContext()と一緒に取り扱う |

Reduxで実現していたstate管理が、useContext & useReducerで実現できるようになり、Reduxが不要になってきました。

### useReducer()を使ってカウンターを作ってみる

#### スタイリングにはMaterial-UIを使用

`Material-UI` をinstallしたら、使いたいコンポーネントをすぐ見つけられるし、勝手にスタイリングしてくれるのでテンションあがります😁

参考： [MATERIAL-UI](https://material-ui.com/)

#### sample1:stateが単数

counter.jsx

```javascript
//useReducerをimport
import React, {useReducer} from 'react'
import Button from '@material-ui/core/Button';
import ButtonGroup from '@material-ui/core/ButtonGroup';

//counterの初期値を0に設定
const initialState = 0
//reducer関数を作成
//countStateとactionを渡して、新しいcountStateを返すように実装する
const reducerFunc = (countState, action)=> {
//reducer関数にincrement、increment、reset処理を書く
//どの処理を渡すかはactionを渡すことによって判断する
  switch (action){
    case 'increment':
      return countState + 1
    case 'decrement':
      return countState - 1
    case 'reset':
      return initialState
    default:
      return countState
  }
}
const Counter = () => {
//作成したreducerFunc関数とcountStateをuseReducerに渡す
//useReducerはcountStateとdispatchをペアで返すので、それぞれを分割代入
  const [count, dispatch] = useReducer(reducerFunc, initialState)
//カウント数とそれぞれのactionを実行する<Button/>を設置する
  return (
    <>
      <h2>カウント：{count}</h2>
      <ButtonGroup color="primary" aria-label="outlined primary button group">
        <Button onClick={()=>dispatch('increment')}>increment</Button>
        <Button onClick={()=>dispatch('decrement')}>decrement</Button>
        <Button onClick={()=>dispatch('reset')}>reset</Button>
      </ButtonGroup>
    </>
  )
}

export default Counter
```

[![](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2F08303c75-70fd-9533-d07c-de46bad7b79e.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=54fe84cc0b7a39145d65d070e10b8463)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2F08303c75-70fd-9533-d07c-de46bad7b79e.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=54fe84cc0b7a39145d65d070e10b8463)

#### sample2: stateが複数

counter2.jsx

```javascript
//useReducerをimport
import React, {useReducer} from 'react'
import Button from '@material-ui/core/Button';
import ButtonGroup from '@material-ui/core/ButtonGroup';

//counterの初期値を0に設定
//2つのcountStateを扱う。それぞれのinitialStateを設定
const initialState ={
  firstCounter: 0,
  secondCounter: 100
}
//reducer関数を作成
//countStateとactionを渡して、新しいcountStateを返すように実装する
const reducerFunc = (countState, action)=> {
//reducer関数にincrement、increment、reset処理を書く
//どの処理を渡すかはactionを渡すことによって判断する
//switch文のactionをaction.typeに変更
//firstCounter、secondCounter用にcaseを設定
//複数のcounterStateを持っている場合は、更新前のcounterStateを展開し、オブジェクトのマージを行う
  switch (action.type){
    case 'increment1':
      return {...countState, firstCounter: countState.firstCounter + action.value}
    case 'decrement1':
      return {...countState, firstCounter: countState.firstCounter - action.value}
    case 'increment2':
      return {...countState, secondCounter: countState.secondCounter + action.value}
    case 'decrement2':
      return {...countState, secondCounter: countState.secondCounter - action.value}
    case 'reset1':
      return {...countState, firstCounter: initialState.firstCounter}
    case 'reset2':
      return {...countState, secondCounter: initialState.secondCounter}
    default:
      return countState
  }
}
const Counter2 = () => {
//作成したreducerFunc関数とcountStateをuseReducerに渡す
//useReducerはcountStateとdispatchをペアで返すので、それぞれを分割代入
  const [count, dispatch] = useReducer(reducerFunc, initialState)
//カウント数とそれぞれのactionを実行する<Button/>を設置する
//dispatchで渡しているactionをオブジェクトに変更して、typeとvalueを設定
  return (
    <>
      <h2>カウント：{count.firstCounter}</h2>
      <ButtonGroup color="primary" aria-label="outlined primary button group">
        <Button onClick={()=>dispatch({type: 'increment1', value: 1})}>increment1</Button>
        <Button onClick={()=>dispatch({type: 'decrement1', value: 1})}>decrement1</Button>
        <Button onClick={()=>dispatch({type: 'reset1'})}>reset</Button>
      </ButtonGroup>
      <h2>カウント2：{count.secondCounter}</h2>
      <ButtonGroup color="secondary" aria-label="outlined primary button group">
        <Button onClick={()=>dispatch({type: 'increment2', value: 100})}>increment2</Button>
        <Button onClick={()=>dispatch({type: 'decrement2', value: 100})}>decrement2</Button>
        <Button onClick={()=>dispatch({type: 'reset2'})}>reset</Button>
      </ButtonGroup>
    </>
  )
}

export default Counter2

```

https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/218656/b89205ba-f8a5-14a6-4021-8ea58f3f6e5d.gif" width=400 />

## useReducer()を使って外部APIを取得してみる

`useEffect()`と`useReducer()`を使って外部APIを取得してみます。

axiosをyarn add

```
$ yarn add axios
```

参考：[axios](https://github.com/axios/axios)

外部API：[JSONPlaceholder](https://jsonplaceholder.typicode.com/)を利用

```App.js
//useReducerとuseReducerをReactからimport
import React, {useReducer,useEffect} from 'react'
import './App.css'
//axiosをimport
import axios from 'axios'

//initialStateを作成
const initialState = {
  isLoading: true,
  isError: '',
  post: {}
}

//reducerを作成、stateとactionを渡して、新しいstateを返すように実装
const dataFetchReducer = (dataState, action) =>{
  switch(action.type) {
    case 'FETCH_INIT':
    return {
      isLoading: true,
      post: {},
      isError: ''
    }
//データの取得に成功した場合
//成功なので、isErrorは''
//postにはactionで渡されるpayloadを代入
    case 'FETCH_SUCCESS':
    return {
      isLoading: false,
      isError: '',
      post: action.payload,
    }
//データの取得に失敗した場合
//失敗なので、isErrorにエラーメッセージを設定
    case 'FETCH_ERROR':
    return {
      isLoading: false,
      post: {},
      isError: '読み込みに失敗しました'
    }
//defaultではそのまま渡ってきたstateを返しておく
    default:
    return dataState
  }
}
const App = () => {
//initialStateとreducer関数をuseReducer()に読み、stateとdispatchの準備
  const [dataState, dispatch] = useReducer(dataFetchReducer, initialState)

  useEffect(()=>{
//http getリクエストをurlを書く
    axios
    .get('https://jsonplaceholder.typicode.com/posts/1')
//リクエストに成功した場合
    .then(res =>{
//dispatch関数を呼び、type:には'FETCH_SUCCESS'、payloadには受け取ったデータを代入する
      dispatch({type:'FETCH_SUCCESS', payload: res.data})
    })
//リクエストに失敗した場合catchの中に入ってくる
    .catch(err => {
      dispatch({type: 'FETCH_ERROR'})
    })
  })
  return (
    <div className='App'>
//Loadingが終わったら記事のタイトルを表示
      <h3>{dataState.isLoading ? 'Loading...': dataState.post.title}</h3>
//エラーがあった場合の処理
      <p>{dataState.isError ? dataState.isError : null}</p>
    </div>
  )
}

export default App
```

なんとかブラウザ上に表示出来た〜嬉し:smiley:
```

[4](https://qiita.com/seira/items/#comments)

コメント一覧へ移動

新規登録して、もっと便利にQiitaを使ってみよう

1. あなたにマッチした記事をお届けします
2. 便利な情報をあとで効率的に読み返せます
3. ダークテーマを利用できます
[ログインすると使える機能について](https://help.qiita.com/ja/articles/qiita-login-user)

[新規登録](https://qiita.com/signup?callback_action=login_or_signup&redirect_to=%2Fseira%2Fitems%2F2fbad56e84bda885c84c&realm=qiita) [ログイン](https://qiita.com/login?callback_action=login_or_signup&redirect_to=%2Fseira%2Fitems%2F2fbad56e84bda885c84c&realm=qiita)

[326](https://qiita.com/seira/items/2fbad56e84bda885c84c/likers)

193

### 関連ノート
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useCallback編+ React.memo)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useContext編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useEffect編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useMemo編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useRef編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useState編)]]
- [[Zettelkasten-Notes/LiteratureNote/データ取得のための React Hooks ライブラリ – SWR]]