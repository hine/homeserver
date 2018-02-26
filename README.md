# homeserver

## これは何？
RaspberryPiをサーバとして、BlackBeanことeRemote mini/RM mini3をコントロールし、赤外線リモコンデバイスをコントロールできるようにします。

## 事前準備
BlackBeanは手順通り家庭内のWiFiに接続させておいてください。RaspberryPiも同じネットワークに配置する必要があります。

また、Pythonで利用するライブラリをインストールするために、RaspberryPi上で以下の作業を行ってください。(python2環境を想定しています)

### broadlinkライブラリのインストール
```
$ sudo pip install broadlink
```

※このライブラリの使い方は[https://github.com/mjg59/python-broadlink](https://github.com/mjg59/python-broadlink)を読んで下さい。

### TornadoとTornado-JSONのインストール
```
$ sudo pip install tornado
$ sudo pip install Tornado-JSON
```

## インストール
```
$ git clone https://github.com/hine/homeserver.git
$ cd homeserver/
```

## 使い方

### リモコンの学習
操作を記憶させたいリモコンを用意してください。そしてリモコン学習用のスクリプトを実行します。
```
$ python script/blackbean_learn.py
```
そうすると、以下のようなメッセージが順次表示されます。
```
Start Discovering... done
Found a BlackBean
```
ここで、同一のネットワークにBlackbeanが見つけられなかった場合はエラーとなります。
続いて、以下のようなメッセージが表示され、BlackbeanのLEDが白く光ります。
```
Entering Learning Mode... done
Please push IR button once within 15 sec.
```
この時、Blackbeanは学習モードになっているので、ここでBlackbeanに向かって覚えさせたいリモコンのボタンを押します。
```
Success.
```
リモコンの信号をうまく拾うことができればSuccessと表示され、そそれに続いて学習したリモコンデータをhexエンコードした数字の文字列が表示されます。この文字列をコピーしておいてください。

### コマンドの登録
コマンドは、blackbean/commands.pyに記載します。各行にコマンドを一つずつ登録します。サンプルのコードは我が家で実際に利用しているものの一部です。
各行は以下のような構成になっています。
```
'[decice名]/[command名]': 'リモコンの学習データ(hexエンコードしたもの)',
```
前半のキー部分は呼び出し用のURLでも利用するものとなります。

### サーバの起動
ここまでくれば準備完了です。サーバを起動します。
```
python homeserver.py
```

### APIの呼び出し
APIは以下のようなURLとなります。
```
http://[RaspberryPiのIPアドレス]:8888/api/[device名]/[command名]
```
レスポンスはJSONで帰ってきます。以下はレスポンスの例です。
```
{"status": "success", "data": {"received": {"device": "tv", "command": "power"}, "rf_command": "tv/power", "result": "success"}}
```
| キー | 内容 |
----|----
| status | 正しいAPIのURLにアクセスできていればsuccess |
| data | blackbeanプログラムからのレスポンス |

blackbeanプログラムからのレスポンスは以下通りです。

| キー | 内容 |
----|----
| received | APIで渡ってきた[device名]と[command名] |
| rf_command | commands.pyで検索するキー名 |
| result | blackbeanにコマンドを送信できればsuccess |
| error_message | resultがerrorの場合のエラー内容 |

## サーバの自動起動
systemdを用いて、RaspberryPi起動時にサーバを自動的に起動する設定を行います。自動起動の設定ファイルは、このプログラムを/home/pi/homeserver/にインストールした前提で記述しています。別の場所にインストールした場合は、scripts/homeserver.serviceの該当場所を書き換えてください。

まずはサービスを登録します。
```
sudo cp scripts/homeserver.service /etc/systemd/system/
```
サービスを起動してみます。
```
sudo service homeserver start
```
サービスを終了してみます。
```
sudo service homeserver stop
```
無事に起動終了が確認できたら、自動起動の設定を行います。
```
sudo systemctl enable homeserver
```
設定が終われば、RaspberryPiを再起動して、サーバーが自動起動するか確認してください。
