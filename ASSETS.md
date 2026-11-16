# 이미지 안내

모든 신규 비주얼은 내장 imagegen 도구로 생성한 임시 콘셉트입니다. 실제 제품 사진이나 확정된 패키지 디자인으로 간주하지 않습니다. 원본 생성 이미지에서 WebP 파일을 파생해 사이트에 사용했습니다.

| 저장 경로 | 용도 |
|---|---|
| `assets/selected/hamster.webp` | 햄스터 대소동 임시 패키지 및 카드 |
| `assets/selected/caelterra.webp` | CAELTERRA 임시 패키지 및 카드 |
| `assets/selected/booster.webp` | 부스터 팩 임시 패키지 |
| `assets/selected/rulebook.webp` | 코어 룰북 임시 표지 |
| `assets/selected/aurelian.webp` | 아우렐리안 제국 콘셉트 |
| `assets/selected/shadow.webp` | 그림자 궁정 콘셉트 |
| `assets/selected/verdant.webp` | 신록의 야생 콘셉트 |
| `assets/selected/ashen.webp` | 잿빛 황무지 콘셉트 |


공통 브랜드 로고와 기존 이미지는 첨부본을 유지합니다. 파비콘은 이전 제작본의 심볼 SVG를 적용했습니다.


## 카엘테라 기본 로고

한국어·영어 홈페이지와 카엘테라 소개 배너는 사용자가 제공한 `카엘테라 로고.png` 원본을 `assets/brand/caelterra-logo.png`에서 불러옵니다.


## v10 절대색감

`assets/selected/absolute-color.webp`는 built-in image_gen으로 제작한 임시 제품 콘셉트입니다. 투명 CMY 도형 파츠, 목표 패턴 카드와 패키지를 표현했습니다. 실제 제품 사양은 아닙니다. 생성 프롬프트는 `IMAGE-PROMPT-absolute-color.md`에 있습니다.


## 카엘테라 웹 이미지 교체

| 사용 위치 | 경로 | 출처 |
| --- | --- | --- |
| 카엘테라 소개 배너 | `assets/caelterra/central-village-portal.webp` | 공유 폴더의 `central_village_portal.png` |
| 게임 목록 및 다른 게임 추천 | `assets/card-art/karden-morvan.webp` | 카르덴 모르반 카드 일러스트 원본 |
| 스타터 세트 | `assets/caelterra/*-card.webp`의 캐릭터 카드 3종 | 카드 관리 도구의 2026-11-02 캐릭터 카드 내보내기 |
| 부스터 팩 | `assets/caelterra/`의 스킬·아이템 카드 3종 | 카드 관리 도구의 2026-11-03 공통 레이아웃 카드 내보내기. 수록 확정 목록이 아닌 카드 예시 |
| 코어 룰북 | `assets/caelterra/rulebook-spread-*.webp` | 제공된 2026-11-13 룰북 정면 PDF의 첫 두 펼침면 |

위 위치에는 사용자 제공 자료의 웹 표시용 WebP를 사용합니다. 기존 카엘테라 임시 콘셉트 파일은 사이트 페이지에서 참조하지 않습니다.

## 회사 소개 브랜드 이미지

제공된 로고의 웹용 이미지인 `assets/brand/scrollrealm-logo-light.png`를 사용합니다. 배경과 선 장식은 `assets/css/studio-pages.css`에서 그립니다.


## 굿즈 콘셉트 이미지

기본 ImageGen 도구로 아래 프롬프트를 사용해 생성했습니다. 웹용 JPEG는 `assets/merchandise/`에 있습니다. 카엘테라 낱장 카드에는 사용자 제공 카드의 기존 `assets/caelterra/` 웹 이미지를 재사용합니다.

- `tunnel.jpg` · Product-mockup for a tabletop game studio shop concept. Wide landscape 3:2 editorial catalog photograph, isolated product centered and fully visible, keep 15% margin on every side. Warm ivory seamless matte studio surface with a quiet natural shadow and clean high-end daylight. No writing, logos, watermark, packaging, props or live animals. Product subject: a curved, low, sand-colored ceramic hamster tunnel with two large smooth oval openings, subtle sunflower relief.
- `bridge.jpg` · Product-mockup for a tabletop game studio shop concept. Wide landscape 3:2 editorial catalog photograph, isolated product centered and fully visible, keep 15% margin on every side. Warm ivory seamless matte studio surface with a quiet natural shadow and clean high-end daylight. No writing, logos, watermark, packaging, props or live animals. Product subject: a low freestanding arch bridge for a hamster habitat, with wide flat pale wood slats, softly rounded corners and no visible hardware.
- `dice.jpg` · Product-mockup for a tabletop game studio shop concept. Wide landscape 3:2 editorial catalog photograph, isolated product centered and fully visible, keep 15% margin on every side. Warm ivory seamless matte studio surface with a quiet natural shadow and clean high-end daylight. No writing, logos, watermark, packaging, props or live animals. Product subject: a matched set of three traditional six-sided tabletop game dice, cream, moss green, and navy, with orderly recessed round pips and softly rounded edges.
- `pawns.jpg` · Product-mockup for a tabletop game studio shop concept. Wide landscape 3:2 editorial catalog photograph, isolated product centered and fully visible, keep 15% margin on every side. Warm ivory seamless matte studio surface with a quiet natural shadow and clean high-end daylight. No writing, logos, watermark, packaging, props or live animals. Product subject: four simple turned wooden board-game pawns in navy, moss, ochre and ivory, all identical in shape, with wide round bases.
- `figure.jpg` · Product-mockup for a tabletop game studio shop concept. Wide landscape 3:2 editorial catalog photograph, isolated product centered and fully visible, keep 15% margin on every side. Warm ivory seamless matte studio surface with a quiet natural shadow and clean high-end daylight. No writing, logos, watermark, packaging, props or live animals. Product subject: one small collectible mini figurine of a golden hamster holding a sunflower seed, on a low round moss-green tabletop miniature base, gentle painted detail.


## 3D 프린팅 햄스터 소품 콘셉트

기본 ImageGen 도구로 제작한 웹용 이미지입니다. 햄스터 집·터널·다리의 상품 목록과 햄스터 집 상세 페이지에 적용했습니다.

- `assets/merchandise/house-3d-print.jpg` · Realistic landscape 3:2 shop catalog product concept photograph. Warm ivory seamless matte studio, three-quarter view, soft window lighting and natural shadow, full object centered with at least 13% margin, high-end simple art direction. Convincing matte filament surface with fine visible 3D printing layer lines. No logos, text, people, live animals, packaging, wood or ceramic. A beautiful low rounded cottage hideout for a hamster habitat, sage green curved removable roof and cream body, a big smooth arch doorway and understated arched roof ribs. One small pressed sunflower motif. Look like a boutique designer 3D printed pet accessory.
- `assets/merchandise/tunnel-3d-print.jpg` · Realistic landscape 3:2 shop catalog product concept photograph. Warm ivory seamless matte studio, three-quarter view, soft window lighting and natural shadow, full object centered with at least 13% margin, high-end simple art direction. Convincing matte filament surface with fine visible 3D printing layer lines. No logos, text, people, live animals, packaging, wood or ceramic. A low gently curved sage green hamster tunnel with two wide openings, clean rounded lips and a sparse raised sunflower motif on the top. Show an object made on an FDM 3D printer from green filament, not pottery.
- `assets/merchandise/bridge-3d-print.jpg` · Realistic landscape 3:2 shop catalog product concept photograph. Warm ivory seamless matte studio, three-quarter view, soft window lighting and natural shadow, full object centered with at least 13% margin, high-end simple art direction. Convincing matte filament surface with fine visible 3D printing layer lines. No logos, text, people, live animals, packaging, wood or ceramic. A low soft terracotta colored wide arched bridge for a hamster habitat, a solid ramp top with fine traction ribs, rounded edges, and a one-piece form suitable for FDM printing. No wood grain, no wooden slats.
