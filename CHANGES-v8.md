# SCROLL REALM — v8

## 문의 창구 통합

- 한국어 / 영어 전체 44페이지 풋터에서 Retailers·Press 중복 링크 제거. Company의 Contact 하나로 통합.
- Contact 양식에 일반·제품 문의, 입점·유통, 취재·미디어, 기타 제안 선택 버튼 추가.
- 선택한 유형에 따라 짧은 작성 안내 변경. 모든 유형은 같은 이름·이메일·제목·문의 내용 필드를 사용.
- 문의 유형은 `category`와 `category_label`로 전달. 메일 제목용 `subject`와 `_subject`에 유형 표시를 붙임. 예: `[입점·유통] 문의 제목`.
- `contact/index.html?type=retail` 또는 `?type=press`처럼 같은 페이지에서 유형을 미리 선택할 수 있음. `general`, `other`도 지원.
- 실제 접수 주소가 없으면 준비 안내를 표시하고 전송을 비활성화. 메시지가 전송되었다고 표시하지 않음.

## SNS 링크

- Discord, X, Instagram, YouTube를 모든 페이지에서 실제 `<a>` 링크로 변경.
- `assets/js/config.js`의 `SCROLLREALM_SOCIAL_URLS`에서 각 채널의 실제 HTTPS 주소를 입력하면 새 탭으로 연결.
- 주소가 빈 채널은 클릭 시 연결 준비 중 안내. JavaScript가 꺼져 있으면 Contact의 공식 채널 안내로 이동.
- 외부 연결에 `noopener noreferrer` 적용. 키보드 선택과 모바일 터치 지원.

## 실제 문의 접수 연결

`assets/js/config.js`의 `SCROLLREALM_CONTACT_ENDPOINT`에 본인이 운영하는 공개 HTTPS 문의 접수 주소를 넣습니다. API 비밀키를 이 파일에 넣으면 안 됩니다.

이 양식은 `multipart/form-data` POST와 JSON 응답을 지원하는 접수 서비스를 사용합니다. Formspree와 같은 양식 접수 서비스를 연결할 수 있습니다. 서비스 측에 필요한 도메인·수신 이메일·스팸 방지 설정은 해당 서비스에서 완료해야 합니다.

전달 필드: `name`, `email`, `topic`, `message`, `category`, `category_label`, `subject`, `_subject`, `_replyto`, `locale`.

유형 키는 언어와 관계없이 `general`, `retail`, `press`, `other`입니다. 관리자 목록은 `category` 필드로 분류하고, 메일함은 연결한 서비스가 사용하는 제목 필드에 맞춰 `[입점·유통]` / `[Retail & distribution]`, `[취재·미디어]` / `[Press & media]` 등의 조건으로 분류 규칙을 설정하면 됩니다.

실제 접수 주소와 SNS 계정 주소는 제공되지 않아 빈 값으로 유지했습니다.

## 확인

- 전체 44페이지의 링크·이미지·앵커와 KO / EN 연결 검사.
- 문의 유형 선택, 유형 사전 선택, 모바일 레이아웃과 SNS 준비 안내 확인.
- 외부 전송이 없는 테스트 환경에서 유형·제목 전달, 성공 상태, 실패 시 입력값 유지 확인.
- 테스트 페이지와 수신 모형은 배포·다운로드 파일에서 제외.
