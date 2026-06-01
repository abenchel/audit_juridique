"use client";

import { useState } from "react";

type Props = { projectCode: string; auditId: string };

export function ExportHtmlButton({ projectCode, auditId }: Props) {
  const [busy, setBusy] = useState(false);

  async function handleExport() {
    setBusy(true);
    try {
      const clone = document.documentElement.cloneNode(true) as HTMLElement;

      const head = clone.querySelector("head");
      const body = clone.querySelector("body");
      if (!head || !body) throw new Error("DOM invalide");

      const links = Array.from(
        head.querySelectorAll('link[rel="stylesheet"], link[as="style"]'),
      ) as HTMLLinkElement[];
      for (const link of links) {
        const href = link.href;
        if (!href) continue;
        try {
          const res = await fetch(href, { credentials: "include" });
          if (!res.ok) continue;
          const css = await res.text();
          const style = document.createElement("style");
          style.setAttribute("data-inlined-from", href);
          style.textContent = css;
          link.replaceWith(style);
        } catch {
          // garder le link distant en fallback (couleurs peuvent casser hors-ligne)
        }
      }

      head.querySelectorAll("script").forEach((s) => s.remove());
      body.querySelectorAll("script").forEach((s) => s.remove());
      body.querySelectorAll("next-route-announcer").forEach((n) => n.remove());
      body.querySelectorAll('[data-nextjs-toast]').forEach((n) => n.remove());

      const wrapper = document.querySelector("article.bg-bg");
      if (wrapper) {
        body.innerHTML = "";
        const wrapped = document.createElement("div");
        wrapped.className = "min-h-screen bg-bg";
        wrapped.appendChild(wrapper.cloneNode(true));
        body.appendChild(wrapped);
      }

      const banner = document.createElement("div");
      banner.style.cssText =
        "background:#f0fdf4;border-bottom:1px solid #00B685;padding:8px 16px;font:12px ui-sans-serif,system-ui;color:#0f172a;text-align:center;";
      banner.textContent = `Export statique — Audit ${projectCode} ${auditId.slice(0, 8)} — ${new Date().toLocaleString("fr-FR")}`;
      body.insertBefore(banner, body.firstChild);

      const html = "<!DOCTYPE html>\n" + clone.outerHTML;
      const blob = new Blob([html], { type: "text/html;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      const ts = new Date().toISOString().slice(0, 16).replace(/[-:T]/g, "");
      a.download = `audit_${projectCode}_${auditId.slice(0, 8)}_${ts}.html`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Export HTML failed", err);
      alert("Échec export HTML : " + (err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <button
      type="button"
      onClick={handleExport}
      disabled={busy}
      className="inline-flex items-center gap-2 rounded-lg border border-line bg-white px-3 py-2 text-sm font-medium text-ink shadow-sm hover:bg-bg disabled:opacity-50"
      title="Télécharger un fichier HTML autonome (colors + tables intacts, partageable hors-ligne)"
    >
      {busy ? "Préparation…" : "Télécharger HTML"}
    </button>
  );
}
