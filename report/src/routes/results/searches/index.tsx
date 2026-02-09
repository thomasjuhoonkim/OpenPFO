import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/results/searches/')({
  component: RouteComponent,
})

function RouteComponent() {
  return <div>Hello "/results/searches/"!</div>
}
