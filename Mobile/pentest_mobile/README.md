# Pentest_mobile no projeto diva (https://github.com/payatu/diva-android)

Projeto para treinar pentest em aplicativos mobiles android :D


# 1 PARTE INSECURE LOGGING

Executa o comando
```
./adb -e shell logcat
```
<p>E logo depois disso conseguiremos ver a senha do cartão no log do dispositivo</p>

- [x] ![alt text](https://github.com/LUCASRENAA/Pentest_mobile/blob/main/imgs/1.png?raw=true)






# 2 PARTE Hardcoding Issues

Executa o comando(Esse comando vai ser útil para quase todas as parte, o código fonte ajuda muito no processo do pentest)
```
localdojadx/jadx diva.apk  -d nome_diretorio

```


ou pode ser o 

```
java -jar /diretorio/apktool.jar b diretorio

```
<p>E logo depois disso conseguiremos ver a senha do vendedor no código fonte</p>

- [x] ![alt text](https://github.com/LUCASRENAA/Pentest_mobile/blob/main/imgs/2.png?raw=true)



<p>Essa vulnerabilidade acontece quando o desenvolvedor acredita que não é possível obter valores de variaveis do programa do código fonte, quando isso na verdade
pode acontecer com o apoio de diversas ferramentas, como o apktools e o jadx. Sendo importante tentar controlar a aplicação através de APIs invés de deixar
senhas e dados sensíveis no código fonte do programa</p>


# 3 PARTE INSECURE DATA STORAGE - PARTE 1 

Executa o comando
```

./adb -e shell
cd /data/data/jakhar.aseem.diva/shared_prefs
cat jakhar.aseem.diva_preferences.xml       

```
<p>E logo depois disso conseguiremos ver os logins e senhas armazenados inseguramente no programa</p>

- [x] ![alt text](https://github.com/LUCASRENAA/Pentest_mobile/blob/main/imgs/3.png?raw=true)




# 4 PARTE INSECURE DATA STORAGE - PARTE 2

Executa o comando
```

./adb -e shell
cd /data/data/jakhar.aseem.diva/databases
sqlite3 ids2
.help
.databases
.tables
select * from myUser;
.q
```
<p>E logo depois disso conseguiremos ver os logins e senhas armazenados inseguramente no programa</p>

- [x] ![alt text](https://github.com/LUCASRENAA/Pentest_mobile/blob/main/imgs/4.png?raw=true)





# 5 PARTE INSECURE DATA STORAGE - PARTE 3

Executa o comando
```

./adb -e shell
cd /data/data/jakhar.aseem.diva 
ls
cat uinfo
```
<p>E logo depois disso conseguiremos ver os logins e senhas armazenados inseguramente no programa</p>

- [x] ![alt text](https://github.com/LUCASRENAA/Pentest_mobile/blob/main/imgs/5.png?raw=true)


# 6 PARTE INSECURE DATA STORAGE - PARTE 4

Executa o comando
```
./adb -e shell
cd /mnt/sdcard
ls -a
cat .uinfo.txt
```
<p>E logo depois disso conseguiremos ver os logins e senhas armazenados inseguramente no programa</p>

- [x] ![alt text](https://github.com/LUCASRENAA/Pentest_mobile/blob/main/imgs/6.png?raw=true)



# 7 PARTE INPUT VALIDATION  ISSUES - PARTE 1 (SQL Injection)

Nem sempre vai ficar tão na cara assim, então é sempre bom abrir o logcate acompanhado de engenharia reversa para encontrar essas falhas, sendo considerada uma falha 
crítica, sqlinjection é muito perigosa
```
./adb -e shell logcat
```
<p>E vamos tentando todas as possiblidades, testando aspas no EditText até encontrar algo no programa.</p>
<p>E o jeito mais comum de sqlinjection é</p>

' or 1 = 1 -- '

- [x] ![alt text](https://github.com/LUCASRENAA/Pentest_mobile/blob/main/imgs/7.png?raw=true)


# 8 PARTE INPUT VALIDATION  ISSUES - PARTE 2 (Visualizando arquivos do celular)

Escreva no EditText
```
file:///data/data/jakhar.aseem.diva/shared_prefs/jakhar.aseem.diva_preferences.xml
```
<p>E logo depois disso conseguiremos ver as informações de dentro do arquivo</p>

- [x] ![alt text](https://github.com/LUCASRENAA/Pentest_mobile/blob/main/imgs/8.png?raw=true)



# 9 PARTE INPUT VALIDATION  ISSUES - PARTE 2 (Visualizando arquivos do celular)



- [x] ![alt text](https://github.com/LUCASRENAA/Pentest_mobile/blob/main/imgs/9_0.png?raw=true)

<p>Antes de tudo, temos que ir no manifest para procurar se conseguimos chamar a intent</p>



- [x] ![alt text](https://github.com/LUCASRENAA/Pentest_mobile/blob/main/imgs/9.png?raw=true)
```
  <intent-filter>
                <action android:name="jakhar.aseem.diva.action.VIEW_CREDS"/>
                <category android:name="android.intent.category.DEFAULT"/>
            </intent-filter>

```

<p>Se a intent-filter estivesse marcado como false, não teria como chamar, mas não está. Então é só rodar esses comandos</p>

```
./adb -e shell am start -n jakhar.aseem.diva/.APICredsActivity -a jakhar.aseem.diva.action.VIEW_CREDS

```
E o resultado é
- [x] ![alt text](https://github.com/LUCASRENAA/Pentest_mobile/blob/main/imgs/9_1.png?raw=true)


# Avisos
Ainda estou terminando de atualizar, pretendo deixar bem legal e com um exemplo de documentação. 
# Certificado
- [x] ![alt text](https://github.com/LUCASRENAA/Pentest_mobile/blob/main/imgs/certificado-pentest-android.png?raw=true)






