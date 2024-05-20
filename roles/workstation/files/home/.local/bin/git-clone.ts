#!/usr/bin/env -S deno run --allow-all

/**
 * @file Run git clone and add upstream remote if possible
 * @copyright Zhangyuan Nie
 * @license MIT
 */

interface Repo {
  owner: string;
  name: string;
}

function parseRepo(s: string) {
  if (s.endsWith(".git") && s.includes("github")) {
    const r = s.match(/(?<owner>\w*)\/(?<name>\w*)\.git$/)?.groups;
    if (r && r.owner && r.name) {
      return r as unknown as Repo;
    }
  }
  return undefined;
}

async function git(...args: string[]) {
  const p = Deno.run({ cmd: ["git", ...args], stdout: "piped" });
  const output = new TextDecoder().decode(await p.output());
  const { success } = await p.status();
  p.close();
  if (!success) Deno.exit(1);
  return output;
}

// main

const repos: Repo[] = [];
for (const arg of Deno.args) {
  const r = parseRepo(arg);
  if (r) repos.push(r);
}

await git("clone", ...Deno.args);

for (const r of repos) {
  const body = await fetch(
    `https://api.github.com/repos/${r.owner}/${r.name}`,
    {
      method: "GET",
      headers: { "Accept": "application/vnd.github.v3+json" },
    },
  ).then((res) => res.json());

  if (body.fork) {
    const upstream = body.parent.clone_url;
    git("-C", `./${r.name}`, "remote", "add", "upstream", upstream);
  }
}
