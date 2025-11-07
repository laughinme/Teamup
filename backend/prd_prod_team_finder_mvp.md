# PROD Team Finder — PRD (MVP)

> Платформа под Олимпиаду PROD: поиск команды и участников (3–5 человек), быстрый онбординг, «For You» рекомендации, заявки/инвайты, модерация и экспорт.

---

## 1) Цели и метрики
**Цель продукта:** централизовать сбор команд и участников финала PROD, снизить хаос в Telegram-чате, ускорить матчинг.

**Ключевые метрики (MVP):**
- TTFM (time-to-first-match): медиана времени от регистрации до первого принятого инвайта/заявки ≤ 24 ч.
- CR онбординга → заполненный профиль ≥ 85%.
- ≥ 70% участников финала имеют хотя бы 1 релевантный матч в «For You» в первые 12 ч.
- ≥ 50% команд комплектуются до требуемых 3–5 человек за N дней (установить для пилота).

**Анти-метрики:**
- Спам-заявки (>5 отклонений подряд от одного кандидата) — мониторинг и лимиты.
- Дубликаты команд/профилей — детект и слияние/бан.

---

## 2) Персоны и сценарии
**Участник-соло (Seeker):**
- Заполнить профиль (направление: backend/frontend/mobile/mlops; стек; уровни; опыт; победы/кейсы; часовой пояс; язык общения; предпочтения по ролям).
- Смотреть «For You» и каталог команд, фильтровать, подавать заявки.

**Капитан/Команда (Team Owner/Admin):**
- Создать команду, описать стек/рольные слоты (например, нужен 1 MLops + 1 frontend), публичность, ожидания, расписание.
- Принимать/отклонять заявки, отправлять инвайты конкретным участникам.

**Организатор (Admin/Moderator):**
- Просматривать и модерировать профили/команды.
- Экспорт CSV (участники, команды, статусы заявок/инвайтов, контакты).

---

## 3) Scope MVP vs Next
**MVP:**
- Регистрация/логин (email magic-link + опционально Telegram OAuth позже).
- Онбординг профиля участника.
- Создание и управление командой (1 владелец, роли участников, статусы: invited, applied, accepted, rejected, left).
- Каталог (участники/команды), фильтры, Postgres Full-Text Search + триграммы.
- «For You» – детерминированные рекомендации на базе анкеты (см. Алгоритм).
- Система заявок/инвайтов, уведомления (in‑app) + email.
- Админ-панель (базовая) + экспорт CSV.

**Later:**
- Чат/DM, Telegram-бот нотификаций.
- SSO через список допущенных финалистов (импорт).
- Интеграция с LMS ВШЭ (экспорт/вебхуки).
- Антиспам ML‑эвристики, скоринг статуса профиля.
- Мобильная PWA.

---

## 4) Архитектура и техстек
**Бэкенд:** FastAPI (ASGI, Pydantic v2, SQLAlchemy 2.0 async, Alembic), PostgreSQL 16, Redis, RabbitMQ.
- Стиль: модульный монолит c явным service layer + repository pattern.
- DI: FastAPI `Depends`.
- Кэш: Redis (идемпотентность, счетчики, feed cache).
- Очереди: RabbitMQ (доменные события + outbox pattern).
- Тесты: Pytest, coverage gates, factory-boy, httpx.
- Логирование/трейсинг: structlog + OpenTelemetry (опционально).

**Фронтенд:** React + Vite, TypeScript, shadcn/ui, Tailwind, TanStack Query, React Router.
- Формы: react-hook-form + zod.
- Состояние: Server State через Query; минимум client state.
- i18n (ru/en) — позже.

**DevOps:** Docker Compose (pg, redis, rabbit, app-api, app-web), pre-commit (ruff/black/isort), `.env`/Vault, GitHub Actions CI (lint/test/migrate).

**NB:** _«Соблюдать существующий шаблон/архитектуру репозитория пользователя»_ — именование пакетов, схемы импорта, конфиги, слои (domain → repository → service → api), кодстайл и линтеры — **не отклоняться**.

---

## 5) Доменные модели (ERD)
```
users (id, email, name, telegram, timezone, created_at, updated_at)
profiles (id, user_id FK, direction ENUM[backend, frontend, mobile, mlops], bio, experience_level ENUM[junior, middle, senior], achievements[], languages_spoken[], preferred_langs_code[], time_commitment ENUM[low, medium, high], visibility ENUM[public, private])
tech_tags (id, slug, kind ENUM[language, framework, tool])
profile_tech_tags (profile_id FK, tech_tag_id FK, level ENUM[1..5])
teams (id, owner_user_id FK, name, description, direction ENUM[...]|NULL(mixed), visibility ENUM[public, private], status ENUM[draft, recruiting, full], created_at)
team_needs (id, team_id FK, direction ENUM[...], required_level ENUM[junior..senior], must_tags[], nice_tags[], slots INT, notes)
team_members (team_id FK, user_id FK, role ENUM[owner, member], status ENUM[invited, applied, accepted, rejected, left], joined_at, left_at)
applications (id, team_id FK, user_id FK, message, status ENUM[pending, accepted, rejected, withdrawn], created_at, updated_at)
invites (id, team_id FK, user_id FK, message, status ENUM[pending, accepted, rejected, expired], created_at, updated_at, expires_at)
notifications (id, user_id FK, kind, payload JSONB, read_at, created_at)
admin_audit (id, actor_user_id, action, entity, entity_id, diff JSONB, created_at)
```
**Индексы:**
- FTS: `profiles.search_vector` (bio + achievements + tech_tags names/slug), GIN.
- Триграммы: `gin_trgm_ops` на `teams.name`, `profiles.bio`.
- Частичные: `team_members(status='accepted')`.

---

## 6) Роли и доступы (RBAC)
- `admin` — полный доступ, модерация, экспорт.
- `organizer` — просмотр всех, экспорт, блокировки.
- `participant` — CRUD своего профиля, своих команд, заявок/инвайтов.
- Политика маршрутов: **require_any(roles)** с «блоком старших ролей» — `admin`/`organizer` автоматически проходят любые
проверки *participant*‑уровня.

---

## 7) Поиск и рекомендации
**Фильтры каталога:** направление, теги стека (must/nice), уровень, часовой пояс, язык общения, статус (ищу команду/ищу участников), заполненность профиля.

**Скоринг «For You» (эвристика MVP):**
- Жесткие фильтры: совпадение выбранного направления и доступных слотов в командах.
- Очки совпадения (пример):
  - Обязательные теги команды vs профиль: +5 за каждый must, −∞ если must отсутствует.
  - Nice-to-have совпадения: +2 каждый.
  - Уровень: точное совпадение +3; ±1 уровень +1; иначе 0.
  - Временная совместимость (timezone ±2 ч): +2.
  - Общий язык общения (ru/en): +2.
  - Предпочтение «вступить в существующую/собрать свою» — приоритетный ранжирующий множитель x1.2.
- Итог: `score = Σ(компоненты)`; top‑N выдача.
- Обновление кеша Redis: ключ `feed:{user_id}` TTL 15 мин; инкрементальное обновление при изменениях профиля/команд (RMQ события).

**Анти‑паттерны:**
- Не показывать команду, если пользователь уже подал заявку/получил отказ/состоит.
- Дедуп по owner‑близости: не спамить вариантами одной команды, если слотов много.

---

## 8) Флоу заявок/инвайтов
1) Участник → Команда: *create application (pending)* → владелец/админы команды **accept/reject**.
2) Команда → Участник: *create invite (pending)* → пользователь **accept/reject** (авто‑join при accept).
3) При accept: проверка лимита 5 участников. При достижении — статус команды `full`, рекрутинг скрывается из каталога.
4) События в RMQ: `application.created`, `application.updated`, `invite.created`, `invite.updated`, `team.member.joined`, `team.full`.

---

## 9) API (контуры контракта)
Base URL: `/api/v1`

**Auth**
- `POST /auth/magic/request` {email}
- `POST /auth/magic/verify` {token}
- `POST /auth/logout`

**Profile**
- `GET /me` → User + Profile
- `PUT /profiles/me` → update profile
- `GET /profiles` (q, filters, paging)
- `GET /profiles/{id}`

**Teams**
- `POST /teams` → create
- `GET /teams` (q, filters, paging)
- `GET /teams/{id}` → detail (+ needs, members)
- `PUT /teams/{id}` → update (owner|admin)
- `POST /teams/{id}/needs` → CRUD слоты

**Applications/Invites**
- `POST /teams/{id}/applications`
- `GET /me/applications` (as candidate)
- `POST /applications/{id}/accept|reject|withdraw`
- `POST /teams/{id}/invites` {user_id}
- `GET /me/invites` (as recipient)
- `POST /invites/{id}/accept|reject`

**Feed**
- `GET /feed/for-you` → [{entity_type, entity_id, score, reason}]

**Admin**
- `GET /admin/export.csv?scope=teams|profiles|members|applications`
- `POST /admin/moderation/{entity}/{id}/hide|unhide|ban`

**Errors:** JSON: `{code, message, details}`. Идемпотентные операции по ключам (Idempotency-Key header) — для заявок/инвайтов.

---

## 10) События и интеграции (RMQ)
Exchange: `domain.events` (topic)
- `profiles.updated` {profile_id}
- `teams.updated` {team_id}
- `application.created/updated` {id, status}
- `invite.created/updated` {id, status}
Консьюмеры:
- `feed-refresher` — инвалидация кеша Recom.
- `mailer` — email уведомления.
- `audit-writer` — запись в admin_audit.

**Outbox:** таблица `outbox(id, event_type, payload, created_at, dispatched_at)` + воркер.

---

## 11) Нефункциональные требования
- **Надежность:** SLA MVP 99.5%; idempotency; транзакции и блокировки при join в команду (чтобы не переполнить >5).
- **Производительность:** `GET /feed` ≤ 150 мс p95 (с кешом), каталоги ≤ 300 мс p95.
- **Безопасность:** JWT (access+refresh), CORS белый список, rate limits (Redis), audit log, защита email enumerate.
- **Конфиденциальность:** контакты по умолчанию скрыты, открываются только после взаимного интереса или через админа.
- **DX:** OpenAPI JSON, Swagger UI.

---

## 12) UI (MVP странички)
- Onboarding Wizard (1–3 экрана): роль (ищу/собираю), направление, стек/теги, уровень, языки, таймзона, контакты.
- Home/For You (карточки: команд/кандидатов, CTA Apply/Invite).
- Browse (фильтры слева; список справа).
- Team Detail (описание, слоты, члены, управление заявками).
- Profile Detail/Edit.
- My Applications / My Invites.
- Admin: списки, фильтры, экспорт.

Компоненты (shadcn): Card, Badge (tags), Dialog (confirm), Sheet (filters), DataTable, Toast.

---

## 13) Алгоритм рекомендаций (деталь)
**Input:** профиль пользователя U, история заявок/инвайтов, активные команды C.
1. Отфильтровать C по направлению U и наличию свободных слотов.
2. Посчитать `score(C,U)` по правилам выше.
3. Нормализовать (min-max), скрыть пересечения с уже взаимодействовавшими командами.
4. Сохранить топ‑30 в Redis `feed:{user_id}` с JSON payload и причинной меткой (`reason`: "must_tags:python,django; timezone:+1; level:middle").
5. Инвалидация по событиям/таймеру.

**Режим для команды:** обратный матчинг кандидатов, то же правило по слоту/тегам.

---

## 14) Экспорт CSV
- `profiles.csv`: user_id, name, email(masked), direction, experience_level, langs, tech_tags(level), achievements.
- `teams.csv`: team_id, owner, direction, needs(slots/must/nice), status, members_count.
- `applications.csv`: team_id, user_id, status, created_at.
- **Защитить PII:** email частично маскируем по умолчанию, полный — только для `organizer|admin`.

---

## 15) Валидаторы и словари
- `direction`: {backend, frontend, mobile, mlops}
- `experience_level`: {junior, middle, senior}
- `languages_spoken`: {ru, en, ...}
- `tech_tags.kind`: {language, framework, tool}
- Ограничение: пользователь может быть **в одной активной команде**; подача заявок возможна в несколько.

---

## 16) Backend задачник (Cursor/LLM Checklist)
1. **Bootstrap:**
   - Инициализировать FastAPI проект по _существующему шаблону пользователя_: модули `auth, profiles, teams, matching, applications, invites, admin, notifications, common`.
   - Подключить Postgres/Redis/RabbitMQ через конфиг-слой; Alembic; настройки logging.
2. **Доменные модели + миграции:**
   - Создать таблицы, индексы (см. ERD), FTS (tsvector) и trigram расширения (`pg_trgm`).
   - Сгенерировать Alembic миграции.
3. **Репозитории/сервисы:**
   - Реализовать репозитории с типизированными методами; сервисы со слоями бизнес-логики; unit-тесты.
4. **Auth (magic-link):**
   - Эндпоинты request/verify; токены JWT (access/refresh); cookie httpOnly; CSRF для небезопасных методов.
5. **Profiles API:** CRUD своего профиля; поиск + фильтры + FTS; пагинация; DTO/сериализация.
6. **Teams + Needs:** CRUD команды; управление слотами; вычисление статус `full`.
7. **Applications/Invites:** все флоу; идемпотентность; контроль гонок (транзакции, `SELECT ... FOR UPDATE`).
8. **Matching service:**
   - Реализация скоринга (конфиг весов в БД или YAML); кэширование фида; инвалидация по RMQ.
   - Эндпоинт `/feed/for-you` (+ причины).
9. **Notifications:** in‑app + email sender (SMTP); воркер в фоне.
10. **Admin & Export:** фильтры, CSV (streaming response), аудит действий.
11. **Observability:** middleware кореляции `X-Request-ID`, метрики Prometheus, healthchecks.
12. **Docs:** OpenAPI c примерами.

**Definition of Done:** юнит‑тесты сервисов (>=80% coverage ядра), e2e happy-path на `applications/invites`, линтеры зелёные, CI прогон, Docker compose `up` без ошибок.

---

## 17) Frontend задачник (Cursor/LLM Checklist)
1. **Bootstrap:** Vite + React + TS; Tailwind; shadcn/ui; TanStack Query; envs.
2. **Роутинг:** `/onboarding`, `/home`, `/browse`, `/teams/:id`, `/profile`, `/me/applications`, `/me/invites`, `/admin`.
3. **Auth:** Magic-link экран (email), обработка verify, хранение токенов (cookie), Query `axios` instance c интерцепторами.
4. **Формы:** Zod схемы (совпадают с бэкендом), RHF, UI-компоненты (Card, Badge, Dialog, DataTable, Pagination, Sheet Filters).
5. **Каталоги:** списки/карточки, фильтры, сохранение поиска в URL, скелетоны загрузки.
6. **For You:** лента с причинами матчинга, CTA Apply/Invite inline.
7. **Team Detail:** табы: Overview, Needs, Members, Applications (approve/reject), Invites.
8. **Notifications/Toasts:** события успех/ошибка, пустые состояния.
9. **i18n:** подготовка (later).
10. **E2E (Playwright) happy-path:** онбординг → подача заявки → accept.

---

## 18) OpenAPI (фрагмент контракта)
```yaml
openapi: 3.0.3
info: {title: PROD Team Finder API, version: 0.1.0}
paths:
  /feed/for-you:
    get:
      summary: Personalized feed
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    entity_type: {type: string, enum: [team, profile]}
                    entity_id: {type: string}
                    score: {type: number}
                    reason: {type: string}
```

---

## 19) Пример SQL/миграций (фрагменты)
```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;

ALTER TABLE profiles ADD COLUMN search_vector tsvector;
CREATE INDEX idx_profiles_fts ON profiles USING GIN (search_vector);
CREATE INDEX idx_teams_name_trgm ON teams USING GIN (name gin_trgm_ops);
```

Триггер на поддержание `search_vector` по `bio` и связанным тегам (материализация в denorm колонку `tech_text`).

---

## 20) Redis ключи
- `feed:{user_id}` → JSON список рекомендаций (TTL 900s)
- `rate:apply:{user_id}:{team_id}` (TTL 60s)
- `idemp:{key}` (TTL 24h)

---

## 21) Email шаблоны
- Magic-link письмо.
- Invite received / Application received / Status changed.

---

## 22) Риски и меры
- Дубликаты и прокси-аккаунты → подтверждение email, поведенческие лимиты, модерация.
- Переполнение команды → транзакционные проверки, уникальный partial index на `accepted` по team_id (≤5).
- Срыв совместимости фронт/бэк → автогенерация API-клиента из OpenAPI.

---

## 23) План релиза (итерации)
1. Auth + Profiles + Admin Export (скелет).
2. Teams + Needs + Catalog.
3. Applications/Invites + Notifications.
4. Matching + For You кеш.
5. Полировка UI + метрики + пилот с организаторами.

---

## 24) Промпт для Cursor/LLM (вставить в задачу)
**System/Rules:**
- Используй существующую структуру моего репозитория (модули, слои, линтеры). Не меняй архитектурные решения без крайней необходимости.
- Стек: FastAPI async + SQLAlchemy 2 + Alembic; Redis; RabbitMQ; React/Vite + shadcn + Tailwind + TanStack Query.
- Следуй PRD ниже. Пиши чистые, типизированные интерфейсы. Покрой сервисный слой тестами.

**Задача:**
1) Сгенерировать каркас модульного монолита с модулями: `auth, profiles, teams, matching, applications, invites, admin, notifications, common`.
2) Описать доменные модели и миграции по ERD. Настроить FTS/trgm индексы.
3) Реализовать контракты API (раздел 9) и сервисную логику. Добавить идемпотентность для заявок/инвайтов.
4) Реализовать matching‑service по разделу 13 + кэш Redis + инвалидация RMQ.
5) На фронте — страницы и формы по разделу 17. Сделать happy‑path e2e.
6) Подготовить `docker-compose.yml` и seed‑скрипт с фейковыми данными (50 профилей, 15 команд).

**Готовность:**
- `docker compose up` поднимает стэк; Swagger доступен; seed данные загружены; можно пройти флоу: онбординг → заявка → accept → попадание в «For You» у остальных как «команда заполнилась/не заполнилась».

---

## 25) Best practices (в контексте твоего стека)
- FastAPI: отделяй DTO (Pydantic) от ORM-моделей; валидация на границе; paginate с `limit/offset` и `ETag`.
- SQLAlchemy: `async_sessionmaker`, `selectinload`, избегай N+1; транзакции через `async with session.begin()`; `FOR UPDATE` при изменении слотов.
- Alembic: «названные» миграции, нерушимость истории; `sqlmodel` не использовать.
- Кэш: только для read‑моделей; инвалидация по событиям; TTL разумный.
- RMQ: outbox паттерн; идемпотентные консьюмеры; DLQ.
- Frontend: коллбеки мутаций через Query invalidate; формы — схему держать в одном месте (zod+pydantic‑синхронизация); оптимистические апдейты только где безопасно.
- Безопасность: `httpOnly` cookies, `SameSite=Lax`, CORS whitelist; rate-limit write‑операций; логируй `actor_id`.

---

**Конец PRD**

