import { AppSidebar } from "@/shared/components/app-sidebar"
import { ChartAreaInteractive } from "@/shared/components/chart-area-interactive"
import { SectionCards } from "@/shared/components/section-cards"
import { SidebarProvider } from "@/shared/components/ui/sidebar"

export default function Page() {
  return (
    <SidebarProvider className="flex-col bg-muted/10">
      <AppSidebar />
      <main className="flex flex-1 flex-col">
        <div className="@container/main mx-auto flex w-full max-w-6xl flex-1 flex-col gap-4 px-4 py-4 md:gap-6 md:px-6 md:py-6">
          <SectionCards />
          <ChartAreaInteractive />
        </div>
      </main>
    </SidebarProvider>
  )
}
