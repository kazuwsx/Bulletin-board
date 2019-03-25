#include <stdio.h>
//① 標準入出力のヘッダをインクルードする

int main(void) {
//② main関数の開始  
  int i;
  //③ 整数型で変数iを定義する
  int countnum;
  //④ 整数型で変数countnumを定義する
  FILE *lockfp;
  //⑤ ロックファイル用のファイルポインタlockfpを定義する
  FILE *countfp;
  //⑥ カウント番号用のファイルポインタcountfpを定義する
  char *lockfile = "lock";
  //⑦ ロックファイルの名前をlockとして定義する
  char *countfile = "count.dat";
  //⑧ カウント番号ファイルの名前をcount.datとして定義する
  for(i=0;i<1000;i++) {
  //⑨ iが0から始まって1000より小さい間、iを1ずつ増やしながらループする
    if( (lockfp = fopen(lockfile, "r")) != NULL) {
    //⑩ もしロックファイルのオープンに失敗しなかったら（つまりロックファイルが存在していたら） 
      fclose(lockfp);
      //⑪ ロックファイルを閉じる
    } else {
      //⑫ もしそうでなかったら（ロックファイルが存在していなかったら）
      lockfp = fopen(lockfile, "w");
      //⑬ ロックファイルを読み込みモードで作成し、lockfpに接続する
      countfp = fopen(countfile, "r+");
      //⑭ カウント番号ファイルを読み込み＋書き込みモードで開き、countfpに接続する
      fscanf(countfp, "%6d", &countnum);
      //⑮ countfpからcountnumに6桁の整数の形式でカウント番号を読み込む
      countnum++;
      //⑯ countnum(カウント番号)の値を1増やす
      rewind(countfp);
      //⑰ countfpのファイルポインタを先頭に戻す
      fprintf(countfp, "%6d", countnum);
      //⑱ countnumからcountfpに6桁の整数の形式でカウント番号を出力する
      printf("%06d", countnum);
      //⑲ countnumの値を6桁の整数の形式で標準出力に出力する
      fclose(countfp);
      //⑳ カウント番号ファイルを閉じる
      fclose(lockfp);
      //㉑ ロックファイルを閉じる
      remove(lockfile);
      //㉒ ロックファイルを削除する
      break;
      //㉓ for文のループを抜ける
    }
  }
  return 0;
}