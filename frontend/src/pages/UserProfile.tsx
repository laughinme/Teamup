import { useMemo, type ReactNode } from "react";
import { AppSidebar } from "@/shared/components/app-sidebar";
import { SidebarProvider } from "@/shared/components/ui/sidebar";
import { useProfileData } from "@/entities/profile/model/useProfile";
import type { ProfileResponse, TechStack } from "@/entities/profile/model/types";
import { useAuth } from "@/app/providers/auth/useAuth";

type RawAuthUser = {
  email?: unknown;
  username?: unknown;
  first_name?: unknown;
  last_name?: unknown;
};

const PANEL_CLASS =
  "rounded-[30px] border border-[#1c5a4b] bg-[#0f3b31] p-6 text-[#f5f8e5]";
const PANEL_SUBTLE_TEXT = "text-[#cbe2c5]";
const PANEL_HEADING_TEXT = "text-[#f1f9e1]";

const DIRECTION_LABELS: Record<string, string> = {
  backend: "Backend-разработчик",
  frontend: "Frontend-разработчик",
  mobile: "Mobile-разработчик",
  mlops: "ML/DevOps инженер"
};

const EXPERIENCE_LABELS: Record<string, string> = {
  junior: "Junior",
  middle: "Middle",
  senior: "Senior"
};

const EXPERIENCE_SCORE: Record<string, number> = {
  junior: 2,
  middle: 4,
  senior: 5
};

const VISIBILITY_META: Record<
  string,
  {
    label: string;
    dotClass: string;
  }
> = {
  public: { label: "Публичный", dotClass: "bg-[#5ee6a6]" },
  private: { label: "Приватный", dotClass: "bg-[#fdd860]" }
};

const TECH_KIND_LABELS: Record<string, string> = {
  language: "LANGUAGE",
  framework: "FRAMEWORK",
  tool: "TOOL"
};

const TECH_LEVEL_LABELS: Record<number, string> = {
  1: "Новичок",
  2: "Базовый",
  3: "Уверенный",
  4: "Продвинутый",
  5: "Эксперт"
};

const formatTimezone = (timezone?: string | null): string => {
  if (!timezone) {
    return "Не указан";
  }

  try {
    const formatter = new Intl.DateTimeFormat("ru-RU", {
      timeZone: timezone,
      timeZoneName: "shortOffset"
    });
    const parts = formatter.formatToParts(new Date());
    const offset = parts.find((part) => part.type === "timeZoneName")?.value ?? "";
    if (offset) {
      const normalizedOffset = offset.replace("GMT", "UTC");
      return `${timezone} (${normalizedOffset})`;
    }
  } catch {
    // Some browsers might not support `shortOffset`; fall back to the raw timezone identifier.
  }

  return timezone;
};

const resolveDisplayName = (user?: RawAuthUser | null): string => {
  if (!user) {
    return "TeamUp Member";
  }
  const firstName =
    typeof user.first_name === "string" && user.first_name.trim().length ? user.first_name.trim() : "";
  const lastName =
    typeof user.last_name === "string" && user.last_name.trim().length ? user.last_name.trim() : "";
  if (firstName || lastName) {
    return [firstName, lastName].filter(Boolean).join(" ").trim();
  }
  const username =
    typeof user.username === "string" && user.username.trim().length ? user.username.trim() : "";
  if (username) {
    return username;
  }
  const email =
    typeof user.email === "string" && user.email.trim().length ? user.email.trim() : undefined;
  if (email) {
    return email.split("@")[0] ?? email;
  }
  return "TeamUp Member";
};

const resolveEmail = (user?: RawAuthUser | null): string | null => {
  if (!user) {
    return null;
  }

  return typeof user.email === "string" && user.email.trim().length ? user.email.trim() : null;
};

const getInitials = (name: string): string => {
  const initials = name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((chunk) => chunk.charAt(0).toUpperCase())
    .join("");
  if (initials.length) {
    return initials;
  }
  return "??";
};

const ProfileHero = ({
  profile,
  displayName,
  email
}: {
  profile: ProfileResponse;
  displayName: string;
  email: string | null;
}) => {
  const directionLabel = DIRECTION_LABELS[profile.direction] ?? profile.direction;
  const experienceLabel = EXPERIENCE_LABELS[profile.experienceLevel] ?? profile.experienceLevel;
  const experienceBadge = experienceLabel ? experienceLabel.toUpperCase() : "—";
  const visibilityMeta = VISIBILITY_META[profile.visibility] ?? {
    label: profile.visibility,
    dotClass: "bg-[#dcebd5]"
  };

  return (
    <section className={`${PANEL_CLASS} flex flex-col items-center text-center lg:w-[340px]`}>
      <div className="flex h-32 w-32 items-center justify-center rounded-full border border-[#1f5949] bg-[#0b2a22] text-3xl font-semibold tracking-[0.35em] text-[#f7fde9]">
        {getInitials(displayName)}
      </div>
      <div className="mt-5 text-2xl font-semibold text-white">{displayName}</div>
      <div className="mt-2 flex items-center gap-2 rounded-full border border-[#1f4c3e] bg-[#0b2b23] px-5 py-1 text-sm text-[#cbead3]">
        <span className="h-2 w-2 rounded-full bg-[#5ee6a6]" />
        {directionLabel}
      </div>
      <p className={`mt-4 text-xs uppercase tracking-[0.5em] ${PANEL_SUBTLE_TEXT}`}>Уровень: {experienceBadge}</p>

      <div className="mt-6 w-full space-y-4 text-left">
        <InfoPill
          label="Часовой пояс"
          value={formatTimezone(profile.timezone)}
        />
        <InfoPill
          label="Видимость профиля"
          value={
            <span className="flex items-center gap-2 text-[#fdf9d7]">
              <span className={`h-2.5 w-2.5 rounded-full ${visibilityMeta.dotClass}`} />
              {visibilityMeta.label}
            </span>
          }
        />
      </div>

      <a
        href={email ? `mailto:${email}` : undefined}
        aria-disabled={!email}
        className={`mt-6 inline-flex w-full items-center justify-center rounded-full px-6 py-3 text-base font-semibold tracking-wide transition ${
          email
            ? "bg-[#fad437] text-[#1b1d0f] hover:bg-[#ffe15f]"
            : "cursor-not-allowed bg-[#f4e7a4]/40 text-[#46442c]/60"
        }`}
      >
        Связаться
      </a>
    </section>
  );
};

const InfoPill = ({ label, value }: { label: string; value: ReactNode }) => (
  <div className="flex flex-col gap-2 rounded-3xl border border-[#1f5344] bg-[#0b2a23] px-5 py-3 text-sm text-white/90 sm:flex-row sm:items-center sm:justify-between sm:text-base">
    <span className="text-xs uppercase tracking-[0.4em] text-[#7dc0a0]">{label}</span>
    <span className="text-white">{value}</span>
  </div>
);

const AboutCard = ({ profile }: { profile: ProfileResponse }) => (
  <section className={`${PANEL_CLASS} flex-1`}>
    <SectionLabel
      title="О себе"
      description="Краткое описание опыта и интересов"
    />
    <p className="mt-4 text-base leading-relaxed text-[#f0f6e4]">
      {profile.bio?.trim()?.length ? profile.bio : "Пока ещё нет описания. Расскажите о себе, чтобы ваши будущие тиммейты узнали вас лучше."}
    </p>
  </section>
);

const ExperienceCard = ({ profile }: { profile: ProfileResponse }) => {
  const score = EXPERIENCE_SCORE[profile.experienceLevel] ?? 1;
  const label = EXPERIENCE_LABELS[profile.experienceLevel] ?? profile.experienceLevel;
  const percent = Math.min(Math.max((score / 5) * 100, 8), 100);

  return (
    <section className={PANEL_CLASS}>
      <SectionLabel title="Опыт" />
      <p className="text-sm text-[#c5dbce]">
        Уровень: <span className="font-semibold text-white">{label ?? "—"}</span>
      </p>
      <div className="mt-4 h-2 rounded-full bg-[#16392f]">
        <div
          className="h-full rounded-full bg-[#f8d94f]"
          style={{ width: `${percent}%` }}
        />
      </div>
      <p className="mt-3 text-xs text-[#7da491]">
        Индикатор условный — цифры зависят от данных backend.
      </p>
    </section>
  );
};

const AchievementsCard = ({ profile }: { profile: ProfileResponse }) => (
  <section className={PANEL_CLASS}>
    <SectionLabel title="Достижения" />
    <p className="mt-4 text-base leading-relaxed text-[#f0f6e4]">
      {profile.achievements?.trim()?.length
        ? profile.achievements
        : "Расскажите о курируемых проектах, хакатонах или заметных результатах — это поможет быстрее найти команду мечты."}
    </p>
  </section>
);

const TechStackCard = ({ techStack }: { techStack: TechStack[] }) => (
  <section className={PANEL_CLASS}>
    <SectionLabel
      title="Технологический стек"
      description="Основные языки, фреймворки и инструменты разработчика"
    />
    <div className="mt-6 space-y-4">
      {techStack.length ? (
        techStack.map((item) => (
          <TechRow tech={item} key={`${item.tag.id}-${item.tag.slug}`} />
        ))
      ) : (
        <div className="rounded-2xl border border-[#1f5344] bg-[#0b2a23] p-4 text-sm text-white/70">
          Вы ещё не добавили технологии. Заполните стек, чтобы матчинг был точнее.
        </div>
      )}
    </div>
  </section>
);

const TechRow = ({ tech }: { tech: TechStack }) => {
  const kindLabel = TECH_KIND_LABELS[tech.tag.kind] ?? tech.tag.kind.toUpperCase();
  const levelPercent = Math.min(Math.max((tech.level / 5) * 100, 4), 100);
  const levelLabel = TECH_LEVEL_LABELS[tech.level] ?? `Уровень ${tech.level}`;

  return (
    <div className="rounded-2xl border border-[#1f5344] bg-[#0b3429] p-4">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-lg font-semibold text-white">{tech.tag.name}</p>
          <p className="text-xs uppercase tracking-[0.35em] text-[#7ec0a4]">{kindLabel}</p>
        </div>
        <div className="text-right text-sm font-medium text-[#f9d64f]">
          {levelLabel}
          <span className="ml-1 text-xs text-[#d4e7c8]">({tech.level}/5)</span>
        </div>
      </div>
      <div className="mt-3 h-2 rounded-full bg-[#153229]">
        <div
          className="h-full rounded-full bg-[#f9d64f]"
          style={{ width: `${levelPercent}%` }}
        />
      </div>
    </div>
  );
};

const SectionLabel = ({ title, description }: { title: string; description?: string }) => (
  <header>
    <p className="text-[0.78rem] uppercase tracking-[0.5em] text-[#cfe5d0]">{title}</p>
    {description ? <p className="mt-1 text-sm text-[#8fb8a1]">{description}</p> : null}
  </header>
);

const ProfileSkeleton = () => (
  <div className="flex w-full flex-col gap-6 lg:flex-row lg:gap-8">
    <div className={`${PANEL_CLASS} animate-pulse lg:w-[340px]`}>
      <div className="mx-auto h-32 w-32 rounded-full bg-[#122f27]" />
      <div className="mt-5 h-5 rounded bg-[#122f27]" />
      <div className="mt-4 h-3 rounded bg-[#122f27]" />
      <div className="mt-6 space-y-3">
        <div className="h-12 rounded-3xl bg-[#122f27]" />
        <div className="h-12 rounded-3xl bg-[#122f27]" />
      </div>
      <div className="mt-6 h-12 rounded-full bg-[#122f27]" />
    </div>
    <div className="flex flex-1 flex-col gap-6">
      <div className={`${PANEL_CLASS} h-48 animate-pulse`} />
      <div className="grid gap-6 md:grid-cols-2">
        <div className={`${PANEL_CLASS} h-48 animate-pulse`} />
        <div className={`${PANEL_CLASS} h-48 animate-pulse`} />
      </div>
      <div className={`${PANEL_CLASS} h-72 animate-pulse`} />
    </div>
  </div>
);

const ProfileErrorState = ({ onRetry }: { onRetry: () => void }) => (
  <div className={`${PANEL_CLASS} flex flex-col items-center justify-center gap-4 text-center`}>
    <p className="text-xl font-semibold text-white">Не удалось загрузить профиль</p>
    <p className="text-sm text-[#b7d6c7]">Проверьте соединение с сервером и попробуйте снова.</p>
    <button
      type="button"
      onClick={onRetry}
      className="rounded-full border border-[#1f5344] px-6 py-2 text-sm font-semibold text-white transition hover:bg-[#134536]"
    >
      Обновить
    </button>
  </div>
);

const ProfileEmptyState = () => (
  <div className={`${PANEL_CLASS} flex flex-col gap-2 text-center`}>
    <p className="text-lg font-semibold text-white">Профиль пока пуст</p>
    <p className="text-sm text-[#cfe5d0]">
      Дополните информацию о себе и добавьте технологии, чтобы команда могла найти вас в TeamUp.
    </p>
  </div>
);

const ProfileContent = ({
  profile,
  displayName,
  email
}: {
  profile: ProfileResponse;
  displayName: string;
  email: string | null;
}) => (
  <div className="flex w-full flex-col gap-6 lg:flex-row lg:gap-8">
    <ProfileHero profile={profile} displayName={displayName} email={email} />
    <div className="flex flex-1 flex-col gap-6">
      <AboutCard profile={profile} />
      <div className="grid gap-6 md:grid-cols-2">
        <ExperienceCard profile={profile} />
        <AchievementsCard profile={profile} />
      </div>
      <TechStackCard techStack={profile.techStack} />
    </div>
  </div>
);

const PAGE_BACKGROUND = "bg-[#023528]";

const UserProfilePage = () => {
  const { data, isLoading, isError, refetch } = useProfileData();
  const auth = useAuth();
  const rawUser = auth?.user as RawAuthUser | null;

  const displayName = useMemo(() => resolveDisplayName(rawUser), [rawUser]);
  const email = useMemo(() => resolveEmail(rawUser), [rawUser]);

let content: ReactNode = null;

  if (isLoading) {
    content = <ProfileSkeleton />;
  } else if (isError) {
    content = <ProfileErrorState onRetry={refetch} />;
  } else if (data) {
    content = <ProfileContent profile={data} displayName={displayName} email={email} />;
  } else {
    content = <ProfileEmptyState />;
  }

  return (
    <SidebarProvider className={`flex min-h-svh flex-col ${PAGE_BACKGROUND}`}>
      <AppSidebar />
      <main className="flex flex-1 justify-center px-4 py-8 text-[#f5f8e5]">
        <div className="w-full max-w-6xl">{content}</div>
      </main>
    </SidebarProvider>
  );
};

export default UserProfilePage;
