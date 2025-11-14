import { IconInnerShadowTop } from "@tabler/icons-react"

import { NavUser } from "@/shared/components/nav-user"

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
        <div className="flex items-center gap-2 text-lg font-semibold text-foreground">
          <span className="rounded-xl bg-primary/10 p-2 text-primary">
            <IconInnerShadowTop className="size-5" />
          </span>
          <span>TeamUp</span>
        </div>
        <div className="ml-auto flex items-center">
          <NavUser user={data.user} />
        </div>
      </div>
    </header>
  )
}
