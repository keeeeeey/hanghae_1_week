# 제목 : 지식IN over flow
- 배포 URL : http://54.180.95.5/
- 구현 유튜브 영상 : https://youtu.be/mU6tup7wXwo
- github repo 주소 : https://github.com/keeeeeey/hanghae_1_week

[![구현영상](./static/image/thumbnail_1week.png)](https://www.youtube.com/watch?v=xwqkv2Y31jE)

## 설명
Stack over flow와 같은, 개발자들이 개발 도중 겪게되는 어려움이나 질문들을 올려 답변을 얻고 공유하는 사이트입니다.
영어로만 이루어진 Stack over flow의 답변이 명쾌하게 와닿지 않고 답답할 때 한글로 된 stack over flow 사이트가 있다면 좀 더 문제해결에 대한 장벽이 낮아지지 않을까 하는 생각에 개발하기로 하였습니다.

### 제작기간, 조원
- 제작기간 : 2022.01.10 ~ 2022.01.13
- 장석우, 김기윤, 김우현, 김선주

### 개발환경 & 기술스택
- 개발환경
   - Pycharm
   - MongoDB, robo3T
   - AWS
- 개발언어
   - HTML, CSS, JavaScript, Python

##### JWT(JSON Web Tokens) : Json 포맷을 이용하여 사용자에 대한 속성을 저장하는 Web Token
   - 프로젝트 사용 방법
      - 로그인 시 해당 유저의 정보와 클라이언트에게 제공되지 않는 KEY를 사용해 암호화
      - 암호화된 토큰을 클라이언트 브라우저의 쿠키에 저장
      - 유저가 웹앱을 사용할 시 쿠키에 저장된 값을 받아 서버에서 복호화하여 해당 유저에게 맞는 서비스를 제공할 수 있음
   - 사용하는 이유 : 암호화하지 않고 해당 유저의 정보를 브라우저에 제공 시 브라우저에 저장된 중요 정보를 공격받을 수 있기 때문에 암호화하여 저장
      - 공격 방법 : XSS(Cross Site Scripting), CSRF(Cross Site Request Forgery)
      - 토큰을 저장할 수 있는 곳(브라우저 내) : LocalStorage, Cookie(각각 장단점이 있음)
##### SSR(Server Side Rendering) : 서버 사이드 렌더링
   - SSR은 서버에서 사용자에게 보여줄 페이지를 모두 구성해 보여주는 방식이며, 
초기 로딩 속도가 빠르기 때문에(한 번에 다 읽어오지 않음) 사용자가 컨텐츠를 빨리 볼 수 있습니다.
 SSR의 경우 브라우저에 대한 서버 응답은 렌더링 준비가 된 HTML 페이지인 반면, CSR의 경우 브라우저는 자바스크립트에 대한 링크가 있는 빈 문서를 제공합니다. 이는 브라우저가 모든 자바스크립트가 다운로드되고 실행될 때까지 기다릴 필요 없이 서버에서 HTML 렌더링을 시작한다는 걸 의미한다.

### 페이지 & 기능
##### index: 메인 페이지
   - 헤더
      - 로그인 O
         - 마이페이지 버튼 : 회원정보수정 페이지로 이동
         - 로그아웃 버튼 : 로그아웃
      - 로그인 X
         - 로그인 버튼 : 로그인 페이지로 이동
      - jwt를 이용하여 자동로그인 및 로그인/비로그인 구분
      - 로그인 페이지와 연동
   - 글목록
      - 목록 10개 단위로 페이징 구현
      - 최신순, 조회순 버튼 클릭 시 해당 순서로 목록 변경
      - 검색
         - 검색 목록 표시
         - 검색하기 위해 입력한 글씨에 해당하는 부분 bold 표시
      - 조회수 저장 및 조회수/최신순으로 정렬
      - 글 상세보기 페이지와 연동
   - 글쓰기 버튼 : 질문글 작성 페이지로 이동
##### login: 로그인 페이지
   - 아이디, 비밀번호 작성
      - 입력 조건에 맞지 않을 경우 사용자에게 표시
      - Sign in 버튼 : 로그인 후 메인 페이지로 이동
   - Join 버튼 : 회원가입 페이지로 이동
##### join: 회원가입 페이지
   - 회원정보 입력
      - 아이디 : 4-12자의 영문과 숫자 조합
      - 비밀번호 : 8-20자의 영문과 숫자 조합, 특수문자(!@#$%^&*) 사용 가능
      - 비밀번호 2번 기입 후 일치 여부 확인
      - 닉네임 : 중복 여부 확인
      - 주소 찾기 : 버튼 클릭 시 주소 찾기
      - 입력하지 않거나, 입력 조건에 맞지 않을 경우 사용자에게 표시
      - 회원가입 버튼 : 회원정보 DB에 저장, 로그인 페이지로 이동
   - 뒤로가기 버튼 : 로그인 페이지로 이동
##### write: 질문글 작성 페이지
   - 헤더 (메인 페이지와 같음)
   - 질문 작성
      - 질문, 질문에 해당하는 내용 작성
      - 이미지 첨부 : 첨부된 이미지 파일이름, 이미지 썸네일 미리보기 구현
      - 질문 등록 버튼 : 질문 등록, 메인 페이지로 이동
   - 작성 취소 버튼 : 메인 페이지로 이동
##### read: 질문글, 답변 페이지
   - 헤더 (메인 페이지와 같음)
   - 질문, 질문에 해당하는 내용, 첨부된 이미지 표시
   - 버튼 표시
      - 로그인한 정보와 글 작성자의 정보가 같을 시
         - 수정 버튼 : 작성 글 내용 수정, 해당 페이지 업데이트
         - 삭제 버튼 : 작성 글 삭제, 메인 페이지로 이동
      - 로그인한 정보와 글 작성자의 정보가 다를 시
         - 나가기 버튼 : 메인 페이지로 이동
   - 답변하기 : 답변내용 입력 후 버튼 클릭하면 답변 등록, 해당 페이지 업데이트
      - 좋아요 기능
         - 좋아요 아이콘 클릭 시 해당 답변에 대한 좋아요 카운트 표시
         - 한 회원당 좋아요 한 번 가능
         - 좋아요 취소 가능
      - 답변 작성자와 로그인한 정보가 같을 시
         - 수정 버튼
            - 기존 답변 내용을 포함한 폼에 답변 수정
            - 수정 완료 시 해당 페이지 업데이트
         - 삭제 버튼 : 답변 삭제
   - 수정하기 : 질문, 질문에 해당하는 내용 수정  
        - 수정 폼 : Modal을 이용하여 팝업 생성을 통해 Update form UI 구현


##### mypage: 회원정보수정 페이지
   - 비밀번호를 제외한 회원가입 시 작성한 내용 표시
   - 비밀번호, 주소 변경 가능
   - 변경 내용 작성 후 회원정보 수정 버튼 클릭 시 수정 및 로그인 페이지로 이동

images ~~~
### API 설계
|페이지|기능|Method|URL|request|response|
|---|---|---|---|---|---|
|index|검색|POST|`/api/search`|<pre>{<br>  words_give: value <br>}|searched_list|
|login|로그인|POST|`/api/login`|<pre>{<br>  username_give: username,<br>  password_give: password<br>}||
|register|회원가입|POST|`/api/register`|<pre>{<br>  id_give: userid,<br>  pw_give: userpw,<br>  nickname_give: usernickname,<br>  email_give: userEmail,<br>  zipcode_give: userZipcode,<br>  address_give: userAddress,<br>  detail_give: userDetailAddress<br>}||
|register|아이디 중복검사|POST|`/api/idCheck`|<pre>{<br>  id_give: userid<br>}|exists(id exists:boolean)|
|register|닉네임 중복검사|POST|`/api/nicknameCheck`|<pre>{<br>  nickname_give: usernickname<br>}|exists(nickname exists:boolean)|
|mypage|회원정보 수정|POST|`/api/updateMember`|<pre>{<br>  pw_give: mypagepw,<br>  zipcode_give: mypageZipcode,<br>  address_give: mypageAddress,<br>  detail_give: mypageDetailAddress<br>}||
|write|질문글 작성|POST|`/api/posting`|<pre>이미지 첨부 X: <br>{<br>  id_give: id,<br>  title_give: title,<br>  content_give: content,<br>  image_checker: image_checker<br>}<pre>이미지 첨부 O: {<br>  id_give: id,<br>  title_give: title,<br>  content_give: content,<br>  image: file,<br>  image_name: filename,<br>  image_checker: image_checker<br> }||
|read|질문글 삭제|POST|`/api/delete`|<pre>{<br>  articleID_give: article_id<br>}||
|read|답변 좋아요 토글, 좋아요 카운팅|POST|`/api/like`|<pre>{<br>  id_give: reply_id,<br>  checker: checker<br> }||
|read|답변 작성|POST|`/api/setReply`|<pre>{<br>  articleID_give: article_id,<br>  reply_give: data<br>}||
|read|질문글 수정|POST|`/api/update`|<pre>{<br>  id_give: id,<br>  title_give: title,<br>  content_give: content<br> }||


### DB 설계
![ex_screenshot](./static/image/erd.png)

### 직면한 문제와 해결 방안

- ajax, javascript, html을 이용한 이미지 파일 업로드
ajax, javascript, html을 이용하여 이미지 파일을 전송하여, 이미지파일을 지정 경로에 저장하고, 경로 데이터를 DB에 저장하였습니다.
해당 과정에서, Formdata타입 및 getElementsByClassName과 html 태그 내 class를 file로 선언하는 과정, 그리고 이미지 파일을 불러와
파일명을 분리하는 과정 등, 몰랐던 지식이 많아 구현함에 있어 배울점이 많았습니다.
구현 중 막히는 부분을 구글 검색엔진을 이용하여 검색하고, 주변에 도움을 청해 필요한 새로운 지식을 이해하며 구현하였습니다.

- 좋아요 기능 구현
토글 방식으로 구현하고, API 하나만을 이용하여 좋아요를 구성하였습니다.
다시말해, 좋아요를 누른 유저는 등록이 되어 한번 더 좋아요를 할 수 없으며, 누르면 좋아요가 취소가 됩니다.
어떤 방식으로 좋아요를 누른 유저를 식별할 것인지 생각해내기가 어려웠습니다.
고민 끝에, DB에 해당 댓글이 좋아요를 누른 유저의 정보를 갖고 있도록 하였습니다. 
유저의 정보를 이용하여 이미 좋아요를 누른 유저인지, 아닌지 구별합니다.

- 검색기능 구현
검색을 하면, 해당 단어를 이용하여 DB내의 데이터를 탐색합니다.
서버에서 받아온 데이터를 클라이언트 측(브라우저)에서 어떻게 새로 보여줘야할지에 대한 방법이 어려웠습니다.
페이지를 들어오는 순간 게시글 내 데이터를 전부 받아와 화면에 노출시키는 로직이 이미 구현되어있고,
다른 방식을 사용해야했기에 고민을했습니다만, 기존에 있던 데이터를 이용한 스크립트를 지우고, 검색결과 데이터를
그 위에 보여주는 방식을 선택하였습니다.

### 자료들
- S.A(Starting Assignment) / 22.01.10 작성 : https://velog.io/@jsw4215/%ED%95%AD%ED%95%B499-Chapter1-%EC%9B%B9%EA%B0%9C%EB%B0%9C-%EB%AF%B8%EB%8B%88-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8W1-D%EB%B0%98-9%EC%A1%B0
