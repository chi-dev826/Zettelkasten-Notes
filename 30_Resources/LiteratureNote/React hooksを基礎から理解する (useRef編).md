---
title: "React hooksを基礎から理解する (useRef編)"
source: "https://qiita.com/seira/items/0e6a2d835f1afb50544d"
author:
  - "[[seira]]"
published: 2020-11-24
created: 2025-07-21
description: "React hooksとは React 16.8 で追加された新機能です。 クラスを書かなくても、 stateなどのReactの機能を、関数コンポーネントでシンプルに扱えるようになりました。 React hooksを基礎から理解する (useState編) React ..."
tags:
  - "clippings"
  - "React"
  - "Hooks"
  - "useRef"
  - "Frontend"
  - "DOM"
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
- [React hooksを基礎から理解する (useMemo編)](https://qiita.com/seira/items/42576765aecc9fa6b2f8)
- React hooksを基礎から理解する (useRef編) 今ここ

## useRefとは

関数コンポーネントでは、Classコンポーネント時のref属性の代わりに、 `useRef` を使って要素への参照を行います。  
また `useRef` では、 `useState` のようにコンポーネント内での値を保持することが出来ます。

### 構文

```jsx
const refObject = useRef(initialValue)

//例
const number = useRef(100);
console.log(number.current); // 100
```

`useRef` は、`.current` プロパティが渡された引数（初期値はinitialValue）を `refObject` へ返します。  
この引数の値が書き換え可能な`.current` プロパティーの値であり、 `.current` プロパティ内に保持することができます。

#### DOMを参照したい場合

```jsx
const inputElement = useRef(null)

//例: inputElement.currentで <input type="text" /> を参照
<input ref={inputElement} type="text" />
console.log(inputElement.current); // <input type="text" />
```

##### DOMの参照例

`useRef` でrefオブジェクトを作成したものをref属性（HTML要素）に指定してDOMを参照しています。

```jsx
const App = () => {
  const inputEl = useRef(null);
  const handleClick = () => {
    inputEl.current.focus();
    console.log("inputEl.current:", inputEl.current);
    //inputEl.current: <input type="text">
  };
  return (
    <>
      <input ref={inputEl} type="text" />
      <button onClick={handleClick}>入力エリアをフォーカスする</button>
    </>
  );
};
```

ボタンクリックで `<input type="text">` がfocusされました。  
  
参照： [React公式サイト](https://ja.reactjs.org/docs/hooks-reference.html#useref)

#### useRefとuseStateをくらべてみる

##### useRefを使ってDOMを参照

useRefを利用すると `text` のstate更新時にのみコンポーネントの再レンダリングが発生します。

```jsx
const App = () => {
  const inputEl = useRef(null);
  const [text, setText] = useState("");
  const handleClick = () => {
    setText(inputEl.current.value);
  };
  console.log("レンダリング！！");
  return (
    <>
      <input ref={inputEl} type="text" />
      <button onClick={handleClick}>set text</button>
      <p>テキスト : {text}</p>
    </>
  );
};
```

[![](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2F795fe524-0716-918c-2f74-b92635aa6542.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=78370bad27f9c8e602fd655982949469)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2F795fe524-0716-918c-2f74-b92635aa6542.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=78370bad27f9c8e602fd655982949469) ※ コンソールに表示される文字列： （誤り） 描画！！　=> （正） レンダリング！！

##### useStateを使ってDOMを参照

入力中の文字列をステート `inputElement` に格納、ボタンが押された時に `setText(inputElement)` で `text` stateへ代入することで `useRef` を使った時と同じ挙動にしています。この場合、 `text` と `inputElement` のstate更新時の両方でコンポーネントの再レンダリングが発生しています。

```jsx
const App = () => {
  const [inputElement, setInputElement] = useState("");
  const [text, setText] = useState("");
  const handleClick = () => {
    setText(inputElement);
  };
  console.log("レンダリング！！");
  return (
    <>
      <input
        value={inputElement}
        onChange={(e) => setInputElement(e.target.value)}
        type="text"
      />
      <button onClick={handleClick}>setText</button>
      <p>テキスト : {text}</p>
    </>
  );
};
```

[![](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2F175c1e6e-3041-909e-8880-550decb083cf.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=ea6cb401e4f5d11d16ca9497c057abee) ※ コンソールに表示される文字列： （誤り） 描画！！　=> （正） レンダリング！！

`useState` を利用している場合はstateの変更される度にコンポーネントの再レンダリングが発生しますが、 `useRef` は値が変更になっても、コンポーネントの再レンダリングは発生しませんでした

コンポーネントの再レンダリングはしたくないけど、内部に保持している値だけを更新したい場合は、保持したい値を `useState` ではなく、 `useRef` を利用するのが良さそうです。

[0](https://qiita.com/seira/items/#comments)

コメント一覧へ移動

新規登録して、もっと便利にQiitaを使ってみよう

1. あなたにマッチした記事をお届けします
2. 便利な情報をあとで効率的に読み返せます
3. ダークテーマを利用できます
[ログインすると使える機能について](https://help.qiita.com/ja/articles/qiita-login-user)

[新規登録](https://qiita.com/signup?callback_action=login_or_signup&redirect_to=%2Fseira%2Fitems%2F0e6a2d835f1afb50544d&realm=qiita) [ログイン](https://qiita.com/login?callback_action=login_or_signup&redirect_to=%2Fseira%2Fitems%2F0e6a2d835f1afb50544d&realm=qiita)

[386](https://qiita.com/seira/items/0e6a2d835f1afb50544d/likers)

212

### 関連ノート
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useCallback編+ React.memo)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useContext編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useEffect編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useMemo編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useReducer編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useState編)]]