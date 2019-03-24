#!/usr/bin/perl --
#①Perlプログラム本体の場所を記述する。

#ユーザ設定
$CHARSET = 'utf-8';
#②掲示板の文字コードにはUTF-８を使うと定義する
$DATAFILE = './log.txt';
# #③掲示板のログを保存するデータファイルの場所を定義する

#メインプログラム
#④プログラムの本体は、編みがかかっている部分だけである
readFormData();
#⑤ブラウザから送られたフォームのデータを読み込む
readDatafile();
#⑥掲示板のログ保存されているデータファイルを読み込む
writeDatafile();
#⑦掲示板に新しく書き込まれた内容をデータファイルに書き出す
browsePage();
#⑧掲示板の内容をHTMLとして出力する
exit;
#⑨プログラム終了

#フォームデータの読込み
sub readFormData
{
  my ($buffer, $pair);
  # ⑩ローカル変数として$bufferと$pairのペアを定義する
  if ($ENV['REQUEST_METHOD'] eq 'POST') { 
    #⑪もしREQUEST_METHODがPOSTだったら
    read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
    #⑫標準入力(STDIN)から$bufferに環境変数CONTENT_LENGTHに示されている長さ分だけデータを読み込む
  }
  else {
  #⑬REQUEST_METHODがGETだったら・・・
    $buffer = $ENV{'QUERY_STRING'};
    #⑭$bufferに環境変数 QUERY_STRINGの内容を読み込む
  }

  foreach $pair (split(/&/, $buffer)) {
  #⑮$bufferの内容を「&」をデリミタとして分割し、それぞれの$pairに格納する
    my ($name, $value) = split(/=/, $pair);
    #⑯$bufferの内容を「=」をデリミタとして分割し、$nameに前半部、$valueに後半部を格納する

    $value =~ tr/+/ /;
    #⑰$value内の「+」を半角スペースに変換する
    $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/chr(hex($1))/eg;
    #⑱$value内で16進数で示された文字コードを文字に変換する
    $value =~ s/&/&amp;/g;
    #⑲$value内の「&」を「&amp;」という文字列に変換する
    $value =~ s/</&lt;/g;
    #⑳$value内の「<」を「&lt;」という文字列に変換する
    $value =~ s/>/&gt;/g;
    #㉑$value内の「>」を「&gt;」という文字列に変換する
    $value =~ s/¥x0D¥x0A/<br>/g;
    #㉒$value内の「¥x0D¥x0A（改行コード）」を「<br>」という文字列に変換する
    $value =~ tr/¥t/ /;
    #㉓$value内の「¥t（タブ）」の文字を半角スペースに変換する

    $FORM{$name} = $value;
    #㉔$FORM{$name}に$valueの内容を格納する。これによって$FORM{'title'}には題名が、$FORM{'author'}には名前が、$FORM{'text'}には本文が入る
    print "ok1"
  }
}

# データファイルの読み込み
sub readDatafile
{
  open (FIEL, "<$DATAFILE");
  #㉕掲示板のログを保存するデータファイルを入力モードで開き、ファイルハンドルFILEに接続する
  eval{ flock(FILE, 1) };
  #㉖ファイルを共有モードでロックする
  @DATA = <FIEL>;
  #㉗データファイルの内容を１行ごとに配列@DATAの要素として記録する
  close FIEL;
  #㉘ファイルハンドルFILEの接続を解除する
}

# データファイルへの書き出し
sub writeDatafile
{
  if($FORM{'title'} && $FORM{'author'} && $FORM{'text'}) {#㉙もし題名と名前と本文のすべてが書き込まれていたら
    unshift @DATA, "$FORM{'title'}¥t$FORM{'author'}¥t$FORM{'text'}¥n";
    #㉚@DATA配列をずらして先頭部分を空け、空いた先頭部分に今回フォームから入力された題名と名前と本文をタブ（¥t）区切りで書き込む
    open(FILE, ">$DATAFILE");
    #㉛掲示板のログを保存するデータファイルを出力モードで開き、ファイルハンドルFILEに接続する
    eval{ flock(FILE, 2) };
    #㉜ファイルを排他モードでロックする
    print FILE @DATA;
    #㉝配列@DATAの内容をファイルに書き出す
    close FIEL;
    #㉞ファイルハンドルFILEの接続を解除する
  }
}

# 掲示板ページの表示
sub browsePage
{
  print "Content-type: text/html; charset=utf-8";
  print <<END;
<!-- ㉟ENDという文字列が来るまで、下記の内容を画面（標準出力）に書き出す -->

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>掲示板サンプル</title>
  <style type="text/css">
    <!--
    h1 { color:green }
    strong { color: blue; font-size: large }
    em { font-style: italic }
    -->
  </style>
</head>
<body>
  <h1>私の掲示板</h1>

  <p>
  ご自由に書き込んでください
  </p>

  <form action="bbs.cgi" method="post"><div>
    題名<input type="text" name="title" size="60"><br>
    名前<input type="text" name="author" size="20"><br>
    本文<br>
    <textarea cols="60" rows="5" name="text"></textarea><br>
    <input type="submit" value="送信">
    <input type="reset" value="リセット">
  </div></form>
  <hr>
END
#㊱ ENDがあるので、ここまでの内容がprintによって出力されることに成る
  my ($i);
  #㊲ ローカル変数として$iを定義する
  for($i = "0"; $i < @DATA; ++$i) {
    # ㊳$iを0に設定し、@DATA配列の配列数よりも$iが小さい間はforのループを繰り返す。なお、毎回ループが開始される前に$iの値を1増やす
    my ($title, $author, $text) = split(/¥t/, $DATA[$i]);
    # ㊴@DATA配列の$i番目の要素をタブ(¥t)をデリミタとして分割し、ローカル変数として定義した$title, $author, $textにそれぞれ格納する
    print "<div><strong>$title</strong><br><em>$author</em><br><br>$text</div><hr>¥n";
    # ㊵$title, $author, $textをHTMLの一部となるように出力する
  }

  print <<END;
  <!-- ㊶ENDという文字列が来るまで、下記の内容を画面（標準出力）に書き出す -->
</body>
</html>
END

}
#㊷ENDがあるので、ここまでの内容がprintによって出力されることになる

