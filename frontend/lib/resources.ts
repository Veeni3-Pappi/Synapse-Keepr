export type Resource = {
  id: string;
  title: string;
  creator: string;
  playlist: string;
  duration: string;
  savedAt: string;
  thumbnailClass: string;
  tags: string[];
};

export const demoResources: Resource[] = [
  {
    id: "docker-networking",
    title: "Docker Networking Is Actually Simple",
    creator: "TechWorld with Nana",
    playlist: "DevOps Fundamentals",
    duration: "18:42",
    savedAt: "Today",
    thumbnailClass: "from-cyan-500 via-blue-600 to-indigo-950",
    tags: ["Docker", "Networking"],
  },
  {
    id: "typescript-patterns",
    title: "10 TypeScript Patterns You Should Know",
    creator: "Fireship",
    playlist: "Frontend Deep Dives",
    duration: "12:08",
    savedAt: "Yesterday",
    thumbnailClass: "from-sky-500 via-blue-700 to-slate-950",
    tags: ["TypeScript", "Frontend"],
  },
  {
    id: "postgres-explained",
    title: "PostgreSQL Indexing Explained",
    creator: "Hussein Nasser",
    playlist: "Backend Systems",
    duration: "24:16",
    savedAt: "2 days ago",
    thumbnailClass: "from-amber-400 via-orange-600 to-stone-950",
    tags: ["PostgreSQL", "Databases"],
  },
  {
    id: "react-server-components",
    title: "React Server Components: The Mental Model",
    creator: "Vercel",
    playlist: "Frontend Deep Dives",
    duration: "20:31",
    savedAt: "4 days ago",
    thumbnailClass: "from-violet-500 via-fuchsia-600 to-slate-950",
    tags: ["React", "Next.js"],
  },
  {
    id: "system-design-cache",
    title: "Caching Strategies for System Design",
    creator: "ByteByteGo",
    playlist: "Backend Systems",
    duration: "15:19",
    savedAt: "Last week",
    thumbnailClass: "from-emerald-400 via-teal-600 to-slate-950",
    tags: ["System Design", "Caching"],
  },
  {
    id: "git-workflow",
    title: "A Git Workflow That Scales With Your Team",
    creator: "The Primeagen",
    playlist: "Developer Workflow",
    duration: "14:55",
    savedAt: "Last week",
    thumbnailClass: "from-rose-400 via-red-600 to-slate-950",
    tags: ["Git", "Workflow"],
  },
];

export const playlists = [
  { name: "DevOps Fundamentals", count: 18 },
  { name: "Frontend Deep Dives", count: 24 },
  { name: "Backend Systems", count: 16 },
  { name: "Developer Workflow", count: 12 },
];
