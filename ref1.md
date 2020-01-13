	• docker툴박스 다운로드 : https://github.com/docker/toolbox/releases
	• docker search oracle-12c => 오라클 이미지 검색
	• docker-machine stop => 도커 머신 종료, 메모리를 8G로 변경
	• docker-machine start => 도커 머신 시작
	• docker pull truevoly/oracle-12c <= 이미지를 가져옴.
	• docker images => 이미지 확인
	• docker run --name oracle12c -d -p 32765:8080 -p 32764:1521 truevoly/oracle-12c
		○ 컨테이너 만들기 (최초 1 회만)
	• docker logs oracle12c =>설치 완료인지 확인
	• docker ps -a => 구동중인 컨테이너 확인
	• docker start oracle12c => 2번째 부터) 컨테이너 구동
	• docker stop oracle12c => 옵션) 컨데이너 실행 중지
	• docker rm oracle12c => 옵션) 컨테이너 삭제
