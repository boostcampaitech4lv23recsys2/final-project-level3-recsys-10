**Usage**
```python
# app 폴더 내에서 아래 명령어 실행
uvicorn main:app --reload --host 0.0.0.0 --port yourport
```

> 예제 코드 출처 : [Flashback 님 : Python - FastAPI DB Connection ( SQLAlchemy )](https://phsun102.tistory.com/m/63)
>
> **주의** : !!slack 에 있는 .env 파일을 /webserver/backend/app/core 에 복사해야 합니다.!!
>
> 👀 FastAPI 에서 Sqlalchemy 를 이용해 GCP Compute Engine 의 MySQL Server 와 연결하는 내용을 담고 있습니다. 
> - `KEYWORD` : Sqlalchemy, GCP Compute Engine, MySQL
>
> **Reference**
> - [Google Compute Engine에서 MySQL을 설정하는 방법](https://cloud.google.com/architecture/setup-mysql?hl=ko#ubuntu)
> - [MySQL ERROR 2003 (HY000): Can't connect to MySQL server on
](https://zetawiki.com/wiki/MySQL_ERROR_2003_(HY000):_Can't_connect_to_MySQL_server_on)
>
> **Recommend**
> - [MySQL GUI : heidisql ](https://www.heidisql.com/download.php)
> ![](https://velog.velcdn.com/images/hobbang2/post/5efb99c6-d264-4a60-a682-1a4911a80e9c/image.png)


# 0. Compute Engine 설치 및 방화벽 설정 
- 참고 : https://velog.io/@hobbang2/ProductServinng-Day76CloudGithub-Action

**설치**
```bash
sudo apt-get install mysql-server
```
**설정**
> 참고 : MySQL 의 default port 는 3306 으로, 아래 config file 에서 변경할 수 있다. 

```bash
sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf

"""내용 수정 ( bind-address = 0.0.0.0 ) 후 wq ( 잘못 고쳤으면 q! ) 
bind-address            = 0.0.0.0
# bind-address          = 127.0.0.1
mysqlx-bind-address     = 127.0.0.1
"""

# 설정 적용을 위해 mysql restart
sudo /etc/init.d/mysql restart
```

# 1. MySQL Server 에 계정 추가 
**SQL Server 접속**
```bash
 mysql -u root -p
```
**User 추가** 
```bash
mysql>  use mysql;
mysql>  CREATE USER 'root'@'%' identified by 'password';

Query OK, 0 rows affected (0.01 sec)
```
**권한 부여** 
```bash
mysql> GRANT ALL PRIVILEGES ON *.* to 'root'@'%';

Query OK, 0 rows affected (0.01 sec)
```

**변경 사항 적용** 
```bash
mysql> flush privileges;

Query OK, 0 rows affected (0.01 sec)
```
**적용 결과 확인** 
```bash
mysql> SELECT Host,User,plugin,authentication_string FROM mysql.user;
```

# 1. Server 확인하기
## 1 ) 지정 ip 에 port 가 열려 있는지 확인하기 
> port 가 열려 있으면 아무런 응답이 오지 않고 command 가 끝남

```bash
nc -z yourip 3306
```
## 2 ) 통신 확인하기
> 멈추고 싶을 때는 ^] 를 입력 

```bash
telnet yourip 3306
```

## 3 ) SQL Server 접속
> mysql 이 설치되어 있어야 함

```bash
mysql -hyourip -uroot -pyourpw
```

# 2. DB Connection 정보 
```bash
# core/config.py
DB_USERNAME = 'username'
DB_PASSWORD = 'password'
DB_HOST = 'hostip' 
DB_PORT = portnum
DB_DATABASE = 'databasename'

f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

---

# session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base # Base 생성
from core.config import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, encoding='utf8')

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()
```

# 3. 결과
![](https://velog.velcdn.com/images/hobbang2/post/e86ecdd9-69f5-443d-a556-88a3f9e5a368/image.png)
