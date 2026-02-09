import { createTheme, type MantineColorsTuple } from "@mantine/core";

const myColor: MantineColorsTuple = [
  "#fffae0",
  "#fff4ca",
  "#ffe899",
  "#ffdb63",
  "#ffce2f",
  "#ffc918",
  "#ffc502",
  "#e3ad00",
  "#ca9a00",
  "#af8400",
];

export const theme = createTheme({
  colors: {
    myColor,
  },
  primaryColor: "myColor",
  fontFamily: "Inter",
});
