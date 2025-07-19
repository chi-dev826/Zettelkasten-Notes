---
title: "Claude？Gemini？いや、それでもGithub Copilotを使い続けるという話"
source: "https://qiita.com/CinnamonSea2073/items/4bca9196723ac48e40b2"
author: "CinnamonSea2073"
published: 2025-07-02
created: 2025-07-18
description: "2025年6月。 世界はGithub Copilot、Claude Code、そして Gemini CLIの3つに分かれ、混沌を極めていた……。 でも「Claude Codeでバイブコーディング！」だの「Gemini CLIにSSHしてスマホからバイブコーディング！」だの..."
tags:
  - "clippings"
  - "AI"
  - "Coding"
  - "GitHubCopilot"
  - "Gemini"
  - "Claude"
---
![](https://relay-dsp.ad-m.asia/dmp/sync/bizmatrix?pid=c3ed207b574cf11376&d=x18o8hduaj&uid=)

## エンジニアとしての市場価値を測りませんか？PR

企業からあなたに合ったオリジナルのスカウトを受け取って、市場価値を測りましょう

[無料でForkwellに登録する](https://lp.recruiting.forkwell.com/scout?argument=249xHStF&dmai=a67f4ef09e582b)

2025年6月。

世界は `Github Copilot` 、 `Claude Code` 、そして `Gemini CLI` の3つに分かれ、混沌を極めていた……。

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1927831/0051e57f-b417-4619-b665-3941895913ab.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1927831%2F0051e57f-b417-4619-b665-3941895913ab.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=7aa7bbd59521fa7b89979b94f8f0781b)

でも「Claude Codeでバイブコーディング！」だの「Gemini CLIにSSHしてスマホからバイブコーディング！」だのばかり話題になっていて、Github Copilotが全然話題になってない気がします。

> 「それCopilotでも出来る...」「なんならもっと楽にできる...」「しかも安い...」

みたいなところ意外とあるんですよ。

この記事では、そんなCopilot Agentの“なんかちょうどいい”魅力を紹介しつつ、劣勢に立たされたGithub Copilot派を立て直すべく、ゆるくやっていきます。

**Github Copilotも良いとこあるよ！！！みんなGithub Copilot使え！！！！！（過激思想）**

---

## Github Copilotとは？

バイブコーディングが分からない方は以下の記事を流し読みすることをお勧めします。  
（とはいえこの記事はもう古いと言ってもいいくらいにはツールの進化が早すぎるので、ややズレは感じます。）

Copilot Agentは以下の記事で大体説明されています。

ややこしいですが、Github Copilotは正確にはGithubのAI機能全体を示すワードであり、Github Coding Agent自体はその中の機能の一つです。今回話題に取り上げるのはそれのVScode版であるGithub CopilotのAgentモードについてです。 **ややこしすぎるでしょ。**

## それ、実はGithubCopilotでも出来る

### 計画を立ててから実行するやつ

最強の切り札を最初から使ってしまうんですが、Github Copilotの最強ポイントは、 **モデルをシームレスに切り替えることができることです。**  
同じコンテキスト、同じチャット、同じ画面で、シームレスにモデルを切り替えながら作業ができる点は、他のチャットツールにはない特徴だと思います。

モデルには個性があります。例えば、

- Claudeは、かなり自律した操作で作業を続けていけることができる点が素晴らしいが、 **ある程度道筋を与えないと迷走してめちゃくちゃになることがある**
- GPTは簡潔に指示をそのまま実行できる点が優れているが、Agentモードのような **全体のコードを自律的に編集できない**
- Geminiは **初期プロトタイプ制作やドキュメント作成には秀でている** が、大規模なコードの扱いは苦手

みたいな感じで。

でもこれをそれぞれに合った用途で切り替えれば、コードに多様性を与えるというか、色々できます。

- GeminiにUI書かせたけどあんまいい感じじゃない...  
	**じゃあ切り替えてClaudeに書かせよう！**
- Claudeにエラーの修復させてるけどずっと同じエラーで躓いている...  
	**GPTに一回整理させてからGeminiに書かせて、Claudeにレビューしてもらおう！**

みたいな無茶ぶりを、難しい設定無しにそのままできます。

その中によく使う小技として、計画を立ててから実行するやつがあります。  
Claude Codeのプランモード的なやつです。

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1927831/9473072c-8935-4dc8-9639-7bbe318ff1c4.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1927831%2F9473072c-8935-4dc8-9639-7bbe318ff1c4.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=fc735a61805fd626541a0d39a7c661b3)

まず `Askモード` で `GPT-4.1` を使用し、計画を立てさせます。  
`Askモード` というのは、ファイルの編集とか作成を封じて、簡単にチャットで打ち合わせだけをするモードです。

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1927831/8360bf8d-d7e7-4124-8115-81d69d5d0384.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1927831%2F8360bf8d-d7e7-4124-8115-81d69d5d0384.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=2a70c7de191b40b249d04b91113e8069)

いい感じに計画を立ててくれます。計画立案にClaudeではなくGPTを利用することで、GPTの特徴である「指示に的確にシンプルに従う」点を生かせます。  
本当はこの点では「ドキュメント作成に秀でている」Geminiを使用したほうがいい結果を得られるんですが、Geminiはプレミアムリクエスト扱いでお金がかかるので、GPTで我慢してます。とはいえ約5円の違いですが...

**追記**: `Gemini2.5 Pro` は約5円ですが、 `Gemini2.0 Flash` であれば約1.435円でした。よっしゃ！みんなGemini使おうぜ！

ちなみに、以下に計画立案をGPT以外にやらせた場合を記載しておきます。プロンプトは全て同じ。

Claudeモデル

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1927831/75b9f105-e5b6-4872-815c-47d55d597ffb.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1927831%2F75b9f105-e5b6-4872-815c-47d55d597ffb.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=b0cce9c8eafbb474724fb70333338793)

最初の応答がめちゃくちゃ遅いし、出力結果が長いです。プロンプトを調整すればもちろんちゃんと計画を作ってくれると思いますが、プロンプトを考えるのはバイブコーディングの「雰囲気でゆるくやる」に反すると勝手に思っているので、今回は考えないものとします。

Geminiモデル

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1927831/35fabb40-a27f-4ffd-adb9-c4739746f9de.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1927831%2F35fabb40-a27f-4ffd-adb9-c4739746f9de.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=c71920461035fe66e92a0344f3a48ebc)

これも応答が遅い。でもさすがはGemini、内容は非常に的確で素晴らしいです。  
ただし、先ほども書いた通りコストがかかるので、金欠学生にとっては、まあGPTでいいかなと言う感じ。  
（Gemini CLI使えば無料？知らんな）

あとはモデルを自律的作業が得意な `Claude` に、モードを `Agent` にして実行するだけ。

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1927831/4d31bebc-927b-4776-bf47-cc45ca1ec98e.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1927831%2F4d31bebc-927b-4776-bf47-cc45ca1ec98e.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=7d659f3586ecceaf2759ab9c66b9e6b3)

ちなみにGroq CloudのAPIキーを設定すれば任意のオープンソースLLMで作業してくれることも可能なので、モデルの多様性に関してはもはや何でもありになっています。DeepseekとかLlamaとか使えます。

### Github操作

Githubの操作とかコミットメッセージの作成とかは、もう様々な自律AIエージェントの基本機能の一つになっていますね。  
でも、Githubの操作はGithub Copilotの十八番。めちゃくちゃ得意だし、GUIだからワンボタンです。

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1927831/1eb13742-1685-49e4-ba7f-81cd589dd071.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1927831%2F1eb13742-1685-49e4-ba7f-81cd589dd071.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=9f911d105c367c34e9d487d3a9077315)  
[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1927831/05e558ea-dd24-4f56-a135-92f1c473ea2d.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1927831%2F05e558ea-dd24-4f56-a135-92f1c473ea2d.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=946125aaa3db13942acd384bb8ba923e)

メッセージ入力欄の✨を押せば、ステージされているファイル内容からコミットメッセージをすぐに出してくれるし、

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1927831/7243b469-31b9-4dfb-95b6-5b68ab52a5c9.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1927831%2F7243b469-31b9-4dfb-95b6-5b68ab52a5c9.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=f9d96adff7900dd1a8704cb0a8715ac0)

現在のPull Request情報を取得させてレビューされた内容を自律的に修正したりなどできます。

## もっと無茶ぶりできる

### 実はマルチモーダルなので色々食わせられる

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1927831/f51d6982-34f9-404e-aef4-f1d142108f61.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1927831%2Ff51d6982-34f9-404e-aef4-f1d142108f61.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=6bc49874cd8e7a41b7d7addbf01409ac)

**スクショを食わせられます。**  
実はこれすごい便利で、普通に画像をコピペするだけでコンテキストに追加して、それについて色々作業できます。  
フロントエンドの作成とかだとこうやってスクショを上げて「これをこうして」って言えるのはめちゃくちゃ便利です。

ですが、 **フロントエンド向けに絞って言うならもっと便利な機能があります。**

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1927831/32ec0edc-16af-4a88-8a48-dc64dec49cc0.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1927831%2F32ec0edc-16af-4a88-8a48-dc64dec49cc0.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=614e996c6dffcf96e687f129822a712e)

**ブラウザーもコンテキストに食わせられます。**  
これによって、Copilotがブラウザの要素を特定したり、CSSを理解して的確に修正したりができます。

### VScodeは高性能テキストエディタなので議事録とか研究とかできる

GithubCopilotは様々なIDEで使用することができます。  
ですがVScodeから使うことを考えた時、 **VScodeはコード作成ツールではなくてただの高性能なテキストエディタなので** （過激思想）  
議事録まとめたりとか研究資料まとめたりとかも十分可能です。

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1927831/4dc88ec3-2949-494d-9ae0-3b598ce6937c.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1927831%2F4dc88ec3-2949-494d-9ae0-3b598ce6937c.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=1d18f29deffe33cb68d39e0824809c69)

Notionの議事録をエクスポートしたフォルダを展開して

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1927831/77a0eeb7-6a5b-4593-be43-9a52c4dd099a.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1927831%2F77a0eeb7-6a5b-4593-be43-9a52c4dd099a.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=f8d2eb822a3d416f694b4e0601e139b2)

ドキュメント関係が得意なGeminiモデルに投げると

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1927831/ce608fd7-d0bf-4b7b-8355-3d6445c9b045.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1927831%2Fce608fd7-d0bf-4b7b-8355-3d6445c9b045.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=3d111388dae4edc23a4dba4784dce283)

このようにまとめてくれます。  
Gemini CLIでもいいと言われそうですが、Claudeのような自律操作が得意なモデルに投げるともっと深く調査してめちゃくちゃ詳しくまとめてきます。

Claudeモデル

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1927831/5d26e46c-4590-4029-b8ed-26849e9fe24e.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1927831%2F5d26e46c-4590-4029-b8ed-26849e9fe24e.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=0a06051e13df3870343fb94b4db8ab22)

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1927831/ef3e1e4f-a55d-444f-8902-e57723e747e8.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1927831%2Fef3e1e4f-a55d-444f-8902-e57723e747e8.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=e804480491aa44835a53effbc156489b)

Talivyと連携すればネット検索もできるので調べ物もできます。  
（ただし本当に日常利用レベルなので論文検索とかは無理、だったら普通にGeminiのDeepsearchの方が優秀）

### 拡張機能が使える

デバッガー、ターミナルはもちろん、リンターやワークスペースなどのVScode関連機能に対してCopilotはアクセスできます。  
**リンターをきつめに設定しておけば、プロンプトで指示をしなくても、めちゃくちゃ型を守ったコーディングをしてくれるわけですね。**  
正直これはCursorもVScodeベースなので同じですが、やはり対応はGithubCopilotの方が進んでいます。

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1927831/9074a480-c040-497f-8bf6-be4079881c96.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1927831%2F9074a480-c040-497f-8bf6-be4079881c96.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=96bf6b768ddc094f9ae765f063373ff1)

以下のリンクの記事のようなことはVScodeの拡張機能として `Github pull request` を導入するとGithub Copilot Agentから勝手にやってくれるようになります。

拡張機能はカスタマイズできますので、いずれオリジナルの処理ができるようにするCopilot拡張機能のプラットフォームが誕生するかもしれませんね。

## 安い

| ツール | 詳細 | 一日あたりのコスト |
| --- | --- | --- |
| Gemini CLI | 無料枠: 1日1,000リクエストまで 0ドル。これを超過する場合はGemini for Google Cloud: 月額19.00ドル。 | **基本的には0ドル** 、Google Cloud版は月額19ドル/30日 ＝ **約$0.63ドル/日** |
| Claude Code | Pro 17ドル/月 (約6,500メッセージ/月)。 | Sonnet 3.5で **7.80ドル〜/日** 、Opus 4で **39.00ドル〜/日** (トークン消費量による)。 |
| **GitHub Copilot Agent** | 無料枠: 月間50プレミアムリクエスト 0ドル。   Copilot Pro: 10ドル/月 (100ドル/年)。月間300プレミアムリクエスト。   Copilot Pro+: 39ドル/月 ($390/年)。月間1500プレミアムリクエスト。 | Proプランで **0.33ドル/日** (定額)。超過分は0.04ドル/リクエスト。 |
| Devin | Coreプラン: 20ドルから（9ACU相当）。1ACU約2.25ドル。   Teamプラン: 500ドル/月（250ACU含む）。1ACU約2.00ドル。 | Coreプランで1日2時間使用の場合 **約18.00ドル** 。Teamプラン固定費用で **約25.00ドル/日** （超過分は別途）。 |
| OpenHands | ソフトウェア自体は無料。利用するLLMのAPI料金が直接発生。OpenRouter経由で1時間利用で約$30消費の報告あり。 | 利用するLLMと作業量に大きく依存。Mistral Devstralモデルの場合、入力 0.1ドル/Mトークン, 出力 0.3ドル/Mトークン。 |
| Cursor | Hobbyプラン: 無料（限定機能）。   Proプラン: 20ドル/月 (16ドル/月・年額)。月間500プレミアムリクエスト含む。   Ultraプラン: 200ドル/月（Proの20倍の利用量）。 | 限定機能では **0ドル** 。Proプランで **約0.67ドル/日** (定額) + プレミアムリクエスト超過時のモデルに応じた従量課金。独自APIキー利用でコスト最適化の可能性あり。 |

主要自律AIコーディングツールの比較がだいたいこんな感じ。  
料金の仕組みはそれぞれ違うからこうやって比較するのは野暮な気がしますが、  
とりあえず月額とかは一日あたりのコストを割り出してみています。

一番安いのはGemini CLIの無料枠ですね。複数同時稼働とかは難しいけど、対話型として作業を続けていくスピードなら申し分ないと思います。  
ですが、もし課金できる前提であるのであればやっぱGithub Proの一日あたり0.33ドルが結構安いです。  
しかもその値段でいろんなモデル使える。強い。

あと学割でGithub Proはタダでもらえるので、学生の方は最強ですね。  
実際にCopilotが使えるようになるのは申請から72時間後なので、興味がある方がいれば以下のリンクから今すぐ申し込みなさい。

## Github Copilotのここがダメ

チャット履歴は全て、PCへローカル保存されています。  
`\AppData\Roaming\Code - Insiders\User\workspaceStorage` にあります。

よって、別PCから同じチャット履歴で作業を再開したりとかできません。  
CLIじゃないからGeminiみたいにSSHから作業とかもできません。  
Codespacesでいい感じにできないかとも思ったけど、上手くいきませんでした。

しょうがないのでこの記事を書いた人は高校からGoogleリモートデスクトップでちまちま作業をしています。（電池消費がマッハ）

## 最後に

生成AIが流行り始めてからずっと言われていることですが、プロンプトは非常に重要です。  
プロンプト調整でどのツールもめちゃくちゃ性能は変わってくると思います。

ですが、既に現在のAIはプロンプトに依存しない精度を獲得していますし、そういう面もあって「バイブコーディング」＝「雰囲気でもっとゆる～～い指示でやる感じのやつ」というものが流行り始めているのかなと感じます。  
（ちなみに海外ではめちゃくちゃプロンプト組むらしいですよ。仕様書レベルで。日本みたいに適当に語り掛けるっていうのはあんまりないみたいです。ソースはない）

そこで大事になってくるのは、コンテキストの量と質です。これを如何に稼ぎつつ、いかに自動で、かつ分かりやすく制御できるものは何か、と行きついた先が、私はGithub Copilotでした。

Github Copilot Agent最高なので、もっと話題にしてあげてください。

[1](https://qiita.com/CinnamonSea2073/items/#comments)

コメント一覧へ移動

新規登録して、もっと便利にQiitaを使ってみよう

1. あなたにマッチした記事をお届けします
2. 便利な情報をあとで効率的に読み返せます
3. ダークテーマを利用できます
[ログインすると使える機能について](https://help.qiita.com/ja/articles/qiita-login-user)

[新規登録](https://qiita.com/signup?callback_action=login_or_signup&redirect_to=%2FCinnamonSea2073%2Fitems%2F4bca9196723ac48e40b2&realm=qiita) [ログイン](https://qiita.com/login?callback_action=login_or_signup&redirect_to=%2FCinnamonSea2073%2Fitems%2F4bca9196723ac48e40b2&realm=qiita)

[28](https://qiita.com/CinnamonSea2073/items/4bca9196723ac48e40b2/likers)

13