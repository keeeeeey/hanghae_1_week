
# 제목 : 지식IN over flow
- 배포 URL : www.naver.com
- 구현 유튜브 영상 : www.youtube.com
- github repo 주소 : https://github.com/keeeeeey/hanghae_1_week

## 설명
Stack over flow와 같은, 개발자들이 개발 도중 겪게되는 어려움이나 질문들을 올려 답변을 얻고 공유하는 사이트입니다.
영어로만 이루어진 Stack over flow의 답변이 명쾌하게 와닿지 않고 답답할 때 한글로 된 stack over flow 사이트가 있다면 좀 더 문제해결에 대한 장벽이 낮아지지 않을까 하는 생각에 개발하기로 하였습니다.

### 제작기간, 조원
- 제작기간 : 2022.01.10 ~ 2022.01.13
- 장석우, 김기윤, 김우현, 김선주

### 개발환경 & 기술스택
- 개발환경
	- Pycharm 2021.03
	- MongoDB, robo3T
	- AWS
- 개발언어
	- JavaScript, HTML, CSS, Python

### 페이지 & 기능
- index
	- 질문 리스트
		- 정렬 : 작성순, 답변많은순
		- 검색
		- 
- login
- join
- write
- read
- mypage

images ~~~
### API 설계
|페이지|기능|Method|URL|request|response|
|---|---|---|---|---|---|
|index|검색|POST|`/api/search`|<pre>{<br>  words_give: value <br>}|searched_list|
|login|로그인|POST|`/api/login`|<pre>{<br>  username_give: username,<br>  password_give: password<br>}||
|register|회원가입|POST|`/api/register`|<pre>{<br>  id_give: userid,pw_give: userpw,<br>  nickname_give: usernickname,<br>  email_give: userEmail,<br>  zipcode_give: userZipcode,<br>  address_give: userAddress,<br>  detail_give: userDetailAddress<br>}||
|register|아이디 중복검사|POST|`/api/idCheck`|<pre>{<br>  id_give: userid<br>}|exists(id exists:boolean)|
|register|닉네임 중복검사|POST|`/api/nicknameCheck`|<pre>{<br>  nickname_give: usernickname<br>}|exists(nickname exists:boolean)|
|mypage|회원정보 수정|POST|`/api/updateMember`|<pre>{<br>  pw_give: mypagepw,<br>  zipcode_give: mypageZipcode,<br>  address_give: mypageAddress,<br>  detail_give: mypageDetailAddress<br>}||
|write|질문글 작성|POST|`/api/posting`|<pre>이미지 첨부 X: <br>{<br>  id_give: id,<br>  title_give: title,<br>  content_give: content,<br>  image_checker: image_checker<br>}<pre>이미지 첨부 O: {<br>  id_give: id,<br>  title_give: title,<br>  content_give: content,<br>  image: file,<br>  image_name: filename,<br>  image_checker: image_checker<br> }||
|read|질문글 삭제|POST|`/api/delete`|<pre>{<br>  articleID_give: article_id<br>}||
|read|답변 좋아요 토글, 좋아요 카운팅|POST|`/api/like`|<pre>{<br>  id_give: reply_id,<br>  checker: checker<br> }||
|read|답변 작성|POST|`/api/setReply`|<pre>{<br>  articleID_give: article_id,<br>  reply_give: data<br>}||
|read|질문글 수정|POST|`/api/update`|<pre>{<br>  id_give: id,<br>  title_give: title,<br>  content_give: content<br> }||


### DB 설계
### 직면한 문제와 해결 방안
### 자료들
- S.A(Starting Assignment) / 22.01.10 작성 : https://velog.io/@jsw4215/%ED%95%AD%ED%95%B499-Chapter1-%EC%9B%B9%EA%B0%9C%EB%B0%9C-%EB%AF%B8%EB%8B%88-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8W1-D%EB%B0%98-9%EC%A1%B0
