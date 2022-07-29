## Intro

> **원티드X프리온보딩 페이히어 팀 프로젝트를 학습 목적으로 처음부터 다시 구현한 레포지토리입니다.**

- 본 프로젝트에서 요구하는 서비스는 가계부(Account Book)입니다.
- 사용자는 본 서비스에 로그인하여, 본인의 소비내역을 기록하고 관리(수정/삭제/복구)할 수 있습니다.
- 사용자는 본 서비스에 로그인하여, 모든 가계부 리스트와 상세내역을 확인할 수 있습니다.
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
  - 유저관리: 
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
  - README에 구현하시 내용(API 및 설계 관련)과 코드에 대한 생각을 자유롭게 작성해주세요.
 
<br>

> **Development**
- #### 🔥 프로젝트 구현기능
  - 유저관리:
    - 회원가입: 유저 회원가입 기능입니다.
      ```
      * 이메일, 닉네임, 패스워드는 필수값입니다.
      * 전화번호, 프로필 이미지는 선택값입니다.
      * 이메일, 닉네임은 중복되지 않습니다.
      * 패스워드는 반드시 8~20자리의 최소 1개의 소문자, 대문자, 숫자, (숫자키)특수문자로 구성됩니다.
      * 패스워드는 해싱 후 DB에 저장됩니다.
      ```
    - 로그인: 유저 로그인 기능입니다. 
      ```
      * DRF-SimpleJwt 라이브리러를 활용했습니다.
      * 이메일, 패스워드는 필수값입니다.
      * 입력받은 이메일과 패스워드가 유저 정보와 일치하는지 확인합니다.
      * 모든 유효성 검사에 통과하면 액세스토큰과 리프레시 토큰을 발급합니다.
      ```
    - 로그아웃: 유저 로그아웃 기능입니다.
      ```
      * DRF-SimpleJwt 라이브리러를 활용했습니다.
      * 리프레시 토큰은 필수값입니다.
      * 유효한 토큰인지를 확인합니다.
      * 만료된 토큰인지를 확인합니다.
      * 모든 유효성 검사에 통과하면 요청받은 리프레시 토큰을 토큰 블랙리스트에 등록합니다.
      * 단, 기존에 발급된 리프레시 토큰은 모두 사용을 제한합니다.
      ```
    - 토큰 재발급: 유저의 토큰을 재발급하는 기능입니다.
      ```
      * DRF-SimpleJwt의 TokenRefreshView 기능을 활용했습니다.
      * 리프레시 토큰은 필수값입니다.
      * 유효한 토큰인지를 확인합니다.
      * 만료된 토큰인지를 확인합니다.
      * 토큰의 타입을 확인합니다. (오직 리프레시 토큰만 사용가능)
      * 모든 유효성 검사에 통과하면 요청받은 리프레시 토큰을 기반으로 액세스토큰을 발급합니다.
      * 단, 리프레시 토큰은 추가로 발급하지 않습니다.
      ```
  - 가계부:
    - 가계부 목록: 인증/인가에 통과한 사용자는 모든 가계부의 리스트 정보를 조회할 수 있습니다.
      ```
      * 키워드 검색기능(가계부 이름에 해당 키워드가 검색조건으로 사용)
      * 정렬기능(가계부 생성일자/목표 예산을 기준으로 오름차순, 내림차순 정렬)
      * 필터링 기능(현재 사용중인 가계부/삭제된 가계부 필터링 조회)
      * 페이지네이션 기능(사용자가 원하는 가계부 개수를 정할 수 있음 >> default: 최신순 10개)
      ```
    - 가계부 생성: 인증/인가에 통과한 사용자는 본인의 가계부를 생성할 수 있습니다.
      ```
      * 사용자는 목표예산을 지정해서 가계부를 생성할 수 있습니다.
      ```
    - 가계부 수정/삭제/복구: 인증/인가에 통과한 사용자는 본인의 가계부를 수정/삭제/복구할 수 있습니다.
      ```
      > 가계부 수정:
        * 해당 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
        * 사용자는 가계부의 이름과 예산만 수정할 수 있습니다.
        * 가계부의 내용을 부분적으로 수정할 수 있습니다.
        
      > 가계부 삭제(soft delete):
        * 해당 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
        * 이미 삭제된 가계부는 다시 삭제할 수 없습니다.
        
      > 가계부 복구:
        * 해당 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
        * 이미 복구된 가계부는 다시 복구할 수 없습니다.
      ```
  - 가계부 카테고리
    - 가계부 카테고리 목록: 인증/인가에 통과한 사용자는 모든 가계부 카테고리의 리스트 정보를 조회할 수 있습니다.
      ```
      * 키워드 검색기능(가계부 카테고리 이름에 해당 키워드가 검색조건으로 사용)
      * 정렬기능(가계부 카테고리 생성일자를 기준으로 오름차순, 내림차순 정렬)
      * 필터링 기능(현재 사용중인 카테고리/삭제된 카테고리 필터링 조회)
      * 페이지네이션 기능(사용자가 원하는 카테고리 개수를 정할 수 있음 >> default: 최신순 10개)
      ```
    - 가계부 카테고리 생성: 인증/인가에 통과한 사용자는 본인의 가계부 카테고리를 생성할 수 있습니다.
      ```
      * 사용자는 원하는 이름의 가계부 카테고리를 생성할 수 있습니다.
      ```
    - 가계부 카테고리 수정/삭제/복구: 인증/인가에 통과한 사용자는 본인의 가계부를 수정/삭제/복구할 수 있습니다.
      ```
      > 가계부 수정:
        * 해당 카테고리가 존재하는지, 본인의 카테고리인지를 확인합니다.
        * 사용자는 카테고리의 이름만 수정할 수 있습니다.
        
      > 가계부 삭제(soft delete):
        * 해당 카테고리가 존재하는지, 본인의 카테고리인지를 확인합니다.
        * 이미 삭제된 카테고리는 다시 삭제할 수 없습니다.
        
      > 가계부 복구:
        * 해당 카테고리가 존재하는지, 본인의 카테고리인지를 확인합니다.
        * 이미 복구된 카테고리는 다시 복구할 수 없습니다.
      ```
  - 가계부 기록
    - 가계부 기록 목록:
      ```
      * 키워드 검색기능(가계부 기록 제목/설명/카테고리에 해당 키워드가 검색조건으로 사용)
      * 정렬기능(가계부 기록 생성일자/가격을 기준으로 오름차순, 내림차순 정렬)
      * 상태 필터링 기능(현재 사용중인 가계부 기록/삭제된 가계부 기록 필터링 조회)
      * 카테고리 필터링 기능(다수의 카테고리 id를 기준으로 이에 해당되는 가계부 기록 필터링 조회)
      * 타입 필터링(가계부의 타입[expenditure/income]을 기준으로 필터링 조회)
      * 페이지네이션 기능(사용자가 원하는 가계부 기록의 개수를 정할 수 있음 >> default: 최신순 10개)
      * 가계부가 존재하는지, 본인의 가계부인지 확인합니다.
      * 사용자 본인의 가계부 기록만을 리스트 조회합니다.
      * 가계부 기록의 총지출/총수입 데이터를 함께 반환합니다.
      * 사용자의 닉네임을 함께 반환합니다.
      ```
    - 가계부 기록 생성:
      ```
      * 가계부 id는 필수 입력값입니다.(path param)
      * 가계부 카테고리 id는 필수 입력값입니다.(query string)
      * 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
      * 카테고리가 존재하는지, 본인의 카테고리인지를 확인합니다.
      * 사용자는 제목/설명/가격/타입을 지정하여 가계부 기록을 생성할 수 있습니다.
      ```
    - 가계부 기록 수정/삭제:
      ```
      > 가계부 수정:
        * 가계부 id는 필수 입력값입니다.(path param)
        * 가계부 기록 id는 필수 입력값입니다.(path param)
        * 가계부가 존재하는지, 본인의 가계부인지를 확인합니다.
        * 가계부 기록이 존재하는지, 본인의 기록인지를 확인합니다.
        * 사용자는 기록의 제목/설명/가격/타입만 수정할 수 있습니다.
        
      > 가계부 삭제(soft delete):
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
  |ID|Feature|Method|URL|Description|
  |---|----------|----|----|----|
  |1|유저 회원가입|POST|api/users/signup|유저 회원가입 기능입니다.|
  |2|유저 로그인|POST|api/users/signin|유저 로그인 기능입니다.|
  |3|유저 로그아웃|POST|api/users/signout|유저 로그아웃 기능입니다.|
  |4|유저 토큰 재발급|POST|api/users/token/refresh|유저 토큰 재발급 기능입니다.|
  |5|게시글 생성|POST|api/posts|본인의 게시글을 생성합니다.|
  |6|게시글 리스트|GET|api/posts|모든 게시글 리스트 정보를 조회합니다.|
  |7|게시글 상세|GET|api/posts/\<int:post_id\>|모든 게시글 상세 정보를 조회합니다.|
  |8|게시글 수정|PATCH|api/posts/\<int:post_id\>|본인의 게시글을 수정합니다.|
  |9|게시글 삭제|DELETE|api/posts/\<int:post_id\>|본인의 게시글을 삭제합니다.|
  |10|게시글 복구|PATCH|api/posts/\<int:post_id\>/restore|본인의 게시글을 복구합니다.|
  |11|게시글 좋아요|POST|api/posts/\<int:post_id\>/like|본인 게시글 포함, 모든 게시글의 좋아요 기능을 사용합니다.|
  
- #### ✨ Swagger UI
  #### ```✔️ 유저 회원가입``` 
  <img width="1000px" alt="스크린샷 2022-07-25 14 06 34" src="https://user-images.githubusercontent.com/89829943/180702579-5f394884-a7a6-4db7-9658-fe32022c9ced.png">
  <img width="1000px" alt="스크린샷 2022-07-25 14 07 09" src="https://user-images.githubusercontent.com/89829943/180702609-1b2c200c-0f8b-467e-ae44-a3af311a2640.png">
  
  #### ```✔️ 유저 로그인```
  <img width="1000px" alt="스크린샷 2022-07-25 14 14 37" src="https://user-images.githubusercontent.com/89829943/180703475-55f6b39e-1d12-4a0d-bfc8-83182b418fb9.png">
  <img width="1000px" alt="스크린샷 2022-07-25 14 15 16" src="https://user-images.githubusercontent.com/89829943/180703483-651ff118-7495-467d-b205-eadc8db1ad9d.png">
  
  #### ```✔️ 유저 로그아웃```
  <img width="1000px" alt="스크린샷 2022-07-26 08 18 34" src="https://user-images.githubusercontent.com/89829943/180892659-f66e8e82-48a9-4e71-b691-b3aa06ce98ea.png">
  <img width="1000px" alt="스크린샷 2022-07-26 08 18 48" src="https://user-images.githubusercontent.com/89829943/180892691-590d6fe5-cfd4-4437-9d00-3faa8721d509.png">
  
  #### ```✔️ 유저 토큰 재발급```
  <img width="1000px" alt="스크린샷 2022-07-26 08 19 13" src="https://user-images.githubusercontent.com/89829943/180892728-a19efbe5-17bb-4157-9f74-d49094c64cf6.png">
  <img width="1000px" alt="스크린샷 2022-07-26 08 19 49" src="https://user-images.githubusercontent.com/89829943/180892750-47c76600-5fce-4179-aefa-4825981619be.png">

  #### ```✔️ 게시글 생성```
  <img width="1000px" alt="스크린샷 2022-07-25 14 19 09" src="https://user-images.githubusercontent.com/89829943/180703881-f7836fb0-edc6-4e39-a34b-5f63487df411.png">
  <img width="1000px" alt="스크린샷 2022-07-25 14 19 34" src="https://user-images.githubusercontent.com/89829943/180703903-9c6a98b3-7e60-49f2-b072-3157285403f1.png">
  
  #### ```✔️ 게시글 리스트```
  <img width="1000px" height="500px" alt="스크린샷 2022-07-25 14 23 14" src="https://user-images.githubusercontent.com/89829943/180704506-2666460f-9303-437f-a097-57c1d0c4d5ac.png">
  <img width="1000px" alt="스크린샷 2022-07-25 14 24 07" src="https://user-images.githubusercontent.com/89829943/180704527-8a644faa-6240-4007-b77e-c19559d0c0b9.png">
  
  #### ```✔️ 게시글 상세```
  <img width="1000px" alt="스크린샷 2022-07-25 14 29 31" src="https://user-images.githubusercontent.com/89829943/180704936-a1bd6f7e-334c-4406-bee6-5351e3d7401d.png">
  <img width="1000px" alt="스크린샷 2022-07-25 14 29 51" src="https://user-images.githubusercontent.com/89829943/180704952-a4015272-ebfb-44c7-9b40-3691fce2e3e4.png">
  
  #### ```✔️ 게시글 수정```
  <img width="1000px" alt="스크린샷 2022-07-25 14 35 05" src="https://user-images.githubusercontent.com/89829943/180705721-ee0dad11-9766-4f89-8c86-dc490501d399.png">
  <img width="1000px" alt="스크린샷 2022-07-25 14 38 21" src="https://user-images.githubusercontent.com/89829943/180705749-6c7b698d-5e85-4e2e-875f-2d6810888b70.png">

  #### ```✔️ 게시글 삭제```
  <img width="1000px" alt="스크린샷 2022-07-25 14 41 00" src="https://user-images.githubusercontent.com/89829943/180706062-927f16bc-a39c-47e8-bcb8-1bb8bf02fd4f.png">
  <img width="1000" alt="스크린샷 2022-07-25 14 41 16" src="https://user-images.githubusercontent.com/89829943/180706079-da15b387-3e39-4fb3-b4a7-fe680a0b947a.png">

  #### ```✔️ 게시글 복구```
  <img width="1000px" alt="스크린샷 2022-07-25 14 43 04" src="https://user-images.githubusercontent.com/89829943/180706335-55c841bb-1f46-4f6d-a76c-0271a89f8499.png">
  <img width="1000px" alt="스크린샷 2022-07-25 14 43 19" src="https://user-images.githubusercontent.com/89829943/180706359-821c846a-0be1-4843-9ccd-bc2f67d3d4bf.png">

  #### ```✔️ 게시글 좋아요```
  <img width="1000px" alt="스크린샷 2022-07-25 14 45 39" src="https://user-images.githubusercontent.com/89829943/180706665-af18609d-e02f-4b42-81c7-265160689360.png">
  <img width="1000px" alt="스크린샷 2022-07-25 14 45 55" src="https://user-images.githubusercontent.com/89829943/180706681-de52c19c-df98-4d68-b220-5cbf11d43c74.png">
  <img width="1000px" alt="스크린샷 2022-07-25 14 46 09" src="https://user-images.githubusercontent.com/89829943/180706695-fb6b4b03-cfbd-4499-9699-f61421e266d6.png">

<br> 

> **Deploy**
- #### 🏖 프로젝트 배포
  #### Docker, Nginx, Gunicorn을 사용하여 AWS EC2 서버에 배포했으며, 비용 등의 이유로 현재는 배포를 중단했습니다.
  <img width="1000px" alt="스크린샷 2022-07-27 08 47 14" src="https://user-images.githubusercontent.com/89829943/181131164-f9bd2137-1f08-4263-9a31-035cd0435af8.png">


  
<br> 

> **Test**
- #### 🚦 테스트코드 작성
  #### 전체 테스트코드: 67 cases
  
  |ID|Feature|Method|Success cases|Fail cases|
  |---|----|----|----|----|
  |1|유저 회원가입|POST|1 case|14 cases|
  |2|유저 로그인|POST|1 case|4 cases|
  |3|유저 로그아웃|POST|1 case|3 cases|
  |4|유저 토큰 재발급|POST|1 case|3 cases|
  |5|게시글 생성|POST|1 case|4 cases|
  |6|게시글 리스트|GET|12 cases|1 case|
  |7|게시글 상세|GET|1 case|2 cases|
  |8|게시글 수정|PATCH|1 case|3 cases|
  |9|게시글 삭제|DELETE|1 case|4 cases|
  |10|게시글 복구|PATCH|1 case|4 cases|
  |11|게시글 좋아요(생성/취소)|POST|2 cases|2 cases|
  <img width="1000px" alt="스크린샷 2022-07-26 08 24 53" src="https://user-images.githubusercontent.com/89829943/180892935-cf0233dc-2c24-43a3-a07c-06b7e3196b91.png">
  <img width="1000px" alt="스크린샷 2022-07-26 08 25 13" src="https://user-images.githubusercontent.com/89829943/180892946-d815559f-bc95-4bf1-b69e-1c8df5be5f83.png">


<br> 

> **Issue**
- #### ⏰ 프로젝트 일정관리
  #### 프로젝트 진행사항을 칸반보드와 이슈티켓으로 관리했습니다.
  <img width="1000px" alt="스크린샷 2022-07-27 07 44 11" src="https://user-images.githubusercontent.com/89829943/181125089-0ebeb41f-e5d3-4248-912e-212ca7ec281a.png">


<br>
<hr>

## Etc

> **Guides**
- #### ⚙️ 프로젝트 설치방법
  #### ```✔️ 로컬 개발 및 테스트용```
  
  1. 해당 프로젝트를 clone하고, 프로젝트 폴더로 이동합니다.
  <br>
  
   ```
   git clone https://github.com/F5-Refresh/donggyu-sns.git
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
  
  '''
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
  git clone https://github.com/F5-Refresh/donggyu-sns.git
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
  
  '''
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
  ```
  
  4. docker-compose 명령을 사용하여 DB와 Django 서버 컨테이너를 실행시킵니다.
  <br>
  
  ```
  docker-compose -f ./docker-compose.yml up (-d)
  ```
  
> **Structure**
- #### 🛠 프로젝트 폴더구조

  ```
  📦.github
   ┣ 📂ISSUE_TEMPLATE
   ┃ ┣ 📜issue-template.md
   ┃ ┗ 📜issue_template.md
   ┗ 📜pull_request_template.md
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
  📦posts
   ┣ 📂migrations
   ┃ ┣ 📜0001_initial.py
   ┃ ┣ 📜0002_initial.py
   ┃ ┣ 📜0003_remove_post_tags_post_tags.py
   ┃ ┣ 📜0004_accessip.py
   ┃ ┗ 📜__init__.py
   ┣ 📂tests
   ┃ ┣ 📜__init__.py
   ┃ ┣ 📜tests_post_create.py
   ┃ ┣ 📜tests_post_delete.py
   ┃ ┣ 📜tests_post_detail.py
   ┃ ┣ 📜tests_post_like.py
   ┃ ┣ 📜tests_post_list.py
   ┃ ┣ 📜tests_post_restore.py
   ┃ ┗ 📜tests_post_update.py
   ┣ 📜__init__.py
   ┣ 📜admin.py
   ┣ 📜apps.py
   ┣ 📜models.py
   ┣ 📜serializers.py
   ┣ 📜urls.py
   ┗ 📜views.py
  📦sns
   ┣ 📜__init__.py
   ┣ 📜asgi.py
   ┣ 📜settings.py
   ┣ 📜urls.py
   ┗ 📜wsgi.py
  📦users
   ┣ 📂migrations
   ┃ ┣ 📜0001_initial.py
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
