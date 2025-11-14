import { AppSidebar } from "@/shared/components/app-sidebar"
import { SidebarProvider } from "@/shared/components/ui/sidebar"

export default function FypPage() {
  return (
    <SidebarProvider className="flex min-h-svh flex-col bg-muted/10">
      <AppSidebar />
      <main className="flex flex-1 items-center justify-center px-4 py-10">
        <h1 className="text-5xl font-semibold tracking-tight text-foreground">
          FYP
        </h1>
      </main>
    </SidebarProvider>
  )
}
