# Connect Server Project

`connect` 서버를 구축하기 위한 프로젝트입니다.  
이 저장소는 **클라이언트 간 연결 관리**, **안정적인 통신 처리**, **운영 가능한 서버 구조**를 목표로 초기 설계부터 구현까지 단계적으로 진행합니다.

## 프로젝트 목적

- 연결(Connect) 중심의 서버 아키텍처 구현
- 확장 가능한 API/서비스 구조 설계
- 개발 초기부터 문서화와 운영 관점을 함께 반영

## 현재 단계

현재는 프로젝트 킥오프 단계로, 기본 방향과 구조를 정의하고 있습니다.  
이후 단계에서 서버 런타임, 라우팅 구조, 인증/권한, 로깅, 배포 구성을 순차적으로 추가할 예정입니다.

## 앞으로 다룰 내용(예정)

- 서버 기본 구조 및 실행 환경 설정
- 연결 세션 관리 및 상태 처리
- 인증/인가 및 보안 정책
- 모니터링/로깅 및 장애 대응 기반
- 배포 파이프라인 및 운영 자동화

## 문서화 원칙

- 변경사항은 README와 함께 지속적으로 업데이트합니다.
- 초기 설계 의도와 실제 구현 간 차이를 추적 가능하도록 기록합니다.

## 프로젝트 문서

- [Connect 서버 개발 계획서](./CONNECT_SERVER_DEVELOPMENT_PLAN.md)

## 빠른 시작

### 요구 사항
- Node.js 20+
- npm 10+

### 설치
```bash
npm install
```

### 개발 서버 실행
```bash
npm run dev
```

기본 포트는 `3000`이며, 다음 환경 변수를 사용할 수 있습니다.

- `PORT`: 서버 포트 (기본값: `3000`)
- `CONNECT_API_TOKEN`: API 인증 토큰 (기본값: `dev-connect-token`)

### 프로덕션 실행
```bash
npm run build
npm start
```

### 테스트
```bash
npm test
```

## API 개요

### 헬스체크
- `GET /health`

### 세션 API (인증 필요)
아래 엔드포인트는 `Authorization: Bearer <token>` 헤더가 필요합니다.

- `POST /api/v1/sessions`  
  세션 생성 (`clientId` 필요)
- `GET /api/v1/sessions/:id`  
  세션 조회
- `DELETE /api/v1/sessions/:id`  
  세션 종료
