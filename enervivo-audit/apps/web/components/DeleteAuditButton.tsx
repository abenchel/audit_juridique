"use client";

import { useTransition } from "react";

interface Props {
  auditId: string;
  onDelete: (auditId: string) => Promise<void>;
}

export function DeleteAuditButton({ auditId, onDelete }: Props) {
  const [isPending, startTransition] = useTransition();

  function handleClick() {
    if (!confirm("Supprimer cet audit ? Cette action est irréversible.")) return;
    startTransition(() => { void onDelete(auditId); });
  }

  return (
    <button
      onClick={handleClick}
      disabled={isPending}
      className="text-red text-xs font-semibold hover:underline disabled:opacity-40"
    >
      {isPending ? "…" : "Supprimer"}
    </button>
  );
}
