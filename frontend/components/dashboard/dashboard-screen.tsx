"use client";

import { useMemo, useState } from "react";
import { HomeIcon, LibraryIcon, MoonIcon, PlayIcon, PlusIcon, SearchIcon, SparkleIcon, SunIcon } from "@/components/icons";
import { demoResources, playlists } from "@/lib/resources";

const navigation = [
  { label: "Overview", icon: HomeIcon },
  { label: "Library", icon: LibraryIcon },
];

export function DashboardScreen() {
  const [query, setQuery] = useState("");
  const [selectedPlaylist, setSelectedPlaylist] = useState("All resources");
  const [isDark, setIsDark] = useState(true);

  const resources = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();

    return demoResources.filter((resource) => {
      const matchesPlaylist = selectedPlaylist === "All resources" || resource.playlist === selectedPlaylist;
      const searchable = [resource.title, resource.creator, resource.playlist, ...resource.tags].join(" ").toLowerCase();
      return matchesPlaylist && searchable.includes(normalizedQuery);
    });
  }, [query, selectedPlaylist]);

  return (
    <div className={isDark ? "min-h-screen bg-[#09090b] text-slate-100" : "min-h-screen bg-slate-50 text-slate-950"}>
      <div className="mx-auto flex min-h-screen max-w-[1600px]">
        <aside className={isDark ? "hidden w-64 shrink-0 border-r border-white/7 bg-[#0c0c0f] px-4 py-6 lg:block" : "hidden w-64 shrink-0 border-r border-slate-200 bg-white px-4 py-6 lg:block"}>
          <Brand />
          <nav className="mt-10 space-y-1" aria-label="Main navigation">
            {navigation.map((item, index) => {
              const Icon = item.icon;
              return <button className={index === 0 ? "flex w-full items-center gap-3 rounded-xl bg-violet-500/15 px-3 py-2.5 text-sm font-medium text-violet-400" : "flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-slate-400 transition hover:bg-white/5 hover:text-slate-100"} key={item.label}><Icon className="size-4" />{item.label}</button>;
            })}
          </nav>
          <div className="mt-10">
            <p className="px-3 text-[11px] font-semibold tracking-[0.14em] text-slate-500 uppercase">Your playlists</p>
            <div className="mt-3 space-y-1">
              <PlaylistButton active={selectedPlaylist === "All resources"} label="All resources" count={70} onClick={() => setSelectedPlaylist("All resources")} />
              {playlists.map((playlist) => <PlaylistButton active={selectedPlaylist === playlist.name} key={playlist.name} label={playlist.name} count={playlist.count} onClick={() => setSelectedPlaylist(playlist.name)} />)}
            </div>
          </div>
          <button className="mt-8 flex w-full items-center gap-2 rounded-xl border border-dashed border-white/12 px-3 py-2.5 text-sm text-slate-400 transition hover:border-violet-400/50 hover:text-violet-300"><PlusIcon className="size-4" />Connect YouTube</button>
          <div className="mt-auto pt-10"><div className="rounded-2xl border border-violet-400/15 bg-violet-500/8 p-4"><SparkleIcon className="size-5 text-violet-400" /><p className="mt-3 text-sm font-medium">Your knowledge, connected.</p><p className="mt-1 text-xs leading-5 text-slate-400">Import your playlists to make every tutorial findable.</p></div></div>
        </aside>

        <main className="min-w-0 flex-1 px-5 py-5 sm:px-8 sm:py-7 lg:px-10">
          <header className="flex items-center justify-between gap-3">
            <div className="flex items-center gap-3 lg:hidden"><Brand compact /></div>
            <div className="hidden sm:block"><p className="text-sm text-slate-500">Thursday, July 16</p><h1 className="mt-1 text-2xl font-semibold tracking-tight">Good afternoon, Alex.</h1></div>
            <div className="flex items-center gap-2"><button onClick={() => setIsDark((value) => !value)} className={isDark ? "grid size-10 place-items-center rounded-xl text-slate-400 transition hover:bg-white/6 hover:text-white" : "grid size-10 place-items-center rounded-xl text-slate-500 transition hover:bg-slate-100 hover:text-slate-950"} aria-label="Toggle colour theme">{isDark ? <SunIcon className="size-4" /> : <MoonIcon className="size-4" />}</button><button className="grid size-9 place-items-center rounded-full bg-gradient-to-br from-violet-400 to-fuchsia-500 text-xs font-bold text-white">AK</button></div>
          </header>

          <section className="mt-8 sm:mt-10">
            <div className="sm:hidden"><p className="text-sm text-slate-500">Thursday, July 16</p><h1 className="mt-1 text-2xl font-semibold tracking-tight">Good afternoon, Alex.</h1></div>
            <div className="mt-6 grid gap-3 sm:grid-cols-3"><Stat label="Saved resources" value="70" detail="Across 4 playlists" /><Stat label="Recently imported" value="12" detail="In the last 7 days" /><Stat label="Learning streak" value="8 days" detail="Keep it going" accent /></div>
          </section>

          <section className="mt-9">
            <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end"><div><p className="text-sm font-medium text-violet-400">Your library</p><h2 className="mt-1 text-xl font-semibold tracking-tight">Find what you were learning.</h2></div><button className="inline-flex items-center justify-center gap-2 rounded-xl bg-violet-500 px-4 py-2.5 text-sm font-medium text-white shadow-lg shadow-violet-600/20 transition hover:bg-violet-400"><PlusIcon className="size-4" />Import playlists</button></div>
            <div className={isDark ? "mt-5 flex items-center gap-3 rounded-2xl border border-white/8 bg-white/[0.035] px-4 shadow-sm" : "mt-5 flex items-center gap-3 rounded-2xl border border-slate-200 bg-white px-4 shadow-sm"}><SearchIcon className="size-5 shrink-0 text-slate-500" /><input value={query} onChange={(event) => setQuery(event.target.value)} className="h-14 w-full bg-transparent text-sm outline-none placeholder:text-slate-500" placeholder="Search videos, topics, or playlists..." aria-label="Search your resources" /><kbd className="hidden rounded border border-white/10 px-1.5 py-0.5 text-xs text-slate-500 sm:block">⌘ K</kbd></div>
          </section>

          <section className="mt-8"><div className="flex items-center justify-between"><h2 className="text-base font-semibold">Recently saved</h2><p className="text-sm text-slate-500">{resources.length} results</p></div>{resources.length ? <div className="mt-4 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">{resources.map((resource) => <ResourceCard key={resource.id} resource={resource} light={!isDark} />)}</div> : <div className={isDark ? "mt-4 rounded-2xl border border-dashed border-white/12 py-16 text-center" : "mt-4 rounded-2xl border border-dashed border-slate-300 py-16 text-center"}><SearchIcon className="mx-auto size-6 text-slate-500" /><p className="mt-3 font-medium">No resources found</p><p className="mt-1 text-sm text-slate-500">Try another topic, creator, or playlist.</p></div>}</section>
        </main>
      </div>
    </div>
  );
}

function Brand({ compact = false }: { compact?: boolean }) {
  return <div className="flex items-center gap-2.5"><span className="grid size-8 place-items-center rounded-lg bg-gradient-to-br from-violet-400 to-fuchsia-600 shadow-lg shadow-violet-500/25"><SparkleIcon className="size-4 text-white" /></span>{!compact && <span className="text-base font-semibold tracking-tight">Synapse Keepr</span>}</div>;
}

function PlaylistButton({ active, label, count, onClick }: { active: boolean; label: string; count: number; onClick: () => void }) {
  return <button onClick={onClick} className={active ? "flex w-full items-center justify-between rounded-xl bg-white/7 px-3 py-2 text-left text-sm text-slate-100" : "flex w-full items-center justify-between rounded-xl px-3 py-2 text-left text-sm text-slate-400 transition hover:bg-white/5 hover:text-slate-100"}><span className="truncate">{label}</span><span className="ml-2 text-xs text-slate-500">{count}</span></button>;
}

function Stat({ label, value, detail, accent = false }: { label: string; value: string; detail: string; accent?: boolean }) {
  return <article className={accent ? "rounded-2xl border border-violet-400/20 bg-gradient-to-br from-violet-500/14 to-fuchsia-500/5 p-4" : "rounded-2xl border border-white/8 bg-white/[0.035] p-4"}><p className="text-sm text-slate-400">{label}</p><p className="mt-3 text-2xl font-semibold tracking-tight">{value}</p><p className="mt-1 text-xs text-slate-500">{detail}</p></article>;
}

function ResourceCard({ resource, light }: { resource: (typeof demoResources)[number]; light: boolean }) {
  return <article className={light ? "group overflow-hidden rounded-2xl border border-slate-200 bg-white p-2 shadow-sm transition hover:-translate-y-0.5 hover:shadow-lg" : "group overflow-hidden rounded-2xl border border-white/8 bg-white/[0.035] p-2 transition hover:-translate-y-0.5 hover:border-white/15 hover:bg-white/[0.055]"}><div className={`relative aspect-video overflow-hidden rounded-xl bg-gradient-to-br ${resource.thumbnailClass}`}><div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_20%,rgba(255,255,255,.22),transparent_32%)]" /><span className="absolute bottom-2 right-2 rounded bg-black/75 px-1.5 py-0.5 text-[11px] font-medium text-white">{resource.duration}</span><span className="absolute left-1/2 top-1/2 grid size-11 -translate-x-1/2 -translate-y-1/2 place-items-center rounded-full bg-white/90 text-slate-950 opacity-0 shadow-lg transition group-hover:opacity-100"><PlayIcon className="ml-0.5 size-4" /></span></div><div className="px-1 pb-1 pt-3"><p className="line-clamp-2 min-h-10 text-sm font-medium leading-5">{resource.title}</p><p className="mt-1 text-xs text-slate-500">{resource.creator}</p><div className="mt-3 flex items-center justify-between gap-2"><span className="truncate text-xs text-violet-400">{resource.playlist}</span><span className="shrink-0 text-xs text-slate-500">{resource.savedAt}</span></div></div></article>;
}
