"""
추상 클래스와 상속, 메소드 오버라이딩의 개념을 활용하여 간단한 은행 계좌 시스템을 구현
추상 클래스를 사용함으로써, 다양한 종류의 계좌(예: 저축 계좌, 체크 계좌 등)를 같은 인터페이스로 관리할 수 있는 유연성을 얻음
어려우면 패스
"""

# Python의 내장 모듈 abc(추상 베이스 클래스)에서 ABCMeta와 abstractmethod를 가져와서 추상 클래스 구현
from abc import ABCMeta, abstractmethod
from random import randint  # randint 함수를 가져와서 랜덤한 숫자 생성 구현(고유한 계좌 번호 생성에 사용)

# Account라는 이름의 추상 클래스를 정의(특정 메소드들의 틀을 제공, 구체적인 내용은 상속받는 하위 클래스에서 정의)
class Account(metaclass=ABCMeta):
    # 계좌 생성 메소드 (추상 메서드로 선언, 상속받는 클래스에서 반드시 구현해야 함.)
    @abstractmethod
    def createAccount(self):
        return 0

    # 계좌 인증 메소드 (추상 메서드)
    @abstractmethod
    def authenticate(self):
        return 0

    # 출금 메소드 (추상 메서드)
    @abstractmethod
    def withdraw(self):
        return 0

    # 입금 메소드 (추상 메서드)
    @abstractmethod          
    def deposite(self):
        return 0

    # 잔액 조회 메소드 (추상 메서드)
    @abstractmethod
    def displaybalance(self):
        return 0

# SavingAccount 클래스로 Account 추상 클래스를 상속받아 실제 은행의 저축 계좌를 모델링
class SavingAccount(Account):
    # 생성자에서는 계좌 정보를 저장할 딕셔너리를 초기화 (예시로 하나의 계좌 정보를 미리 저장해 두었음)
    def __init__(self):
        self.savingAccounts = {"11111" : ["ELLT", 1]}
    
    # 계좌 생성 메소드로 사용자로부터 이름과 초기 입금액을 받아 새로운 계좌를 생성 (계좌 번호는 랜덤)
    def createAccount(self, name, initialDeposite):
        self.accountNumber = str(randint(10000,99999))  # 랜덤한 계좌 번호 생성.
        self.savingAccounts[self.accountNumber] = [name, initialDeposite]  # 계좌 정보 저장.
        print(f"계좌 생성 완료! 계좌 번호는 {self.accountNumber}")  # 사용자에게 계좌 생성 성공 메시지와 계좌 번호를 출력.
    
    # 계좌 인증 메소드에서는 사용자가 제공한 이름과 계좌 번호를 검증하여, 일치하는 경우 인증에 성공한 것으로 처리
    def authenticate(self, name, accountNumber):
        accountNumber = str(accountNumber)
        if accountNumber in self.savingAccounts:  # 계좌 번호가 딕셔너리에 존재하는지 확인
            if self.savingAccounts[accountNumber][0] == name:  # 이름이 일치하는지 확인
                print("인증 성공!")  # 인증 성공 메시지 출력
                self.accountNumber = accountNumber  # 인증된 계좌 번호를 인스턴스 변수에 저장.
                return True
            else:
                print("인증 실패!")  # 이름이 일치하지 않는 경우, 인증 실패 메시지를 출력.
                return False
        else:
            print("인증 실패!")  # 계좌 번호가 존재하지 않는 경우, 인증 실패 메시지를 출력.
            return False

    # 출금 메소드에서는 사용자로부터 출금액을 입력받아 계좌의 잔액과 비교한 후, 충분한 잔액이 있을 경우 출금 처리
    def withdraw(self, withdrawalAmount):
        if self.savingAccounts[self.accountNumber][1] >= withdrawalAmount:  # 출금액이 잔액보다 작거나 같은지 확인.
            self.savingAccounts[self.accountNumber][1] -= withdrawalAmount  # 출금액만큼 잔액에서 차감.
            print("출금 성공!")  # 출금 성공 메시지 출력.
            self.displaybalance()  # 변경된 잔액을 표시.
        else:
            print("잔액 부족!")  # 잔액이 부족한 경우, 해당 메시지를 출력.

    # 입금 메소드에서는 사용자로부터 입금액을 받아 계좌의 잔액에 추가
    def deposite(self, depositeAmount):
        self.savingAccounts[self.accountNumber][1] += depositeAmount  # 입금액을 잔액에 추가.
        print("입금 성공!")  # 입금 성공 메시지 출력.
        self.displaybalance()  # 변경된 잔액을 표시.

    # 잔액 조회 메소드에서는 현재 계좌의 잔액을 사용자에게 표시
    def displaybalance(self):
        print(f"계좌 잔액: {self.savingAccounts[self.accountNumber][1]}")  # 현재 잔액을 출력.

# SavingAccount 클래스의 인스턴스를 생성. 이 인스턴스를 통해 계좌 생성, 인증, 입출금 등의 작업을 수행
savingAccount = SavingAccount()

#사용자가 명시적으로 종료를 선택하기 전까지 무한 loop
while True:
    # 사용자에게 수행할 작업을 선택하도록 안내
    print("1 입력: 계좌 생성")
    print("2 입력: 내 계좌에 접근")
    print("3 입력: 종료")
    userChoice = int(input(""))  # 사용자의 입력을 받아서 정수로 변환

    if userChoice == 1:
        # 사용자가 새 계좌를 생성하길 원하는 경우, 이름과 초기 입금액을 입력받음
        name = input("생성할 계좌의 소유주 이름을 입력하세요.: ")
        initialDeposite = int(input("초기 입금액을 입력하세요.: "))
        # 입력받은 정보를 바탕으로 새 계좌를 생성
        savingAccount.createAccount(name, initialDeposite)

    elif userChoice == 2:
        # 기존 계좌에 접근하길 원하는 경우, 이름과 계좌 번호를 입력받아 인증을 시도
        name = input("계좌의 소유주 이름을 입력하세요.: ")
        accountNumber = int(input("계좌 번호를 입력하세요.: "))
        authenticateStatus = savingAccount.authenticate(name, accountNumber)
        if authenticateStatus:
            # 인증에 성공한 경우, 추가 작업을 선택할 수 있는 내부 루프로 진입
            while True:
                print("1 입력: 출금")  # 출금
                print("2 입력: 입금")  # 입금
                print("3 입력: 잔액 조회")  # 잔액 조회
                print("4 입력: 계좌 종료")  # 내부 루프 종료
                userChoice = int(input(""))
                if userChoice == 1:
                    withdrawAmount = int(input("출금할 돈을 입력하세요.: "))
                    savingAccount.withdraw(withdrawAmount)  # 출금 처리
                elif userChoice == 2:
                    depositeAmount = int(input("입금할 돈을 입력하세요.: "))
                    savingAccount.deposite(depositeAmount)  # 입금 처리
                elif userChoice == 3:
                    savingAccount.displaybalance()  # 잔액 조회
                elif userChoice == 4:
                    break  # 내부 루프를 종료하고, 다시 상위 메뉴로 돌아감

    elif userChoice == 3:
        break  # 사용자가 프로그램 종료를 선택한 경우, 전체 루프를 종료



"""
HW_1:

본인이 직접 클래스를 활용한 코드를 작성해보자.

GPT, 구글링 모두 활용가능.
그러나 코드를 작성할 때, "전체 코드를 작성해줘"와 같은 프롬프트는 최대한 지양하면서 코딩

월요일에 간단히 리뷰 및 발표 그리고 오류가 나는데 모르겠다면 질문 가능합니다!
"""