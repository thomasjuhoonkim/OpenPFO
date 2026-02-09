//  @ts-check

import { tanstackConfig } from "@tanstack/eslint-config";
import mantine from "eslint-config-mantine";
import simpleImportSort from "eslint-plugin-simple-import-sort";

export default [
  ...tanstackConfig,
  ...mantine,
  {
    plugins: {
      "simple-import-sort": simpleImportSort,
    },
    rules: {
      "simple-import-sort/imports": "error",
      "simple-import-sort/exports": "error",
    },
  },
  {
    rules: {
      "sort-imports": "off",
      "import/order": "off",
      "@typescript-eslint/array-type": "off",
      "import/consistent-type-specifier-style": "off",
    },
  },
  {
    languageOptions: {
      parserOptions: {
        tsconfigRootDir: process.cwd(),
        project: ["./tsconfig.json"],
      },
    },
  },
];
