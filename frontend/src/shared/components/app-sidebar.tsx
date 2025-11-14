import { IconInnerShadowTop } from "@tabler/icons-react"
import { Link, NavLink } from "react-router-dom"

import { NavUser } from "@/shared/components/nav-user"
import { cn } from "@/shared/lib/utils"

const data = {
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  },
}

export function AppSidebar() {
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
          <NavUser user={data.user} />
        </div>
      </div>
    </header>
  )
}
