---
title: "React hooksを基礎から理解する (useCallback編+ React.memo)"
source: "https://qiita.com/seira/items/8a170cc950241a8fdb23"
author:
  - "[[seira]]"
published: 2020-06-29
created: 2025-07-21
description: "React hooksとは React 16.8 で追加された新機能です。 クラスを書かなくても、 stateなどのReactの機能を、関数コンポーネントでシンプルに扱えるようになりました。 React hooksを基礎から理解する (useState編) React ..."
tags:
  - "clippings"
  - "React"
  - "Hooks"
  - "useCallback"
  - "ReactMemo"
  - "Frontend"
  - "PerformanceOptimization"
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
- React hooksを基礎から理解する (useCallback編)　 今ここ
- [React hooksを基礎から理解する (useMemo編)](https://qiita.com/seira/items/42576765aecc9fa6b2f8)
- [React hooksを基礎から理解する (useRef編)](https://qiita.com/seira/items/0e6a2d835f1afb50544d)

↓React.memo, useCallBack, useMemoに関する記事なので、よろしければ参考にしてみてください↓  
[【React】もっと速くなる！？パフォーマンス最適化に挑戦！](https://qiita.com/seira/items/9e38204758030cd5442a)

## useCallbackとは

useCallbackはパフォーマンス向上のためのフックで、メモ化したコールバック関数を返します。

useEffectと同じように、依存配列(=\[deps\] コールバック関数が依存している要素が格納された配列)の要素のいずれかが変化した場合のみ、メモ化した値を再計算します。

### メモ化とは

メモ化とは同じ結果を返す処理について、初回のみ処理を実行記録しておき、値が必要となった2回目以降は、前回の処理結果を計算することなく呼び出し値を得られるようにすることです。

イベントハンドラーのようなcallback関数をメモ化し、不要に生成される関数インスタンスの作成を抑制、再描画を減らすことにより、都度計算しなくて良くなることからパフォーマンスを向上が期待できます。

### 基本形

```jsx
useCallback(callbackFunction, [deps]);
```

sampleFuncは、再レンダーされる度に新しく作られますが、a,bが変わらない限り、作り直す必要はありません。

```jsx
const sampleFunc = () => {doSomething(a, b)}
```

usecallbackを使えば、依存配列の要素a,bのいずれかが変化した場合のみ、メモ化したsampleFuncの値を再計算します。一方で全て前回と同じであれば、前回のsampleFuncを再利用します。

```jsx
const sampleFunc = useCallback(
  () => {doSomething(a, b)}, [a, b]
);
```

### 再レンダーによるコストについて検証してみる

Text,Count,Buttonコンポーネントを子に持つ親コンポーネントCounterコンポーネントを作成しました。

testVol1.jsx

```javascript
import React, {useState} from 'react'

//Titleコンポーネント(子)
const Title = () => {
  console.log('Title component')
  return (
    <h2>useCallBackTest vol.1</h2>
  )
}

//Buttonコンポーネント(子)
const Button = ({handleClick,value}) => {
  console.log('Button child component', value)
  return <button type="button" onClick={handleClick}>{value}</button>
}

//Countコンポーネント(子)
const Count = ({text, countState}) => {
  console.log('Count child component', text)
  return <p>{text}:{countState}</p>
}

//Counterコンポーネント（親）
const Counter = () => {

  const [firstCountState, setFirstCountState] = useState(0)
  const [secondCountState, setSecondCountState] = useState(10)

//+ 1 ボタンのstateセット用関数
  const incrementFirstCounter = () => setFirstCountState(firstCountState + 1)

//+ 10 ボタンのstateセット用関数
  const incrementSecondCounter = () => setSecondCountState(secondCountState + 10)

//子コンポーネントを呼び出す
  return (
    <>
      <Title/>
      <Count text="+ 1 ボタン" countState={firstCountState}/>
      <Count text="+ 10 ボタン" countState={secondCountState}/>
      <Button handleClick={incrementFirstCounter} value={'+1 ボタン'}/>
      <Button handleClick={incrementSecondCounter} value={'+10 ボタン'}/>
    </>
  )
}

export default Counter
```

[![](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2Fe1536c38-d2a2-847b-a419-4e7dc372a637.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=d20934cc011d6eb150d3e13bfe341d01)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2Fe1536c38-d2a2-847b-a419-4e7dc372a637.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=d20934cc011d6eb150d3e13bfe341d01)

console.logを実行しているだけですが、すべてのコンポーネントが再レンダーされています。この部分で高コストな処理を行っていれば、その分だけパフォーマンスに悪影響を与えることになりますし、サイトが大きくなると、負荷も大きくなっていきます。

### React.memoについて

React.memoでは、コンポーネントが返した React 要素を記録し、再レンダーされそうになった時に本当に再レンダーが必要かどうかをチェックして、必要な場合のみ再レンダーします。  
デフォルトでは、等価性の判断にshallow compareを使っており、オブジェクトの1階層のみを比較することになります。

React.memoは、メモ化したいコンポーネントをラップして使います。

```jsx
//Titleコンポーネント(子)
const Title = React.memo(() => {
  console.log('Title component')
  return (
    <h2>useCallBackTest vol.1</h2>
  )
})

//Buttonコンポーネント(子)
const Button = React.memo(({handleClick,value}) => {
  console.log('Button child component', value)
  return <button type="button" onClick={handleClick}>{value}</button>
})

//Countコンポーネント(子)
const Count = React.memo(({text, countState}) => {
  console.log('Count child component', text)
  return <p>{text}:{countState}</p>
})
```

[![](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2Fdb1c3427-7111-8ac2-e910-38374f962536.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=262a83c428b182f1cdfef7834b5e9b25)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2Fdb1c3427-7111-8ac2-e910-38374f962536.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=262a83c428b182f1cdfef7834b5e9b25)

コンポーネントをReact.memoでラップしてメモ化すると、初回にTitleコンポーネント、Countコンポーネント２つ、Buttonコンポーネント２つがすべてレンダリングされました。

２回目以降、Titleコンポーネントについてはpropsがないので再レンダリングされていません。

Countコンポーネントについては、数字が更新されたコンポーネントについてのみ再レンダーされているので、最適化されています。

Buttonコンポーネントについては、ボタンのどちらかをクリックしたときにクリックされていないボタンも合わせ、２つのボタンが再レンダーされているので、最適化出来ていないようです。

#### Buttonコンポーネントは何故再レンダーされたか

Counter.jsx

```javascript
//Counterコンポーネント（親）
const Counter = () => {

  const [firstCountState, setFirstCountState] = useState(0)
  const [secondCountState, setSecondCountState] = useState(10)

//+ 1 ボタンのstateセット用関数
  const incrementFirstCounter = () => setFirstCountState(firstCountState + 1)

//+ 10 ボタンのstateセット用関数
  const incrementSecondCounter = () => setSecondCountState(secondCountState + 10)

//子コンポーネントを呼び出す
  return (
    <>
      <Title/>
      <Count text="+ 1 ボタン" countState={firstCountState}/>
      <Count text="+ 10 ボタン" countState={secondCountState}/>
      <Button handleClick={incrementFirstCounter} value={'+1 ボタン'}/>
      <Button handleClick={incrementSecondCounter} value={'+10 ボタン'}/>
    </>
  )
}
```

`<Button handleClick={incrementFirstCounter} value={'+1 ボタン'}/>` 、 `<Button handleClick={incrementSecondCounter} value={'+10 ボタン'}/>` の２つのButtonコンポーネントについて、いずれかのボタンをクリックしたときに、stateが更新されるので再レンダーされますが、更新されていないほうのstateのボタンも再レンダーされています。一方のボタンがクリックされて親コンポーネントであるCounterコンポーネントが再レンダーされたタイミングで関数も再生成されており、再生成された関数をReact.memoが別の関数と認識したことによります。

#### React.memoについてもう少し詳しく

React.memoの第二引数には関数を渡すことができます。  
第一引数として前回のprops（prevProps）を、第二引数として今回のprops（nextProps）を受け取ることが出来、真偽値を返すように書くことが出来ます。（areEqual）

```jsx
const メモ化されたコンポーネント = React.memo(元のコンポーネント, (prevProps, nextProps) => {/* true or flase */})
```

このareEqual関数はpropsが等しいときにtrueを返し、propsが等しくないときにfalseを返します。  
trueを返したときは再レンダーをスキップ、falseを返したときは再レンダーを行います。  
(areEqualを省略した場合は、propsのshallow compareで等価性を判断することになります。)  
また等価性のチェックにも、当然コストがかかることを考慮しなければなりません。

\[React公式サイト（React.memo）\] ([https://ja.reactjs.org/docs/react-api.html#reactmemo](https://ja.reactjs.org/docs/react-api.html#reactmemo))

### useCallbackとReact.memoを組み合わせて最適化

親コンポーネントであるCounterコンポーネントが再レンダーされたタイミングで関数が再生成されないようにするため、useCallbackを使って最適化していきます。

```jsx
//ReactからuseCallbackをimport
import React, {useState, useCallback} from 'react'

//Titleコンポーネント(子)
//React.memoでラップ
const Title = React.memo(() => {
  console.log('Title component')
  return (
    <h2>useCallBackTest vol.1</h2>
  )
})

//Buttonコンポーネント(子)
//React.memoでラップ
const Button = React.memo(({handleClick,value}) => {
  console.log('Button child component', value)
  return <button type="button" onClick={handleClick}>{value}</button>
})

//Countコンポーネント(子)
//React.memoでラップ
const Count = React.memo(({text, countState}) => {
  console.log('Count child component', text)
  return <p>{text}:{countState}</p>
})

//Counterコンポーネント（親）
const Counter = () => {

  const [firstCountState, setFirstCountState] = useState(0)
  const [secondCountState, setSecondCountState] = useState(10)

//+ 1 ボタンのstateセット用関数
//useCallbackで関数をラップし、依存配列には関数内で利用しているfirstCountStateを入れます。
  const incrementFirstCounter = useCallback(() => setFirstCountState(firstCountState + 1),[firstCountState])

//+ 10 ボタンのstateセット用関数
//useCallbackで関数をラップし、依存配列には関数内で利用しているsecondCountStateを入れます。
  const incrementSecondCounter = useCallback(() => setSecondCountState(secondCountState + 10),[secondCountState])

//子コンポーネントを呼び出す
  return (
    <>
      <Title/>
      <Count text="+ 1 ボタン" countState={firstCountState}/>
      <Count text="+ 10 ボタン" countState={secondCountState}/>
      <Button handleClick={incrementFirstCounter} value={'+1 ボタン'}/>
      <Button handleClick={incrementSecondCounter} value={'+10 ボタン'}/>
    </>
  )
}

export default Counter
```

[![](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2F0272d2f9-bf54-1903-e377-b8cbe47e0b9d.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=41ee4dda183ceaaf9ee49a23d0c48e9d)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2F0272d2f9-bf54-1903-e377-b8cbe47e0b9d.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=41ee4dda183ceaaf9ee49a23d0c48e9d)

うまく最適化出来ました！  
useCallbackでメモ化されたコールバック関数は、React.memoでメモ化されたコンポーネントへ渡して利用することで初めて不要な再描画をスキップ出来るようになります。  
React.memoとuseCallback、さっそくリファクタリングに役立ちそうです

React.memo/useCallback/useMemo関連の記事を書き直しましたので、よろしければどうぞ！！

- [【React】もっと速くなる！？パフォーマンス最適化に挑戦！](https://qiita.com/seira/items/9e38204758030cd5442a)

[1](https://qiita.com/seira/items/#comments)

コメント一覧へ移動

新規登録して、もっと便利にQiitaを使ってみよう

1. あなたにマッチした記事をお届けします
2. 便利な情報をあとで効率的に読み返せます
3. ダークテーマを利用できます
[ログインすると使える機能について](https://help.qiita.com/ja/articles/qiita-login-user)

[新規登録](https://qiita.com/signup?callback_action=login_or_signup&redirect_to=%2Fseira%2Fitems%2F8a170cc950241a8fdb23&realm=qiita) [ログイン](https://qiita.com/login?callback_action=login_or_signup&redirect_to=%2Fseira%2Fitems%2F8a170cc950241a8fdb23&realm=qiita)

[396](https://qiita.com/seira/items/8a170cc950241a8fdb23/likers)

250

### 関連ノート
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useContext編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useEffect編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useMemo編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useReducer編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useRef編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useState編)]]
- [[Zettelkasten-Notes/DevIdeas/movie-appのUI改善]]