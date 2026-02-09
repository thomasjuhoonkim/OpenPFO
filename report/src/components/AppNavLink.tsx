import { Link } from '@tanstack/react-router'
import { NavLink } from '@mantine/core'

export function AppNavLink(props: any) {
  return <NavLink component={Link} {...props} />
}
