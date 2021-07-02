# BitcoinProject
## 목표
가상화페는 많은 의미로 뜨거운 감자이다. 여러 프로그램들은 자동 매수, 매도를 구현하고 제공하고 있다. 본 프로젝트는 이런 프로그램을 만드는 분들에게 도움을 주기 위해 제작된 것이다. 
본 프로젝트는 가상화폐의 가격등과 같은 정보를 시리얼 통신을 통해 전달하는 것을 목표로 하며, 시리얼 통신을 통해서 자동으로 매수 매도 명령으로 받아 시장가로 처리해준다.

## 기능 


## 사용 방법
1. git을 통해 다운로드한다.:
<pre><code>git clone https://github.com/YouJaeBeom/BitcoinProject.git</code></pre> 
2. 필요한 라이브러리 설치 :
<pre><code> pip install -r requirments.txt </code></pre>
3. 확인하고자 하는 코인명 세팅
> 프로젝트 설치한 위치에 coin.txt 생성, BTC,XRP 와 같은 코인명을 , 로 구분해서 작성 
4. 자동 매매, 매수하고자하는 api key, scret key 세팅
5. 실행하기 :
<pre><code> python bitcoin.py </code></pre>
