# Hollow Knight(copy game)
#### 메트로배니아 액션 플랫포머 게임   
대못을 사용한 평타 공격과 영혼을 소모하는 주문을 이용해 적들을 쓰러뜨리고 맵을 탐험한다.   
체력은 가면의 개수로 나타내며 공격을 받으면 가면이 하나씩 깨진다. 적을 공격해서 얻은 영혼은 그릇에 모인다.  
의자에 앉아 회복, 지도 갱신, 게임 저장을 할 수 있다.
부적, 가면, 그릇 등 아이템들을 수집하고 대못을 강화하며 최종보스를 잡는 것이 목적이다.
***
## Game state
1. 로고   
Team Cherry 로고가 잠시 나오고 사라진다.   
2. 타이틀   
게임 시작, 설정, 업적, 더보기, 게임 종료 버튼이 나타난다.     
    - 키보드 이벤트   
    마우스 커서가 사라지고 어느 버튼(메뉴)을 가리키고 있는지 표시한다.  
        - 화살표 - 메뉴 이동
        - 스페이스바/엔터 - 메뉴 선택
        - ESC - 게임 종료 선택
    - 마우스 이벤트   
     커서가 나타나고 어느 버튼을 가리키고 있는지 표시한다.  
        - 마우스 이동 - 메뉴 이동
        - 마우스 클릭 - 메뉴 선택 
    - 메뉴
        - 게임 시작 - 프로필 선택 화면을 띄운다.   
          프로필을 선택하면 해당 프로필의 정보를 불러와 게임을 시작한다.
        - 게임 종료 - 게임을 종료할 것인지 묻는 화면을 띄운다.   
          예를 누르면 게임을 종료하고 아니요를 누르면 타이틀 화면으로 돌아간다.
        
3. 게임 플레이   
본격적으로 게임을 시작한다.   
주인공, NPC, 공격하면 부서지는 모션이 나오는 물건들, 적들이 나타난다.
    - 키보드 이벤트
        - 화살표
            - 좌우 화살표 - 주인공이 좌우로 이동한다.
            - 상하 화살표
                - npc와 대화, 의자에 앉거나 다른 곳으로 이동할 수 있다.
                - 길게 누르면 카메라가 살짝 상하로 움직인다(게임 플레이 중 시야 확보를 위함).   
        - ESC
            - 게임이 일시정지 상태가 되며 메뉴를 띄운다.
                - 계속 - 게임을 계속한다.
                - 설정 - 설정을 바꾼다.
                - 종료하고 메뉴로 이동 - 현재 진행상황을 저장하고 타이틀 화면으로 이동한다.
        - z
            - 대못을 이용한 평타 공격을 한다.
            - 화살표 키와 같이 누르면 해당 방향으로 공격한다.
        - x
            - 점프한다. 길게 누를 수록 높이 점프한다.
        - c
            - 돌진(대시)한다.
        - a
            - 길게 누르면 체력을 회복하고 짧게 누르면 공격 주문이 나간다.
        - Tab
            - 누르고 있는 동안 지도를 본다.  
            지도를 보는 동안 주인공의 이동 속도가 느려진다.
        
***
## 필요한 기술
1. 충돌 처리
    - 전투
        - 적과 닿거나 적의 공격에 닿았을 때
    - 필드 이동
        - 가시, 톱날에 닿거나 산성 용액에 닿았을 때
        - 지형지물에 착지하거나 매달릴 때
2. 키보드/마우스 입력 처리      
3. 더블 버퍼링/애니메이션
4. 사운드
    - 장소, 상황에 따른 배경음악
    - 주인공, 적 움직임에 관한 효과음(공격, 피격, 점프, 착지 등)
5. 맵 제작
    - 지형지물 생성, 관리
6. 파일 입출력
    - 진행 상황 저장 및 불러오기    

***
## 개발 범위
![필드](https://user-images.githubusercontent.com/70762557/95732501-cb0d5b80-0cbb-11eb-83e4-9246420f90a4.PNG)   
일반 필드에서 몹과 싸우고 지형지물을 밟아 올라가며 주인공의 기본 조작을 익힙니다.  
만약 주인공이 체력의 개수가 0이 되어 게임 오버가 되면 다시 게임을 시작할 때 이 필드에서부터 시작하게 됩니다.   

![마을](https://user-images.githubusercontent.com/70762557/95732506-cc3e8880-0cbb-11eb-8a64-135ed65ddff3.PNG)   
마을에는 의자가 있고, 의자에 앉아서 체력을 모두 회복할 수 있습니다.   

![보스](https://user-images.githubusercontent.com/70762557/95732513-ce084c00-0cbb-11eb-9938-eabdebad4d92.PNG)   
보스를 처치하고 나면 보스방에서 왼쪽으로 나갈 수 있습니다. 왼쪽으로 나가면 게임 클리어 화면이 나왔다가 타이틀 화면으로 돌아갑니다. 

![개발범위](https://user-images.githubusercontent.com/70762557/95712217-617f5400-0c9f-11eb-9b69-058d97087468.PNG)   

## 개발 일정
![개발 일정](https://user-images.githubusercontent.com/70762557/95712267-75c35100-0c9f-11eb-8a83-617bf993b1e1.PNG)   


***
## 진행 상황   
![진행상황](https://user-images.githubusercontent.com/70762557/99884718-aff71980-2c73-11eb-88c9-18d700cacf35.PNG)   

## 주차별 커밋   
![commits](https://user-images.githubusercontent.com/70762557/99884721-b1284680-2c73-11eb-94de-a4d39d6fdf98.PNG)   

## Game Objects   
### knight   
![classes](https://user-images.githubusercontent.com/70762557/99884719-b1284680-2c73-11eb-99a5-4913d009859c.PNG)
![관계도](https://user-images.githubusercontent.com/70762557/99884723-b1c0dd00-2c73-11eb-8fe7-cf4ca2bc1ddb.PNG)   
주황색: 이벤트를 받으면 전환되는 관계   
파란색: 자동으로 전환되는 관계   

### ui   
![frame](https://user-images.githubusercontent.com/70762557/99884722-b1c0dd00-2c73-11eb-8ce8-03c5011b49eb.PNG)   
frame은 health(mask)를 가지고 있으며 mask의 애니메이션을 결정한다.   

### crawlid   
![crawlid](https://user-images.githubusercontent.com/70762557/99885111-fc435900-2c75-11eb-91c7-cd9d948d94b5.PNG)   
walk, death 애니메이션이 있다.

***
## 진행 상황   
![진행상황](https://user-images.githubusercontent.com/70762557/101285426-7b18c400-3828-11eb-8a6a-33419c7268b4.PNG)   
평타 위아래 공격과 의자 구현 못했습니다.   
   
## 주차별 커밋   
![commits_week](https://user-images.githubusercontent.com/70762557/101285422-76541000-3828-11eb-9336-a70515c51052.png)   
   
## 플레이 영상 캡쳐
![캡쳐1](https://user-images.githubusercontent.com/70762557/101285564-40635b80-3829-11eb-9d9e-ffc8bd50ee69.png)   
![캡쳐2](https://user-images.githubusercontent.com/70762557/101285566-41948880-3829-11eb-9336-4719fc6f10a4.png)   
   
## 인터뷰   
![함1](https://user-images.githubusercontent.com/70762557/101285429-7ce28780-3828-11eb-8417-cd082774b429.jpg)   
![함2](https://user-images.githubusercontent.com/70762557/101285436-7e13b480-3828-11eb-99db-831b4fa39514.jpg)   
이후에 점프 오류 수정했습니다.  
   
## 발표 영상   
1차 발표: https://youtu.be/g6ptzB0o2AY   
2차 발표: https://youtu.be/PtD4GkplWzc   
3차 발표: https://youtu.be/yORJ5L83FPk   
