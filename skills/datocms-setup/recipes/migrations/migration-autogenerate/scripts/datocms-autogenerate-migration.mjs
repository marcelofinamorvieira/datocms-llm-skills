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

function usage() {
  console.error(
    [
      'Usage:',
      '  node scripts/datocms-autogenerate-migration.mjs "<name>" --from=<env>',
      '    [--to=<env>] [--profile=<profile-id>] [--ts] [--js] [--schema=<filter>]',
    ].join('\n'),
  );
}

const rawArgs = process.argv.slice(2);

if (rawArgs.length === 0 || rawArgs.includes('--help')) {
  usage();
  process.exit(rawArgs.includes('--help') ? 0 : 1);
}

const name = rawArgs[0];
let from;
let to;
const passthroughArgs = [];

for (const arg of rawArgs.slice(1)) {
  if (arg.startsWith('--from=')) {
    from = arg.slice('--from='.length);
    continue;
  }

  if (arg.startsWith('--to=')) {
    to = arg.slice('--to='.length);
    continue;
  }

  passthroughArgs.push(arg);
}

if (!name || !from) {
  usage();
  process.exit(1);
}

const autogenerateTarget = to ? `${from}:${to}` : from;

run([
  'migrations:new',
  name,
  `--autogenerate=${autogenerateTarget}`,
  ...passthroughArgs,
]);
