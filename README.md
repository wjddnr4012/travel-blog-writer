# travel-blog-writer

해외여행 블로그 글(여행 경비 총정리, 일정 후기)을 정해진 스타일로 쓰고, Wikimedia Commons의 자유 라이선스 사진을 찾아 캡션과 출처를 붙여 넣어주는 Agent Skill입니다.

## 설치

```bash
npx skills add wjddnr4012/travel-blog-writer
```

## 사용 예

- "다낭 4박5일 여행 블로그 글 써줘"
- "아이슬란드 오로라 여행 경비 정리 글 써줘. 내용은 랜덤으로"

## 구성

- `skills/travel-blog-writer/SKILL.md`: 글 스타일, 골격, 작업 순서
- `skills/travel-blog-writer/scripts/fetch_commons_images.py`: 자유 라이선스 사진 검색·다운로드와 출처표 생성
- `skills/travel-blog-writer/scripts/contact_sheet.py`: 받은 사진을 한 장에 모아 보는 검수용 미리보기 (Pillow 필요)
- `skills/travel-blog-writer/references/example-shanghai.md`: 완성 예시 글

## 주의

Wikimedia Commons 사진은 대부분 CC BY / CC BY-SA 라이선스라 블로그에 게시할 때 작가명, 라이선스, 원본 링크를 반드시 표기해야 합니다.
