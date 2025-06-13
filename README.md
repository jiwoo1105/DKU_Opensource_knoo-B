# 📚 **KNOO-B** 📺  
### 포텐(14조): 기분에 따른 영화/책 추천 서비스  

---

## 🌟 **프로젝트 소개**
**KNOO-B**는 사용자의 **감정 상태**를 분석하여, **도서**와 **영화**를 추천해주는 **감정 분석 기반 서비스**입니다.  
기분에 맞는 콘텐츠를 추천해줘요! 😊

---

## 👨‍💻 **팀원 소개**
<div style="display: flex; justify-content: space-around; margin-bottom: 20px;">
  <!-- jiwoo1105 Section -->
  <div style="background-color: #f4f4f9; padding: 20px; border-radius: 12px; width: 30%; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
    <h3 style="color: #4CAF50;">**jiwoo1105**</h3>
    <ul style="list-style-type: none;">
      <li>📊 감정 분석 API 연동 및 감정 경계 로직 처리</li>
      <li>📍 유클리드 거리 기반 메타데이터 매칭 시스템 개발</li>
      <li>📉 Matplotlib을 활용한 감정 분석 시각화 시스템 구현</li>
    </ul>
  </div>

  <!-- jeewonkim4206 Section -->
  <div style="background-color: #f4f4f9; padding: 20px; border-radius: 12px; width: 30%; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
    <h3 style="color: #FF9800;">**jeewonkim4206**</h3>
    <ul style="list-style-type: none;">
      <li>🖥 PySide2 기반 사용자 인터페이스 설계 및 개발</li>
      <li>🎨 직관적이고 사용자 친화적인 UI/UX 디자인</li>
      <li>📊 프로젝트 발표 및 시연 자료 제작</li>
    </ul>
  </div>

  <!-- HunJB Section -->
  <div style="background-color: #f4f4f9; padding: 20px; border-radius: 12px; width: 30%; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
    <h3 style="color: #2196F3;">**HunJB**</h3>
    <ul style="list-style-type: none;">
      <li>📚 도서/영화 메타데이터 구조화 및 관리 시스템 구축</li>
      <li>🔍 Hugging Face 기반 도서/영화 검색 시스템 개발</li>
      <li>📖 저자 및 줄거리 정보 자동 추출 및 연동 시스템 구현</li>
    </ul>
  </div>
</div>

---

## 💡 **주요 기능**
1. **사용자 감정 분석** 🔍
2. **도서/영화 메타데이터 기반 추천** 🎬📚
3. **통합 검색 시스템** (도서, 영화, 제목 검색) 🔎
4. **시각화된 분석 결과 제공** 📊

---

## 📅 **회의록 (Meeting Notes)**

> 프로젝트 진행 중 작성된 회의 회의록입니다.

| **날짜**        | **내용 요약**                             | **링크**                        |
|------------------|-------------------------------------------|---------------------------------|
| 2025-05-11       | 프로젝트 초기 계획 수립, 역할 분담 논의   | [보기](./meeting-notes/2025-05-11.md)  |
| 2025-05-18       | GoEmotions 분석 API 연동 및 DB 설계 논의 | [보기](./meeting-notes/2025-05-18.md)  |
| 2025-05-25       | 반대 감정 추출 로직 및 UI 구조 확정       | [보기](./meeting-notes/2025-05-25.md)  |
| 2025-05-31       | 메타데이터 구조화 및 매칭 시스템 구현    | [보기](./meeting-notes/2025-05-31.md)  |
| 2025-06-01       | UI 개선 및 검색 기능 구현, PPT 준비      | [보기](./meeting-notes/2025-06-01.md)  |

---

## 🔧 **Git Commit 컨벤션**
<img width="967" alt="스크린샷 2024-04-08 15 28 23" src="https://github.com/GraduationDku/tastyhub/assets/112964257/ce4f22cd-858b-4695-8fe2-404862b4ee3">
<img width="1630" alt="스크린샷 2024-04-08 15 28 39" src="https://github.com/GraduationDku/tastyhub/assets/112964257/9a536ee7-3b89-4be1-b77e-d098ffd8be60">

---

## 🎥 **구현 영상**
프로젝트 구현 영상을 확인하실 수 있습니다.

[![KNOO-B 구현 영상](https://img.youtube.com/vi/uIsLRql8ePQ/0.jpg)](https://youtu.be/uIsLRql8ePQ)

*위 이미지를 클릭하시면 YouTube에서 영상을 시청하실 수 있습니다.*

## ⚠️ **한계점**
- 사용된 감정 분석 API(`nlp04/korean_sentiment_analysis_dataset3_best`)는 구체적인 행동이나 문장이 포함되지 않은 경우 **정확한 감정 분석**이 어려울 수 있습니다.

---

