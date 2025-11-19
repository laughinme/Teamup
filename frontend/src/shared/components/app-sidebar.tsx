import { IconInnerShadowTop } from "@tabler/icons-react"
import { Link, NavLink, useLocation } from "react-router-dom"

import { useAuth } from "@/app/providers/auth/useAuth"
import { NavUser } from "@/shared/components/nav-user"
import { cn } from "@/shared/lib/utils"

export function AppSidebar() {
  const auth = useAuth()
  const hasUser = Boolean(auth?.user)
  const location = useLocation()
  const isProfileRoute = location.pathname === "/user-profile" || location.pathname === "/account"

  const resolvedAuth = auth?.user as { name?: unknown; username?: unknown; email?: unknown } | null
  const authEmail =
    resolvedAuth && typeof resolvedAuth.email === "string" && resolvedAuth.email.trim().length
      ? resolvedAuth.email.trim()
      : null
  const authName =
    resolvedAuth && typeof resolvedAuth.name === "string" && resolvedAuth.name.trim().length
      ? resolvedAuth.name.trim()
      : resolvedAuth && typeof resolvedAuth.username === "string" && resolvedAuth.username.trim().length
        ? resolvedAuth.username.trim()
        : null
  const fallbackUser = {
    name: authName ?? authEmail ?? "TeamUp Member",
    email: authEmail ?? "member@teamup.app",
    avatar: "/avatars/shadcn.jpg",
  }

  const headerClass = cn(
    "supports-[backdrop-filter]:bg-background/80 border-b bg-background/95 px-4 py-3 shadow-sm backdrop-blur",
    isProfileRoute && "border-[#02281f] bg-[#02281f] text-white shadow-none backdrop-blur-0"
  )

  const brandTextClass = cn(
    "flex items-center gap-2 text-lg font-semibold",
    isProfileRoute ? "text-white" : "text-foreground"
  )

  const brandIconClass = cn(
    "rounded-xl p-2",
    isProfileRoute ? "bg-white/10 text-white" : "bg-primary/10 text-primary"
  )

  const navClass = cn(
    "ml-6 flex items-center rounded-full px-1 py-1 text-sm font-medium",
    isProfileRoute ? "bg-[#0d352c]/80 text-white" : "bg-muted text-muted-foreground"
  )

  const navLinkClass = (isActive: boolean) =>
    isProfileRoute
      ? cn(
          "rounded-full px-4 py-1.5 transition",
          isActive ? "bg-[#0f3b31] text-white" : "text-white/60 hover:text-white"
        )
      : cn(
          "rounded-full px-4 py-1.5 transition",
          isActive
            ? "bg-background text-foreground shadow-sm"
            : "text-muted-foreground hover:text-foreground"
        )

  const authButtonClass = cn(
    "inline-flex items-center rounded-xl px-4 py-2 text-sm font-medium shadow transition",
    isProfileRoute
      ? "bg-white/10 text-white hover:bg-white/20"
      : "bg-primary text-primary-foreground hover:bg-primary/90"
  )

  return (
    <header className={headerClass}>
      <div className="mx-auto flex w-full max-w-6xl items-center gap-3">
        <Link to="/fyp" className={brandTextClass}>
          <span className={brandIconClass}>
            <IconInnerShadowTop className="size-5" />
          </span>
          <span>TeamUp</span>
        </Link>
        <nav className={navClass}>
          <NavLink
            to="/fyp"
            className={({ isActive }) => navLinkClass(Boolean(isActive))}
          >
            FYP
          </NavLink>
        </nav>
        <div className="ml-auto flex items-center">
          {hasUser ? (
            <NavUser user={fallbackUser} />
          ) : (
            <Link
              to="/auth"
              className={authButtonClass}
            >
              Войти
            </Link>
          )}
        </div>
      </div>
    </header>
  )
}
