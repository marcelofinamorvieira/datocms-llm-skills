import { spawnSync } from 'node:child_process';

function run(args) {
  const result = spawnSync('npx', ['datocms', ...args], {
    stdio: 'inherit',
    shell: process.platform === 'win32',
  });

  if (result.status !== 0) {
    throw new Error(`Command failed: npx datocms ${args.join(' ')}`);
  }
}

const rawArgs = process.argv.slice(2);
const dryRun = rawArgs.includes('--dry-run');
const profiles = rawArgs.filter((arg) => arg !== '--dry-run');

if (profiles.length === 0) {
  console.error(
    'Usage: node scripts/datocms-sync-projects.mjs <profile...> [--dry-run]',
  );
  process.exit(1);
}

const timestamp = new Date().toISOString().replace(/[:.]/g, '-');

for (const profile of profiles) {
  const destination = `${profile}-sync-${timestamp}`;
  const args = [
    'migrations:run',
    `--profile=${profile}`,
    `--destination=${destination}`,
  ];

  if (dryRun) {
    args.push('--dry-run');
  }

  console.log(`\n==> ${profile} -> ${destination}`);
  run(args);
}
