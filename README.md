## Intro

> **원티드X프리온보딩 페이히어 팀 프로젝트를 학습 목적으로 처음부터 다시 구현한 레포지토리입니다.**

- 본 프로젝트에서 요구하는 서비스는 가계부(Account Book)입니다.
- 사용자는 본 서비스에 로그인하여, 본인의 소비내역을 기록하고 관리(수정/삭제/복구)할 수 있습니다.
- 사용자는 본 서비스에 로그인하여, 본인의 가계부 리스트와 상세내역을 확인할 수 있습니다.
- 단, 로그인하지 않은 사용자는 가계부 내역에 대한 접근제한 처리가 되어야 합니다.

<br>

> **Index**
- [Team Project](#team-project)
- [Environments](#environments)
- [Personal Project](#personal-project)
- [Etc](#etc)

<br>
<hr>

## Team Project

> **팀 프로젝트 소개**
- #### 👉 [팀 프로젝트 레포지토리 주소](https://github.com/F5-Refresh/payhere)
  ```
   > 과제 제출기업: 페이히어(payhere)
   > 팀명: F5-Refresh
   > 팀원: 5명
   > 프로젝트 기간: 22.07.04 ~ 22.07.08
  ```
<br>
<hr>

## Environments

<br>
<div align="center">
<img src="https://img.shields.io/badge/Python-blue?style=plastic&logo=Python&logoColor=white"/>
<img src="https://img.shields.io/badge/Django-092E20?style=plastic&logo=Django&logoColor=white"/>
<img src="https://img.shields.io/badge/Django Rest Framework-EE350F?style=plastic&logo=Django&logoColor=white"/>
<img src="https://img.shields.io/badge/MySQL-00979D?style=plastic&logo=MySQL&logoColor=white"/>
</div>

<br>
<div align="center">
<img src="https://img.shields.io/badge/AWS EC2-FF9900?style=plastic&logo=Amazon AWS&logoColor=white"/>
<img src="https://img.shields.io/badge/AWS RDS-527FFF?style=plastic&logo=Amazon RDS&logoColor=white"/>
<img src="https://img.shields.io/badge/Docker-%230db7ed.svg?style=plastic&logo=Docker&logoColor=white"/>
<img src="https://img.shields.io/badge/nginx-%23009639.svg?style=plastic&logo=NGINX&logoColor=white"/>
<img src="https://img.shields.io/badge/gunicorn-EF2D5E?style=plastic&logo=Gunicorn&logoColor=white"/>
<img src="https://img.shields.io/badge/Swagger-%23Clojure?style=plastic&logo=swagger&logoColor=white"/>
</div>

<br>
<hr>


## Personal Project

> **Period**
- #### ⚡️ 22.07.10 ~ 22.07.28

<br>

> **Analysis**
- #### 📌 필수 구현사항
  - 사용자 관리: 
    - 회원가입:
      ```
      * 고객은 이메일과 비밀번호를 통해서 회원가입을 할 수 있습니다.
      ```
    - 유저 로그인 및 로그아웃:
      ```
      * 고객은 회원가입 이후, 로그인과 로그아웃을 할 수 있습니다.
      * 고객은 로그인 이후에 가계부 관련 기능을 사용할 수 있습니다.
      * 로그인하지 않은 고객은 가계부에 접근할 수 없습니다.
      ```
  - 가계부:
    - 가계부 생성:
      ```
      * 고객은 가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있습니다.
      ```
    - 가계부 목록:
      ```
      * 고객은 지금까지 기록한 가계부 리스트를 볼 수 있습니다.
      ```
    - 가계부 상세:
      ```
      * 고객은 가계부의 상세한 세부내역을 볼 수 있습니다.
      ```
    - 가계부 수정:
      ```
      * 고객은 가계부의 금액과 메모를 수정할 수 있습니다.
      ```
    - 가계부 삭제/복구:
      ```
      * 고객은 가계부에서 삭제를 원하는 내역을 삭제할 수 있습니다.
      * 단, 삭제한 내역은 언제든지 다시 복구할 수 있어야만 합니다.
      ```
      
- #### 📌 선택 구현사항     
  - 별도의 요구사항이 없는 것은 지원자가 판단해서 개발해주세요.
  - 테스트 케이스 작성시 가산점이 있습니다.
  - Docker를 이용해서 개발시 가산점이 있습니다.
 
- #### 📌 참고사항
  - 언어와 프레임워크는 Python과 Django/Flask/FastAPI로 제한합니다.
  - DB는 MySQL version 5.7을 사용해주세요.
  - html 페이지를 개발하지 않아도 됩니다.
  - 토큰을 발행해서 인증/인가를 제어하는 방식으로 구현해주세요.
  - 구현이 불가능한 부분에 대해서는 가능한 부분까지 구현하는 것을 목표로 해주세요.
  - 모든 코드에는 이유가 있어야 하고 동료에게 설명할 수 있어야 합니다.
  - README에 구현하신 내용(API 및 설계 관련)과 코드에 대한 생각을 자유롭게 작성해주세요.
 
<br>

> **Development**
- #### 🔥 프로젝트 구현기능
  - 사용자 관리:
    - 회원가입
      ```
      > 사용자 회원가입 기능입니다.
      
      * 이메일, 닉네임, 패스워드는 필수값입니다.
      * 전화번호, 프로필 이미지는 선택값입니다.
      * 이메일, 닉네임은 중복되지 않습니다.
      * 패스워드는 반드시 8~20자리의 최소 1개의 소문자/대문자/숫자/(숫자키)특수문자로 구성됩니다.
      * 패스워드는 해싱 후 DB에 저장됩니다.
      ```
    - 로그인
      ```
      > 사용자 로그인 기능입니다.
      
      * DRF-SimpleJwt 라이브리러를 활용했습니다.
      * 이메일, 패스워드는 필수값입니다.
      * 입력받은 이메일과 패스워드가 유저 정보와 일치하는지 확인합니다.
      * 모든 유효성 검사에 통과하면 액세스토큰과 리프레시 토큰을 발급합니다.
      ```
    - 로그아웃
      ```
      > 사용자 로그아웃 기능입니다.
      
      * DRF-SimpleJwt 라이브리러를 활용했습니다.
      * 리프레시 토큰은 필수값입니다.
      * 유효한 토큰인지를 확인합니다.
      * 만료된 토큰인지를 확인합니다.
      * 모든 유효성 검사에 통과하면 요청받은 리프레시 토큰을 토큰 블랙리스트에 등록합니다.
      * 단, 기존에 발급된 리프레시 토큰은 모두 사용을 제한합니다.
      ```
    - 토큰 재발급
      ```
      > 사용자의 토큰을 재발급하는 기능입니다.
      
      * DRF-SimpleJwt의 TokenRefreshView 기능을 활용했습니다.
      * 리프레시 토큰은 필수값입니다.
      * 유효한 토큰인지를 확인합니다.
      * 만료된 토큰인지를 확인합니다.
      * 토큰의 타입을 확인합니다.(오직 리프레시 토큰만 사용가능)
      * 모든 유효성 검사에 통과하면 요청받은 리프레시 토큰을 기반으로 액세스토큰을 발급합니다.
      * 단, 리프레시 토큰은 추가로 발급하지 않습니다.
      ```
  - 가계부:
    - 가계부 목록
      ```
      > 인증/인가에 통과한 사용자는 본인 가계부의 리스트 정보를 조회할 수 있습니다.
      
      * 키워드 검색기능(가계부 이름에 해당 키워드가 검색조건으로 사용)
      * 정렬기능(가계부 생성일자/목표 예산을 기준으로 오름차순, 내림차순 정렬)
      * 필터링 기능(현재 사용중인 가계부/삭제된 가계부 필터링 조회)
      * 페이지네이션 기능(사용자가 원하는 가계부 개수를 정할 수 있음 >> default: 최신순 10개)
      ```
    - 가계부 생성
      ```
      > 인증/인가에 통과한 사용자는 본인의 가계부를 생성할 수 있습니다.
      
      * 사용자는 목표예산을 지정해서 가계부를 생성할 수 있습니다.
      ```
    - 가계부 수정/삭제/복구
      ```
      > 인증/인가에 통과한 사용자는 본인의 가계부를 수정/삭제/복구할 수 있습니다.
      
      - 가계부 수정:
        * 해당 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
        * 사용자는 가계부의 이름과 예산만 수정할 수 있습니다.
        * 가계부의 내용을 부분적으로 수정할 수 있습니다.
        
      - 가계부 삭제(soft delete):
        * 해당 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
        * 이미 삭제된 가계부는 다시 삭제할 수 없습니다.
        
      - 가계부 복구:
        * 해당 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
        * 이미 복구된 가계부는 다시 복구할 수 없습니다.
      ```
  - 가계부 카테고리
    - 가계부 카테고리 목록
      ```
      > 인증/인가에 통과한 사용자는 본인 가계부 카테고리의 리스트 정보를 조회할 수 있습니다.
      
      * 키워드 검색기능(가계부 카테고리 이름에 해당 키워드가 검색조건으로 사용)
      * 정렬기능(가계부 카테고리 생성일자를 기준으로 오름차순, 내림차순 정렬)
      * 필터링 기능(현재 사용중인 카테고리/삭제된 카테고리 필터링 조회)
      * 페이지네이션 기능(사용자가 원하는 카테고리 개수를 정할 수 있음 >> default: 최신순 10개)
      ```
    - 가계부 카테고리 생성
      ```
      > 인증/인가에 통과한 사용자는 본인의 카테고리를 생성할 수 있습니다.
      
      * 사용자는 원하는 이름의 가계부 카테고리를 생성할 수 있습니다.
      ```
    - 가계부 카테고리 수정/삭제/복구
      ```
      > 인증/인가에 통과한 사용자는 본인의 카테고리를 수정/삭제/복구할 수 있습니다.
      
      - 가계부 카테고리 수정:
        * 해당 카테고리가 존재하는지, 본인의 카테고리인지를 확인합니다.
        * 사용자는 카테고리의 이름만 수정할 수 있습니다.
        
      - 가계부 카테고리 삭제(soft delete):
        * 해당 카테고리가 존재하는지, 본인의 카테고리인지를 확인합니다.
        * 이미 삭제된 카테고리는 다시 삭제할 수 없습니다.
        
      - 가계부 카테고리 복구:
        * 해당 카테고리가 존재하는지, 본인의 카테고리인지를 확인합니다.
        * 이미 복구된 카테고리는 다시 복구할 수 없습니다.
      ```
  - 가계부 기록
    - 가계부 기록 목록
      ```
      > 인증/인가에 통과한 사용자는 본인 가계부 기록의 리스트 정보를 조회할 수 있습니다.
      
      * 가계부가 존재하는지, 본인의 가계부인지 확인합니다.
      * 사용자 본인의 가계부 기록만을 리스트 조회합니다.
      * 가계부 기록의 총지출/총수입 데이터를 함께 반환합니다.
      * 사용자의 닉네임을 함께 반환합니다.
      
      - 부가기능:
        * 키워드 검색기능(가계부 기록 제목/설명/카테고리에 해당 키워드가 검색조건으로 사용)
        * 정렬기능(가계부 기록 생성일자/가격을 기준으로 오름차순, 내림차순 정렬)
        * 상태 필터링 기능(현재 사용중인 가계부 기록/삭제된 가계부 기록 필터링 조회)
        * 카테고리 필터링 기능(다수의 카테고리 id를 기준으로 이에 해당되는 가계부 기록 필터링 조회)
        * 타입 필터링(가계부의 타입[expenditure/income]을 기준으로 필터링 조회)
        * 페이지네이션 기능(사용자가 원하는 가계부 기록의 개수를 정할 수 있음 >> default: 최신순 10개)
      ```
    - 가계부 기록 생성
      ```
      > 인증/인가에 통과한 사용자는 본인의 기록을 생성할 수 있습니다.
      
      * 가계부 id는 필수 입력값입니다.(path param)
      * 가계부 카테고리 id는 필수 입력값입니다.(query string)
      * 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
      * 카테고리가 존재하는지, 본인의 카테고리인지를 확인합니다.
      * 사용자는 제목/설명/가격/타입을 지정하여 가계부 기록을 생성할 수 있습니다.
      ```
    - 가계부 기록 수정/삭제
      ```
      > 인증/인가에 통과한 사용자는 본인의 기록을 수정/삭제/복구할 수 있습니다.
      
      - 가계부 기록 수정:
        * 가계부 id는 필수 입력값입니다.(path param)
        * 가계부 기록 id는 필수 입력값입니다.(path param)
        * 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
        * 가계부 기록이 존재하는지, 본인의 기록인지를 확인합니다.
        * 사용자는 기록의 제목/설명/가격/타입만 수정할 수 있습니다.
        
      - 가계부 기록 삭제(soft delete):
        * 가계부 id는 필수 입력값입니다.(path param)
        * 가계부 기록 id는 필수 입력값입니다.(path param)
        * 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
        * 가계부 기록이 존재하는지, 본인의 기록인지를 확인합니다.
        * 이미 삭제된 기록은 다시 삭제할 수 없습니다.
      ```
       
<br>

> **Modeling**
- #### 🚀 ERD 구조
  <img width="1000px" alt="스크린샷 2022-07-26 09 08 13" src="https://user-images.githubusercontent.com/89829943/180895403-641dd300-549b-44f9-ba9e-6e0929cf51e3.png">


<br> 

> **API Docs**
- #### 🌈 API 명세서
  |ID|Feature|Method|URL|
  |---|----------|----|----|
  |1|사용자 회원가입|POST|api/users/signup|
  |2|사용자 로그인|POST|api/users/signin|
  |3|사용자 로그아웃|POST|api/users/signout|
  |4|사용자 토큰 재발급|POST|api/users/token/refresh|
  |5|가계부 생성|POST|api/account-books|
  |6|가계부 리스트|GET|api/account-books|
  |7|게시글 수정|PATCH|api/account-books/\<int:account_book_id\>|
  |8|게시글 삭제|DELETE|api/account-books/\<int:account_book_id\>|
  |9|게시글 복구|PATCH|api/account-books/\<int:account_book_id\>/restore|
  |10|카테고리 생성|POST|api/account-books/categories|
  |11|카테고리 리스트|GET|api/account-books/categories|
  |12|카테고리 수정|PATCH|api/account-books/categories/\<int:account_book_category_id\>|
  |13|카테고리 삭제|DELETE|api/account-books/categories/\<int:account_book_category_id\>|
  |14|카테고리 복구|PATCH|api/account-books/categories/\<int:account_book_category_id\>/restore|
  |15|가계부 기록 생성|POST|api/account-books/\<int:account_book_id\>/logs|
  |16|가계부 기록 리스트|GET|api/account-books/\<int:account_book_id\>/logs|
  |17|게시글 기록 수정|PATCH|api/account-books/\<int:account_book_id\>/logs/\<int:account_book_log_id\>|
  |18|게시글 기록 삭제|DELETE|api/account-books/\<int:account_book_id\>/logs/\<int:account_book_log_id\>|
  
  
- #### ✨ Swagger UI
  #### ```✔️ 사용자 회원가입``` 
  <img width="1000px" alt="스크린샷 2022-07-29 11 13 53" src="https://user-images.githubusercontent.com/89829943/181668672-d319ebc3-a0bf-4b0a-8163-ee0a21598b1b.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 14 16" src="https://user-images.githubusercontent.com/89829943/181668695-175afa5d-5223-4d98-a562-c09333658c4d.png">
  
  #### ```✔️ 사용자 로그인```
  <img width="1000px" alt="스크린샷 2022-07-29 11 17 19" src="https://user-images.githubusercontent.com/89829943/181668976-e847610d-5dd0-4fab-a5fc-c5305b1d90ea.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 17 35" src="https://user-images.githubusercontent.com/89829943/181668993-bbab822b-1c93-49fa-a5d8-b6942beede35.png">
  
  #### ```✔️ 사용자 로그아웃```
  <img width="1000px" alt="스크린샷 2022-07-29 11 21 01" src="https://user-images.githubusercontent.com/89829943/181669401-7540c353-7cdf-41ce-865a-2b3951a0a28b.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 19 44" src="https://user-images.githubusercontent.com/89829943/181669231-9b567817-0029-4f72-b16e-8578a9e2c381.png">

  #### ```✔️ 사용자 토큰 재발급```
  <img width="1000px" alt="스크린샷 2022-07-29 11 22 49" src="https://user-images.githubusercontent.com/89829943/181669666-dc0f3a3c-e93c-4606-bd80-536e445f639a.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 23 06" src="https://user-images.githubusercontent.com/89829943/181669682-b09f3740-e2b1-439c-99bf-ebd5abd633bc.png">

  #### ```✔️ 가계부 생성```
  <img width="1000px" alt="스크린샷 2022-07-29 11 33 52" src="https://user-images.githubusercontent.com/89829943/181670909-8efc2d58-1dba-4a5b-9656-063916bbc9a5.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 32 32" src="https://user-images.githubusercontent.com/89829943/181670921-1d6dfbc2-f566-4653-9f33-5ffaf187892b.png">

  #### ```✔️ 가계부 리스트```
  <img width="1000px" alt="스크린샷 2022-07-29 11 31 20" src="https://user-images.githubusercontent.com/89829943/181671018-271981e9-a821-4ea1-b7ee-b12d325d593e.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 31 41" src="https://user-images.githubusercontent.com/89829943/181671036-aec6bb34-be7f-4758-8ba1-2554e3df13dd.png">

  #### ```✔️ 가계부 수정```
  <img width="1000px" alt="스크린샷 2022-07-29 11 37 34" src="https://user-images.githubusercontent.com/89829943/181671275-5a4c009d-4d4c-44c6-bfa5-599bd1ec3790.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 37 49" src="https://user-images.githubusercontent.com/89829943/181671295-01b37247-5cbd-422b-a7a4-97fab4e4c3cb.png">
  
  #### ```✔️ 가계부 삭제```
  <img width="1000px" alt="스크린샷 2022-07-29 11 40 57" src="https://user-images.githubusercontent.com/89829943/181671774-8e25e3a4-3501-4f8e-9a03-f7f2ceb99dc5.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 41 14" src="https://user-images.githubusercontent.com/89829943/181671787-7a1c37ae-9e23-4a3b-a7ad-87a9bb5828b8.png">
  
  #### ```✔️ 가계부 복구```
  <img width="1000px" alt="스크린샷 2022-07-29 11 41 43" src="https://user-images.githubusercontent.com/89829943/181671807-ed20b865-7d9c-4cc8-ae46-d14b049593c9.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 42 01" src="https://user-images.githubusercontent.com/89829943/181671822-def60e68-5a72-40db-9b94-6caa02c295fd.png">

  #### ```✔️ 카테고리 생성```
  <img width="1000px" alt="스크린샷 2022-07-29 11 44 27" src="https://user-images.githubusercontent.com/89829943/181672215-08b9b9d3-46d0-4e49-a0f2-934a3e664c5b.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 44 52" src="https://user-images.githubusercontent.com/89829943/181672228-ab32d54a-fb9d-4473-9278-2102531bd11c.png">
  
  #### ```✔️ 카테고리 리스트```
  <img width="1000px" alt="스크린샷 2022-07-29 11 45 39" src="https://user-images.githubusercontent.com/89829943/181672253-5a556d4d-f59e-4874-9716-f8fe35a3b504.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 45 58" src="https://user-images.githubusercontent.com/89829943/181672275-bbc6e934-80dd-4f56-bfcc-ed7a7d5c38ea.png">
  
  #### ```✔️ 카테고리 수정```
  <img width="1000px" alt="스크린샷 2022-07-29 11 48 16" src="https://user-images.githubusercontent.com/89829943/181672668-be9c4902-3f79-4c10-82a2-2ff8d81e7f6d.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 48 32" src="https://user-images.githubusercontent.com/89829943/181672681-cad4c28e-ea32-41bb-b5a9-28c9d2108e9c.png">

  #### ```✔️ 카테고리 삭제```
  <img width="1000px" alt="스크린샷 2022-07-29 11 49 01" src="https://user-images.githubusercontent.com/89829943/181672716-c1b0c2df-0d52-4436-9e61-799d79d64cfb.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 49 13" src="https://user-images.githubusercontent.com/89829943/181672732-478b582b-4db4-4185-8136-b6ea5617dc2f.png">

  #### ```✔️ 카테고리 복구```
  <img width="1000px" alt="스크린샷 2022-07-29 11 49 33" src="https://user-images.githubusercontent.com/89829943/181672753-dbd10739-0433-48f0-85a3-7e7d498c5721.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 49 52" src="https://user-images.githubusercontent.com/89829943/181672775-91952330-fe4e-4a6a-bcc7-4079564f48c6.png">

  #### ```✔️ 가계부 기록 생성```
  <img width="1000px" alt="스크린샷 2022-07-29 11 52 54" src="https://user-images.githubusercontent.com/89829943/181673234-b504a310-ca90-4d15-9805-7afce1b8c4cb.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 53 14" src="https://user-images.githubusercontent.com/89829943/181673248-ad68d243-dbfa-4623-9216-aee289541c6a.png">
  
  #### ```✔️ 가계부 기록 리스트```
  <img width="1000px" alt="스크린샷 2022-07-29 11 54 36" src="https://user-images.githubusercontent.com/89829943/181673268-2fc965c5-b785-451b-852c-8a5858f93383.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 55 05" src="https://user-images.githubusercontent.com/89829943/181673286-b66bcfed-29c8-4001-b727-75f788d84ee2.png">

  #### ```✔️ 가계부 기록 수정```
  <img width="1000px" alt="스크린샷 2022-07-29 11 57 52" src="https://user-images.githubusercontent.com/89829943/181673724-5d0e107b-ea24-46ca-b44c-fa4f46f290c5.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 57 52" src="https://user-images.githubusercontent.com/89829943/181673773-31a86efc-f3c6-4412-8335-d89bb2d49829.png">
  
  #### ```✔️ 가계부 기록 삭제```
  <img width="1000px" alt="스크린샷 2022-07-29 11 58 31" src="https://user-images.githubusercontent.com/89829943/181673802-a76326e4-2c63-4b35-ad24-ade999256642.png">
  <img width="1000px" alt="스크린샷 2022-07-29 11 58 54" src="https://user-images.githubusercontent.com/89829943/181673817-73f23193-20fc-4397-8ce1-475e05ff22c5.png">

<br> 

> **Deploy**
- #### 🏖 프로젝트 배포
  #### Docker, Nginx, Gunicorn을 사용하여 AWS EC2 서버에 배포했으며, 비용 등의 이유로 현재는 배포를 중단했습니다.
  <img width="1000px" alt="스크린샷 2022-07-27 08 47 14" src="https://user-images.githubusercontent.com/89829943/181131164-f9bd2137-1f08-4263-9a31-035cd0435af8.png">


<br> 

> **Test**
- #### 🚦 테스트코드 작성
  #### 전체 테스트코드: 119 cases
  
  |ID|Feature|Method|Success cases|Fail cases|
  |---|----|----|----|----|
  |1|사용자 회원가입|POST|1 case|14 cases|
  |2|사용자 로그인|POST|1 case|4 cases|
  |3|사용자 로그아웃|POST|1 case|3 cases|
  |4|사용자 토큰 재발급|POST|1 case|3 cases|
  |5|가계부 생성|POST|1 case|4 cases|
  |6|가계부 리스트|GET|9 cases|1 case|
  |7|가계부 수정|PATCH|1 case|3 cases|
  |8|가계부 삭제|DELETE|1 case|4 cases|
  |9|가계부 복구|PATCH|1 case|4 cases|
  |10|카테고리 생성|POST|1 case|2 cases|
  |11|카테고리 리스트|GET|7 cases|1 case|
  |12|카테고리 수정|PATCH|1 case|3 cases|
  |13|카테고리 삭제|DELETE|1 case|4 cases|
  |14|카테고리 복구|PATCH|1 case|4 cases|
  |15|가계부 기록 생성|POST|1 case|8 cases|
  |16|가계부 기록 리스트|GET|12 cases|3 cases|
  |17|가계부 기록 수정|PATCH|1 case|5 cases|
  |18|가계부 기록 삭제|DELETE|1 case|6 cases|
  <img width="1000px" alt="스크린샷 2022-07-29 07 45 43" src="https://user-images.githubusercontent.com/89829943/181665424-0d4552d0-96d5-4d98-ab8e-22b6c5c435ca.png">
  <img width="1000px" alt="스크린샷 2022-07-29 07 45 58" src="https://user-images.githubusercontent.com/89829943/181665446-02205b2e-d704-4cb6-9f47-6c93fe353367.png">
  
<br> 

> **Issue**
- #### ⏰ 프로젝트 일정관리
  #### 프로젝트 진행사항을 칸반보드와 이슈티켓으로 관리했습니다.
  <img width="1000px" alt="스크린샷 2022-07-28 11 31 18" src="https://user-images.githubusercontent.com/89829943/181666193-757be56a-365a-4efb-bf49-4f4257cb20c8.png">


<br>
<hr>

## Etc

> **Guides**
- #### ⚙️ 프로젝트 설치방법
  #### ```✔️ 로컬 개발 및 테스트용```
  
  1. 해당 프로젝트를 clone하고, 프로젝트 폴더로 이동합니다.
  <br>
  
   ```
   git clone https://github.com/pasitoapasito/wantedP.O-payhere.git
   cd project directory
   ```
  
  2. 가상환경을 만들고, 프로젝트에 필요한 python package를 다운받습니다.
  <br>
  
  ```
  conda create --name project-name python=3.9
  conda activate project-name
  pip install -r requirements.txt
  ```
  
  3. manage.py 파일과 동일한 위치에서 환경설정 파일을 만듭니다.
  <br>
  
  ```
  ex) .env file 
  
  ## general ##
  DEBUG         = True
  ALLOWED_HOSTS = ALLOWED_HOSTS
  SECRET_KEY    = SECRET_KEY

  ## Docker DB ##
  MYSQL_TCP_PORT      = '3306'
  MYSQL_DATABASE      = MYSQL_DATABASE
  MYSQL_ROOT_PASSWORD = MYSQL_ROOT_PASSWORD
  MYSQL_USER          = MYSQL_USER
  MYSQL_PASSWORD      = MYSQL_PASSWORD

  ## AWS RDS ##
  RDS_HOSTNAME = RDS_HOSTNAME
  RDS_DB_NAME  = RDS_DB_NAME
  RDS_USERNAME = RDS_USERNAME
  RDS_PASSWORD = RDS_PASSWORD
  RDS_PORT     = '3306'
  ```
  
  4. project-name/settings.py에서 DB설정을 적절하게 변경합니다.
  <br>
  
  ```
  Docker로 DB를 구축하는 경우 or AWS RDS로 DB를 구축하는 경우 등
  다양한 방법으로 DB를 구축하는 경우에 맞게 DB 설정을 변경합니다.
  
  
  ## Docker DB ##
  DATABASES = {
      'default': {
          'ENGINE'  : 'django.db.backends.mysql',
          'NAME'    : get_env_variable('MYSQL_DATABASE'),
          'USER'    : 'root',
          'PASSWORD': get_env_variable('MYSQL_ROOT_PASSWORD'),
          'HOST'    : 'localhost',
          'PORT'    : get_env_variable('MYSQL_TCP_PORT'),
      }
  }
  
  '''
  ## AWS RDS ##
  DATABASES = {
      'default': {
          'ENGINE'  : 'django.db.backends.mysql',
          'NAME'    : get_env_variable('RDS_DB_NAME'),
          'USER'    : get_env_variable('RDS_USERNAME'),
          'PASSWORD': get_env_variable('RDS_PASSWORD'),
          'HOST'    : get_env_variable('RDS_HOSTNAME'),
          'PORT'    : get_env_variable('RDS_PORT'),
          'OPTIONS' : {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
      }
  }
  '''
  ```
  
  5. DB의 Table 구조를 최신 modeling에 맞게 설정합니다.
  <br>
  
  ```
  python manage.py migrate
  ```
  
  6. 개발용 서버를 실행합니다.
  <br>
  
  ```
  python manage.py runserver 0:8000
  ```

  #### ```✔️ 배포용```
  1. 배포용 서버에서 해당 프로젝트를 clone하고, 프로젝트 폴더로 이동합니다.
  <br>
  
  ```
  git clone https://github.com/pasitoapasito/wantedP.O-payhere.git
  cd project directory
  ```
  
  2. manage.py 파일과 동일한 위치에서 도커 환경설정 파일을 만듭니다.
  <br>
  
  ```
  ex) .env file 
  
  ## general ##
  DEBUG         = True
  ALLOWED_HOSTS = ALLOWED_HOSTS
  SECRET_KEY    = SECRET_KEY

  ## Docker DB ##
  MYSQL_TCP_PORT      = '3306'
  MYSQL_DATABASE      = MYSQL_DATABASE
  MYSQL_ROOT_PASSWORD = MYSQL_ROOT_PASSWORD
  MYSQL_USER          = MYSQL_USER
  MYSQL_PASSWORD      = MYSQL_PASSWORD

  ## AWS RDS ##
  RDS_HOSTNAME = RDS_HOSTNAME
  RDS_DB_NAME  = RDS_DB_NAME
  RDS_USERNAME = RDS_USERNAME
  RDS_PASSWORD = RDS_PASSWORD
  RDS_PORT     = '3306'
  ```
  
  3. project-name/settings.py에서 DB설정을 적절하게 변경합니다.
  <br>
  
  ```
  Docker로 DB를 구축하는 경우 or AWS RDS로 DB를 구축하는 경우 등
  다양한 방법으로 DB를 구축하는 경우에 맞게 DB 설정을 변경합니다.
  
  
  ## Docker DB ##
  DATABASES = {
      'default': {
          'ENGINE'  : 'django.db.backends.mysql',
          'NAME'    : get_env_variable('MYSQL_DATABASE'),
          'USER'    : 'root',
          'PASSWORD': get_env_variable('MYSQL_ROOT_PASSWORD'),
          'HOST'    : 'db',
          'PORT'    : get_env_variable('MYSQL_TCP_PORT'),
      }
  }
  
  '''
  ## AWS RDS ##
  DATABASES = {
      'default': {
          'ENGINE'  : 'django..backends.mysql',
          'NAME'    : get_env_variable('RDS_DB_NAME'),
          'USER'    : get_env_variable('RDS_USERNAME'),
          'PASSWORD': get_env_variable('RDS_PASSWORD'),
          'HOST'    : get_env_variable('RDS_HOSTNAME'),
          'PORT'    : get_env_variable('RDS_PORT'),
          'OPTIONS' : {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
      }
  }
  '''
  ```
  
  4. docker-compose 명령을 사용하여 DB와 Django 서버 컨테이너를 실행시킵니다.
  <br>
  
  ```
  docker-compose -f ./docker-compose.yml up (-d)
  ```

<br>

> **Structure**
- #### 🛠 프로젝트 폴더구조

  ```
  📦account_books
   ┣ 📂migrations
   ┃ ┣ 📜0001_initial.py
   ┃ ┣ 📜0002_alter_accountbook_name.py
   ┃ ┣ 📜0003_alter_accountbookcategory_name_and_more.py
   ┃ ┣ 📜0004_alter_accountbooklog_title.py
   ┃ ┣ 📜0005_alter_accountbook_name_and_more.py
   ┃ ┗ 📜__init__.py
   ┣ 📂tests
   ┃ ┣ 📜__init__.py
   ┃ ┣ 📜tests_account_book_categories.py
   ┃ ┣ 📜tests_account_book_logs.py
   ┃ ┗ 📜tests_account_books.py
   ┣ 📂views
   ┃ ┣ 📜account_book_categories.py
   ┃ ┣ 📜account_book_logs.py
   ┃ ┗ 📜account_books.py
   ┣ 📜__init__.py
   ┣ 📜admin.py
   ┣ 📜apps.py
   ┣ 📜models.py
   ┣ 📜serializers.py
   ┗ 📜urls.py
   📦config
   ┗ 📂nginx
   ┃ ┗ 📜nginx.conf
   📦core
   ┣ 📂migrations
   ┃ ┗ 📜__init__.py
   ┣ 📂utils
   ┃ ┣ 📜decorator.py
   ┃ ┗ 📜get_obj_n_check_err.py
   ┣ 📜__init__.py
   ┣ 📜admin.py
   ┣ 📜apps.py
   ┣ 📜models.py
   ┣ 📜tests.py
   ┗ 📜views.py
   📦payhere
   ┣ 📜__init__.py
   ┣ 📜asgi.py
   ┣ 📜settings.py
   ┣ 📜urls.py
   ┗ 📜wsgi.py
   📦users
   ┣ 📂migrations
   ┃ ┣ 📜0001_initial.py
   ┃ ┣ 📜0002_alter_user_email.py
   ┃ ┗ 📜__init__.py
   ┣ 📂tests
   ┃ ┣ 📜__init__.py
   ┃ ┣ 📜tests_refesh_token.py
   ┃ ┣ 📜tests_signin.py
   ┃ ┣ 📜tests_signout.py
   ┃ ┗ 📜tests_signup.py
   ┣ 📜__init__.py
   ┣ 📜admin.py
   ┣ 📜apps.py
   ┣ 📜models.py
   ┣ 📜serializers.py
   ┣ 📜urls.py
   ┗ 📜views.py
   ┣ 📜.env
   ┣ 📜.gitignore
   ┣ 📜docker-compose.yml
   ┣ 📜Dockerfile
   ┣ 📜manage.py
   ┣ 📜README.md
   ┗ 📜requirements.txt
  ```
