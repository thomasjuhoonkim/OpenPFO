import { NavLink } from "@mantine/core";
import { Link } from "@tanstack/react-router";

export function AppNavLink(props: any) {
  return <NavLink component={Link} {...props} />;
}
