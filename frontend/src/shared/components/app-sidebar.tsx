import { IconInnerShadowTop } from "@tabler/icons-react"
import { Link, NavLink } from "react-router-dom"

import { useAuth } from "@/app/providers/auth/useAuth"
import { NavUser } from "@/shared/components/nav-user"
import { cn } from "@/shared/lib/utils"

export function AppSidebar() {
  const auth = useAuth()
  const hasUser = Boolean(auth?.user)

  const fallbackUser = {
    name: auth?.user?.email ?? "TeamUp Member",
    email: auth?.user?.email ?? "member@teamup.app",
    avatar: "/avatars/shadcn.jpg",
  }

  return (
    <header className="supports-[backdrop-filter]:bg-background/80 border-b bg-background/95 px-4 py-3 shadow-sm backdrop-blur">
      <div className="mx-auto flex w-full max-w-6xl items-center gap-3">
        <Link to="/fyp" className="flex items-center gap-2 text-lg font-semibold text-foreground">
          <span className="rounded-xl bg-primary/10 p-2 text-primary">
            <IconInnerShadowTop className="size-5" />
          </span>
          <span>TeamUp</span>
        </Link>
        <nav className="ml-6 flex items-center gap-2 rounded-full bg-muted px-1 py-1 text-sm font-medium">
          <NavLink
            to="/fyp"
            className={({ isActive }) =>
              cn(
                "rounded-full px-4 py-1.5 transition",
                isActive
                  ? "bg-background text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              )
            }
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
              className="inline-flex items-center rounded-xl bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow transition hover:bg-primary/90"
            >
              Войти
            </Link>
          )}
        </div>
      </div>
    </header>
  )
}
