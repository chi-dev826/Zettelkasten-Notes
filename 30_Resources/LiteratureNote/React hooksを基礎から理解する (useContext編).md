---
title: "React hooksを基礎から理解する (useContext編)"
source: "https://qiita.com/seira/items/fccdf4e73c59c491558d"
author:
  - "[[seira]]"
published: 2020-06-08
created: 2025-07-21
description: "React hooksとは React 16.8 で追加された新機能です。 クラスを書かなくても、stateなどのReactの機能を、関数コンポーネントでシンプルに扱えるようになりました。 React hooksを基礎から理解する (useState編) React h..."
tags:
  - "clippings"
  - "React"
  - "Hooks"
  - "useContext"
  - "Frontend"
  - "StateManagement"
---
![](https://relay-dsp.ad-m.asia/dmp/sync/bizmatrix?pid=c3ed207b574cf11376&d=x18o8hduaj&uid=)

この記事は最終更新日から3年以上が経過しています。

## React hooksとは

React 16.8 で追加された新機能です。  
クラスを書かなくても、 `state` などのReactの機能を、関数コンポーネントでシンプルに扱えるようになりました。

- [React hooksを基礎から理解する (useState編)](https://qiita.com/seira/items/f063e262b1d57d7e78b4)
- [React hooksを基礎から理解する (useEffect編)](https://qiita.com/seira/items/e62890f11e91f6b9653f)
- React hooksを基礎から理解する (useContext編) 今ここ
- [React hooksを基礎から理解する (useReducer編)](https://qiita.com/seira/items/2fbad56e84bda885c84c)
- [React hooksを基礎から理解する (useCallback編)](https://qiita.com/seira/items/8a170cc950241a8fdb23)
- [React hooksを基礎から理解する (useMemo編)](https://qiita.com/seira/items/42576765aecc9fa6b2f8)
- [React hooksを基礎から理解する (useRef編)](https://qiita.com/seira/items/0e6a2d835f1afb50544d)

## useContextとは

### Contextとは?

Reactコンポーネントのツリーに対して「グローバル」とみなすデータについて利用するように設計されています。  
コンポーネントの再利用をより難しくする為、慎重に利用しなくてはなりません。

`Context` によってコンポーネントツリー間におけるデータの橋渡しについて、すべての階層ごとに渡す必要性がなくなり、propsバケツリレーをしなくても下の階層で `Context` に収容されているデータにアクセスできるようになりました。

参考： [React公式サイト コンテクスト](https://ja.reactjs.org/docs/context.html)

### useContextとは?

`useContext` とは、 `Context` 機能をよりシンプルに使えるようになった機能。  
親からPropsで渡されていないのに、 `Context` に収容されているデータへよりシンプルにアクセスできるというものです。

[![](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2F15306049-e6ae-fd95-e051-13b6363ebf65.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=3e3475038eeb0b2efae104206bb1487e)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2F15306049-e6ae-fd95-e051-13b6363ebf65.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=3e3475038eeb0b2efae104206bb1487e)

### かんたんなサンプルを作ってみる

階層はこんな感じ  
[![](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/218656/6afdb387-e04c-5714-b32a-69d761f2e9a6.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2F6afdb387-e04c-5714-b32a-69d761f2e9a6.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=0fb522e5b0fe4e933ff748ef239534b4)

【ContextA.jsx】  
ContextBをimportしている

react.js

```javascript
import React from 'react'
import ContextB from './ContextB'

const ContextA = () => <ContextB/>
```

export default ContextA
```

【ContextB.jsx】  
ContextCをimportしている

react.js

```javascript
import React from 'react'
import ContextC from './ContextC'

const ContextB = () => <ContextC/>
```

export default ContextB
```

【ContextC.jsx】  
Appをimportしている

react.js

```javascript
//ReactからuseContextをimport
import React, {useContext} from 'react'
//AppコンポーネントからUserContext, HobbyContextをimport
import {UserContext, HobbyContext} from '../../App'

const ContextC = () => {
//useContextの引数に、UserContextやHobbyContextを渡すことによって、
//AppコンポーネントでProviderに渡したvalueの値を変数に代入することが出来る
  const user = useContext(UserContext)
  const hobby = useContext(HobbyContext)
  return (
    <p>{user.name}{user.age}歳: 趣味は{hobby}です。</p>
  )
}

export default ContextC
```

【App.js】  
ContextAをimportしている。

react.js

```javascript
// ReactからcreateContextとuseStateをimport
import React, {createContext, useState} from 'react'
import './App.css';
import Context from './components/ContextSample/ContextA'

//createContextを使ってUserContextとHobbyContextを作成
export const UserContext = createContext()
export const HobbyContext = createContext()

function App() {
//useStateを使ってuserを作成
  const [user, setUser] = useState({
    name: 'セイラ',
    age: '17'
  })
//useStateを使ってhobbyを作成
  const [hobby, setHobby] = useState('キャンプ')
  return (
    <div className='App'>
//userContext。Providerを作成、valueにはuserをセット
      <UserContext.Provider value={user}>
//HobbyContext.Providerを作成、valueにはhobbyをセット
        <HobbyContext.Provider value={hobby}>
          <Context/>
        </HobbyContext.Provider>
      </UserContext.Provider>
    </div>
  )
}

export default App
```

`React.createContext` からの戻り値を受け取り、そのコンテクストの現在値を返します。  
`React.createContext` の現在値は、ツリー内でこのフックを呼んだコンポーネントの直近にある `<Context.Provider>` の `value` の値によって決まります。

`useContext` を呼び出すコンポーネントはコンテクストの値が変化するたびに毎回再レンダーされます。

ちなみにContextC.jsxを `useContext` を使わずに書くと以下。  
`Consumer` を使って `Provider` を読み取っています。

javascript.js

```javascript
import React from 'react'
import {UserContext, HobbyContext} from '../../App'

const ContextC = () => {

  return (
    <>
      <UserContext.Consumer>
        {
          user => {
            return (
              <HobbyContext.Consumer>
                { hobby => <p>{user.name}({user.age}歳): 趣味：{hobby}</p> }
              </HobbyContext.Consumer>
            )
          }
        }
      </UserContext.Consumer>
    </>
  )

}

export default ContextC
```

useContextを使うと、随分シンプルに書けることがわかります

表示はこの通り  
[![ss.png](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2F416d83af-21da-df75-3e27-21f6efac5d02.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F218656%2F416d83af-21da-df75-3e27-21f6efac5d02.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=0668fd0ba32ac350d702aefd1922db27)

このようにuseContextを使うことにより、Contextをよりシンプルに分かりやすく書けました

## 最後に

次回は `useReducer` について書きたいと思います。

### 参考にさせていただいたサイト

[3](https://qiita.com/seira/items/#comments)

コメント一覧へ移動

新規登録して、もっと便利にQiitaを使ってみよう

1. あなたにマッチした記事をお届けします
2. 便利な情報をあとで効率的に読み返せます
3. ダークテーマを利用できます
[ログインすると使える機能について](https://help.qiita.com/ja/articles/qiita-login-user)

[新規登録](https://qiita.com/signup?callback_action=login_or_signup&redirect_to=%2Fseira%2Fitems%2Ffccdf4e73c59c491558d&realm=qiita) [ログイン](https://qiita.com/login?callback_action=login_or_signup&redirect_to=%2Fseira%2Fitems%2Ffccdf4e73c59c491558d&realm=qiita)

[321](https://qiita.com/seira/items/fccdf4e73c59c491558d/likers)

202

### 関連ノート
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useCallback編+ React.memo)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useEffect編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useMemo編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useReducer編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useRef編)]]
- [[Zettelkasten-Notes/LiteratureNote/React hooksを基礎から理解する (useState編)]]