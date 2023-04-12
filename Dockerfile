# 베이스 이미지 설정
FROM timegatime/py_mssql_pyodbc

# 작업 디렉토리 설정
WORKDIR /usr/src/app

# 필요한 파일 복사

COPY requirements.txt ./

# 필요한 라이브러리 설치
RUN pip install -r requirements.txt

# 애플리케이션 파일 복사
COPY ./ ./


CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000", "--insecure"]

EXPOSE 8000

