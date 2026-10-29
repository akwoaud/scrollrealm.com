# SCROLL REALM 웹사이트 v12

한국어 23페이지와 영어 23페이지, 총 46페이지로 구성된 정적 웹사이트입니다. 기본 글꼴은 SUIT입니다.

이번 변경은 메인 배너의 절대색감 슬라이드 추가입니다. 한국어·영어 모두 CAELTERRA → 햄스터 대소동 → 절대색감 순서의 3개 배너를 표시합니다. 자세한 내용은 `CHANGES-v12.md`를 확인하세요.

v10에서는 절대색감의 게임 목록, 한국어·영어 소개 페이지와 임시 제품 이미지를 추가했습니다. 구매 주소는 `SCROLLREALM_SHOP_URLS.absoluteColor`에서 연결합니다. 자세한 내용은 `CHANGES-v10.md`를 확인하세요.

게임 노출 순서는 제작 순서와 중요도에 따라 **CAELTERRA → 햄스터 대소동 → 절대색감**으로 유지합니다. 메인·Games·다른 게임 목록에 같은 기준을 적용합니다.

## 파일 사용

저장소에서는 사이트 파일이 `dist/`에 있습니다. 배포용 ZIP에는 `index.html`, `assets/`, 각 페이지 폴더가 최상위에 들어 있습니다. 압축을 풀어 `index.html`을 열거나 해당 파일들을 정적 웹 호스팅에 올리면 됩니다.

## 주소 설정

사이트 기준 `assets/js/config.js`에서 다음 항목을 수정합니다.

- `SCROLLREALM_SHOP_URLS`: 실제 네이버스토어 상품 주소. `hamster`는 게임, `hamsterHouse`는 Shop의 햄스터 집 굿즈입니다.
- `SCROLLREALM_SOCIAL_URLS`: Discord, X, Instagram, YouTube의 실제 HTTPS 주소.
- `SCROLLREALM_CONTACT_ENDPOINT`: 실제 문의 접수 서비스의 공개 HTTPS 주소.

SNS 주소를 비워두면 클릭 시 준비 안내를 표시합니다. 문의 접수 주소를 비워두면 실제 전송은 비활성화됩니다. 비밀 API 키나 비밀번호를 설정 파일에 입력하지 마세요.

## 문의 유형과 분류

Contact는 하나의 공통 양식을 사용합니다. 유형 키는 `general`, `retail`, `press`, `other`이며, 선택값을 접수 데이터와 메일 제목에 함께 전달합니다. 실제 접수 서비스와 메일 분류 규칙은 별도로 연결해야 합니다.

설정과 변경 내용은 `CHANGES-v8.md`를 확인하세요. Shop 상세와 메인 배너에 관한 이전 변경은 `CHANGES-v7.md`에 있습니다.

## 상품 정보와 이미지

현재 기획 예시 상품은 판매 전 상태로 표시합니다. 확정되지 않은 가격·사양·출시일을 임의로 입력하지 않았습니다. 콘셉트 이미지 안내와 출처는 `ASSETS.md`를 확인하세요.
