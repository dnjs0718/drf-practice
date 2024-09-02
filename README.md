# Django-Rest-Framework practice repository
***

### 도메인 요구사항
- 주소록
  - 목록
    - 목록에 출력될 필드는 다음과 같습니다.
      - 프로필 사진
      - 이름
      - 이메일
      - 전화번호
      - 회사 (직책)
      - 라벨
    - 정렬
      - 기본 출력은 등록 순서대로 정렬합니다.
      - 이름, 이메일, 전화번호 중 하나를 선택하여 정렬할 수 있습니다.
      - 정렬은 오름차순/내림차순/해제 순입니다.
    - 페이징
      - 스크롤 페이징 처리가 되도록합니다.
  - 연락처 (상세보기/입력)
    - 입/출력 필드는 다음과 같습니다.
      - 프로필 사진 : url 입력 방식
      - 이름
      - 이메일
      - 전화번호
      - 회사
      - 직책
      - 메모
      - 라벨
        - 사용자 정의 라벨
        - 연락처 1개에 라벨 다수 연결 가능
      - 기타 항목 추가
        - 주소
        - 생일
        - 웹사이트

***
### 사용 기술 스택
- 기술
  - python 
  - django-rest-framework
  - MySQL

- 가상환경
  - [pipenv](https://github.com/pypa/pipenv)

- API docs
  - [drf-yasg](https://github.com/axnsan12/drf-yasg)
 
- 환경 변수
  - DB_NAME
  - DB_USER
  - DB_PW
  - DB_HOST
  - DB_PORT
  - SECRET_KEY

- 문서
  - 로컬 서버 실행 후 [문서](http://localhost:8000/swagger/) 접속

- 선택 사항
  - 유닛테스트 시행
  - drf-yasg를 활용한 문서화 시행
 
- 초기세팅 
  - `db/schema.sql` 을 통하여 초기 디비 마이그레이션 가능
  - `db/data.sql` 을 통하여 초기 데이터 세팅 가능
