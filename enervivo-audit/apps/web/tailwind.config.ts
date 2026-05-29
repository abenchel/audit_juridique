import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Charte EnerVivo officielle (cf. rapport_audit_DDENIS_v6.html)
        bg: "var(--bg)",
        "bg-card": "var(--bg-card)",
        "bg-soft": "var(--bg-soft)",
        ink: {
          DEFAULT: "var(--ink)",
          mid: "var(--ink-mid)",
          soft: "var(--ink-soft)",
        },
        line: "var(--line)",
        "line-strong": "var(--line-strong)",
        solar: {
          DEFAULT: "var(--solar)",
          deep: "var(--solar-deep)",
          soft: "var(--solar-soft)",
        },
        green: {
          DEFAULT: "var(--green)",
          soft: "var(--green-soft)",
        },
        amber: {
          DEFAULT: "var(--amber)",
          soft: "var(--amber-soft)",
        },
        red: {
          DEFAULT: "var(--red)",
          soft: "var(--red-soft)",
        },
        violet: {
          DEFAULT: "var(--violet)",
          soft: "var(--violet-soft)",
        },
      },
      fontFamily: {
        sans: ["var(--font-montserrat)", "system-ui", "sans-serif"],
        display: ["var(--font-baloo)", "cursive"],
        mono: ["var(--font-mono)", "monospace"],
      },
      borderRadius: {
        DEFAULT: "6px",
        lg: "12px",
      },
      boxShadow: {
        sm: "0 1px 2px rgba(28,120,98,.06)",
        md: "0 4px 16px rgba(28,120,98,.08)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
